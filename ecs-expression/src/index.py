import http.client
import json
import time

import requests

requests.packages.urllib3.disable_warnings()


"""
Get the policy resource representation for RMS.
"""


def get_policy_resource(domain_id, resource):
    return {
        "domain_id": domain_id,
        "region_id": resource.get("region_id"),
        "resource_id": resource.get("id"),
        "resource_name": resource.get("name"),
        "resource_provider": resource.get("provider"),
        "resource_type": resource.get("type"),
    }


"""
The evaluation result of a rule will be either Compliant or NonCompliant.
In this example, if ten or more ECSs are in the status of SHUTOFF, NonCompliant is returned. Otherwise, Compliant is returned.
Here, the Config advanced query API is used. You can use related APIs of other services as needed.
"""


def evaluate_compliance(context, domain_id):
    logger = context.getLogger()
    token = context.getToken()
    endpoint_url = context.getUserData("RMS_ENDPOINT_URL")
    
    # see: https://docs.otc.t-systems.com/config/api-ref/permissions_policies_and_supported_actions/advanced_queries.html
    url = f"{endpoint_url}/v1/resource-manager/domains/{domain_id}/run-query"

    body = {
        "expression": "select count(*) as cnt from resources where provider = 'ecs' and type = 'cloudservers' and properties.status = 'SHUTOFF'"
    }
    r = requests.post(
        url=url,
        json=body,
        headers={"X-Auth-Token": token},
        verify=False,
    )
    # on error: {'error_code': 'RMS.00010006', 'error_msg': 'You are not authorized with rms:resources:runQuery'}
    if r.status_code != http.client.OK:
        err = r.json()
        
        if err.get("error_code") == "RMS.00010006":
            logger.error("Check FunctionGraph agency IAM permissions: %s.", err.get("error_msg"))
        else:
            logger.error("Failed to run query: %s", err.get("error_msg"))
        
        return "Error"
      
    # example {"query_info":{"select_fields":["cnt"]},"results":[{"cnt":0}]}
    logger.info(r.json())
    cnt = r.json().get("results")[0].get("cnt")
    if cnt < 10:
        logger.info("%d Compliant", cnt)
        return "Compliant"
    else:
        logger.info("%d NonCompliant", cnt)
        return "NonCompliant"


"""
Update the policy state in RMS with the evaluation result.
"""


def update_policy_state(context, domain_id, evaluation):
    logger = context.getLogger()
    endpoint_url = context.getUserData("RMS_ENDPOINT_URL")
    url = f"{endpoint_url}/v1/resource-manager/domains/{domain_id}/policy-states"

    logger.info(
        "Updating policy state with URL: %s, payload: %s", url, json.dumps(evaluation)
    )

    return requests.put(
        url=url,
        headers={"X-Auth-Token": context.getToken()},
        json=evaluation,
        verify=False,
    )


"""
FunctionGraph handler to handle the incoming event and evaluate compliance for the resource.
"""


def handler(event, context):

    logger = context.getLogger()
    resource = event.get("invoking_event", {})

    if resource.get("name") != "Account":
        return

    logger.info("Event: %s", event)

    compliance_state = evaluate_compliance(context, event.get("domain_id"))
    
    if compliance_state == "Error":
        logger.error("Failed to evaluate compliance.")
        return { "statusCode": http.client.INTERNAL_SERVER_ERROR, "body": "Failed to evaluate compliance." }

    policy_state_payload = {
        "policy_resource": get_policy_resource(event.get("domain_id"), resource),
        "trigger_type": event.get("trigger_type"),
        "compliance_state": compliance_state,
        "policy_assignment_id": event.get("policy_assignment_id"),
        "policy_assignment_name": event.get("policy_assignment_name"),
        "function_urn": event.get("function_urn"),
        "evaluation_time": event.get("evaluation_time"),
        "evaluation_hash": event.get("evaluation_hash"),
    }

    for retry in range(3):
        response = update_policy_state(context, event.get("domain_id"), policy_state_payload)
        
        if response.status_code == http.client.TOO_MANY_REQUESTS:
            logger.error("TOO_MANY_REQUESTS: retry again, attempt %d", retry + 1)
            time.sleep(1)
        else:
            if response.status_code == http.client.OK:
                logger.info("Update policyState successfully.")
                return { "statusCode": http.client.OK, "body": "Update policy state successfully." }
            else:
                logger.error(
                    "Failed to update policyState with response: %s", response.json()
                )
            break
          
    return { "statusCode": http.client.INTERNAL_SERVER_ERROR, "body": "Failed to update policy state." }
