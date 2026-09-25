#!/usr/bin/env python3
import json
import os

import requests
from requests import HTTPError

IAM_ENDPOINT = "https://iam.eu-de.otc.t-systems.com:443"
RMS_ENDPOINT = "https://rms.eu-de.otc.t-systems.com"


def check_required_environment_variables():
    required_variables = (
        "OTC_SDK_DOMAIN_ID",
        "OTC_USER_NAME",
        "OTC_USER_PASSWORD",
        "OTC_DOMAIN_NAME",
    )
    missing_variables = [
        variable for variable in required_variables if not os.environ.get(variable)
    ]
    if missing_variables:
        raise EnvironmentError(
            "Missing required environment variables: " + ", ".join(missing_variables)
        )


def token_iam(username, password, domain, https_insecure=False):
    """authenticate a user by password"""
    auth = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": username,
                        "password": password,
                        "domain": {"name": domain},
                    }
                },
            },
            "scope": {"domain": {"name": domain}},
        }
    }

    _session = requests.session()
    authstr = json.dumps(auth, indent=4)

    _token_url = f"{IAM_ENDPOINT}/v3/auth/tokens"

    if "X-Auth-Token" in _session.headers:
        del _session.headers["X-Auth-Token"]

    if https_insecure:
        response = _session.post(
            _token_url,
            data=authstr,
            verify=False,
            headers={"Content-Type": "application/json;charset=utf8"},
        )
    else:
        response = _session.post(
            _token_url,
            data=authstr,
            headers={"Content-Type": "application/json;charset=utf8"},
        )
    if response.status_code != 201:
        raise HTTPError(response=response)

    headers = response.headers
    token = headers["x-subject-token"]

    return token


def get_cloud_services(provider=None):
    headers = {
        "x-auth-token": token,
        "Content-Type": "application/json;charset=utf8",
    }
    _headers = headers
    _url = f"{RMS_ENDPOINT}/v1/resource-manager/domains/{os.environ.get('OTC_SDK_DOMAIN_ID')}/providers"

    _get_result = requests.get(_url, headers=_headers)
    _response_data = _get_result.json()

    _filtered_response_data = {
        "resource_providers": [
            {
                "provider": resource_provider.get("provider"),
                "display_name": resource_provider.get("display_name"),
                "resource_types": [
                    {
                        "name": resource_type.get("name"),
                        "display_name": resource_type.get("display_name"),
                        "regions": resource_type.get("regions"),
                    }
                    for resource_type in resource_provider.get("resource_types", [])
                ],
            }
            for resource_provider in _response_data.get("resource_providers", [])
            if not provider or resource_provider.get("provider") == provider
        ]
    }

    return _get_result.status_code, _filtered_response_data


def query_cloud_service_resource(provider, type, resource_id=None):
    _headers = {
        "x-auth-token": token,
        "Content-Type": "application/json;charset=utf8",
    }
    _url = f"{RMS_ENDPOINT}/v1/resource-manager/domains/{os.environ.get('OTC_SDK_DOMAIN_ID')}/provider/{provider}/type/{type}/resources"
    
    if resource_id:
        _url += f"/{resource_id}"

    _get_result = requests.get(_url, headers=_headers)
    print(f"Query Cloud Services Result: {_get_result.status_code}")
    _response_data = _get_result.json()
    print(json.dumps(_response_data, indent=2))

    return _get_result.status_code, _response_data


########################################################################
if __name__ == "__main__":
    check_required_environment_variables()
    token = token_iam(
        username=os.environ.get("OTC_USER_NAME"),
        password=os.environ.get("OTC_USER_PASSWORD"),
        domain=os.environ.get("OTC_DOMAIN_NAME"),
    )
    
    ###############################################################################################
    # Get all Cloud Services
    status, data = get_cloud_services()
    print(f"Get Cloud Services Status: {status}")
    print(json.dumps(data, indent=2))

    ###############################################################################################
    # Get Cloud Services for provider "ecs"
    status, data = get_cloud_services(provider="ecs")
    print(f"Get Cloud Services Status: {status}")
    print(json.dumps(data, indent=2))

    ###############################################################################################
    # Query Cloud Service Resource by provider "ecs" and type "cloudservers"
    status, data = query_cloud_service_resource(
        provider="ecs",
        type="cloudservers",
    )
    print(f"Query Cloud Service Resource Status: {status}")
    print(json.dumps(data, indent=2))
    
    ###############################################################################################
    # Query Cloud Service Resource by provider "ecs", type "cloudservers", and specific resource_id
    status, data = query_cloud_service_resource(
        provider="ecs",
        type="cloudservers",
        resource_id="cdb29bdd-1235-4e98-90d3-34bb77450393",
    )
    print(f"Query Cloud Service Resource Status: {status}")
    print(json.dumps(data, indent=2))
