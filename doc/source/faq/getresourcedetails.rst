How to get Resource Details
=============================

.. toctree::
  :maxdepth: 1
  :hidden:

To get details of a specific resource, see following sections in the **Config User Guide**:

-  :docs_otc:`Quering a Resource <config/api-ref/apis/resource_query/querying_a_resource.html>`
-  :docs_otc:`Querying Resources of a Specific Type <config/api-ref/apis/resource_query/querying_resources_of_a_specific_type.html>`


Example Request 
----------------

GET /v1/resource-manager/domains/{domain_id}/provider/{provider}/type/{type}/resources/{resource_id} 

Example
""""""""

You can use :github_repo_master:`utils/getcloudservices.py <utils/getcloudservices.py>` execute the query.

with following Python code:

.. code-block:: python
   :caption: Adaptions

    # .....
    if __name__ == "__main__":
        check_required_environment_variables()
        token = token_iam(
            username=os.environ.get("OTC_USER_NAME"),
            password=os.environ.get("OTC_USER_PASSWORD"),
            domain=os.environ.get("OTC_DOMAIN_NAME"),
        )

        ###############################################################################################
        # Query Cloud Service Resource by provider "ecs", type "cloudservers", and specific resource_id
        status, data = query_cloud_service_resource(
            provider="ecs",
            type="cloudservers",
            resource_id="7ffd8564-d88a-4bc9-ab51-d8b79a57d0e6",
        )
        print(f"Query Cloud Service Resource Status: {status}")
        print(json.dumps(data, indent=2))    


.. code-block:: python
   :caption: Run the script:

   python3 utils/getcloudservices.py


.. code-block:: json
   :caption: Sample Response:
   :linenos:

    {
      "page_info" : {
        "current_count" : 1,
        "next_marker" : null
      },
      "resources" : [ {
        "checksum" : "89ca775e88e04b2c200ccbf9e219ad0d7da42e3f446e5c953d443288134eec41",
        "created" : "2020-02-21T08:41:05Z",
        "ep_id" : "0",
        "ep_name" : "default",
        "id" : "7ffd8564-d88a-4bc9-ab51-d8b79a57d0e6",
        "name" : "ecs-test-1",
        "project_id" : "059b5e0a2500d5552fa1c00adada8c06",
        "project_name" : "project_name",
        "properties" : {
          "status" : "ACTIVE"
        },
        "provider" : "ecs",
        "provisioning_state" : "Succeeded",
        "region_id" : "regionid1",
        "tags" : {
          "use" : "test"
        },
        "type" : "cloudServers",
        "updated" : "2020-02-21T08:41:05Z"
      } ]
    }

