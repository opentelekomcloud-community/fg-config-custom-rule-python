# -*- coding:utf-8 -*-

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
In this example, if the properties.status of a resource matches the specified ECSstatus,
NonCompliant is returned. Otherwise, Compliant is returned.
"""


def evaluate_compliance(logger, resource, parameter):

    if resource.get("properties").get("status") == parameter.get("ECSstatus").get(
        "value"
    ):
        logger.info("NonCompliant")
        return "NonCompliant"
    else:
        logger.info("Compliant")
        return "Compliant"


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

    logger.debug("Invoking event: %s", json.dumps(event))

    resource = event.get("invoking_event", {})
    parameters = event.get("rule_parameter", {})

    compliance_state = evaluate_compliance(logger, resource, parameters)

    requests = {
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
        response = update_policy_state(context, event.get("domain_id"), requests)
        if response.status_code == http.client.TOO_MANY_REQUESTS:
            logger.error("TOO_MANY_REQUESTS: retry again, attempt %d", retry + 1)
            time.sleep(1)
        else:
            if response.status_code == http.client.OK:
                logger.info("Update policyState successfully.")
            else:
                logger.error("Failed to update policyState with response: %s", response.json())
            break
