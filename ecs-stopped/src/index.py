# -*- coding:utf-8 -*-

import http.client
import json
import time

import requests

requests.packages.urllib3.disable_warnings()


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
Setting Logic
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


def update_policy_state(context, domain_id, evaluation):
    endpoint_url = context.getUserData("RMS_ENDPOINT_URL")
    url = f"{endpoint_url}/v1/resource-manager/domains/{domain_id}/policy-states"

    context.getLogger().info("Updating policy state with URL: %s", url)
    context.getLogger().info("Evaluation payload: %s", json.dumps(evaluation))

    return requests.put(
        url=url,
        headers={"X-Auth-Token": context.getToken()},
        json=evaluation,
        verify=False,
    )


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
            logger.error("TOO_MANY_REQUESTS: retry again")
            time.sleep(1)
        else:
            if response.status_code == http.client.OK:
                logger.info("Update policyState successfully.")
            else:
                logger.error("Failed to update policyState.")
                logger.error(response.json())
            break
