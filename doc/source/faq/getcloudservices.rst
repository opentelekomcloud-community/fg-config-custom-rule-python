How to get Cloud Services
===========================

.. toctree::
  :maxdepth: 1
  :hidden:


To query all cloud services, resources and regions, see 

- :docs_otc:`Listing Cloud Services <config/api-ref/apis/resource_query/listing_cloud_services.html>`

You can use :github_repo_master:`utils/getcloudservices.py <utils/getcloudservices.py>` execute the query.


Example Request
----------------

GET /v1/resource-manager/domains/{domain_id}/providers


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
        # Get Cloud Services for provider "ecs"
        status, data = get_cloud_services(provider="ecs")
        print(f"Get Cloud Services Status: {status}")
        print(json.dumps(data, indent=2))


.. code-block:: python
   :caption: Run the script:

   python3 utils/getcloudservices.py

.. code-block:: json
   :caption: Sample Response:
   :linenos:

    {
      "total_count" : 1,
      "resource_providers" : [ {
        "provider" : "ecs",
        "display_name" : "ECS",
        "category_display_name" : "Compute",
        "resource_types" : [ {
          "name" : "cloudservers",
          "display_name" : "Cloud servers",
          "global" : false,
          "regions" : [ "regionid1", "regionid2", "regionid3", "regionid4", "regionid5", "regionid6" ],
          "console_endpoint_id" : "ecm",
          "console_list_url" : "#/ecs/manager/vmList",
          "console_detail_url" : "#/ecs/manager/ecsDetail?instanceId={id}",
          "track" : "tracked"
        } ]
      } ]
    }

Here you will find:

 - line (4): provider name: **ecs**
 - line (8): resource_types.name: **cloudservers**

