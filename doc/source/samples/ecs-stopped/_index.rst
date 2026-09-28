Sample to check if an ECS instance is stopped
================================================

.. toctree::
    :maxdepth: 1
    :hidden:


This example demonstrates how to verify whether an Elastic Cloud Server (ECS) instance is in a stopped state using a custom rule.

Prerequisites
-------------

Before running this example, ensure you have the following:

- :ref:`prerequisites`
- An existing ECS instance that you want to check.


FunctionGraph function
-----------------------

.. literalinclude:: ../../../../ecs-stopped/src/index.py
  :language: python
  :caption: ecs-stopped/src/index.py

.. note::
  The parameter **ECSstatus** is defined in the config deployment file in
  :ref:`opentelekomcloud_rms_policy_assignment_v1.my_policy_assignment<ecs_policy_assignment>`
  
  .. code-block:: hcl

    parameters = {  
      ECSstatus = "\"SHUTOFF\""
    }


Terraform deployment files
--------------------------

FunctionGraph deployment files
""""""""""""""""""""""""""""""""""""""""""""""
.. tabs::

    .. tab:: Function

      .. literalinclude:: ../../../../ecs-stopped/terraform/function.tf
        :language: hcl
        :caption: ecs-stopped/terraform/function.tf
   
    .. tab:: Function Agency

      .. literalinclude:: ../../../../ecs-stopped/terraform/function-agency.tf
        :language: hcl
        :caption: ecs-stopped/terraform/function-agency.tf

    .. tab:: Function LogGroup

      .. literalinclude:: ../../../../ecs-stopped/terraform/function-logging.tf
        :language: hcl
        :caption: ecs-stopped/terraform/function-logging.tf

Config deployment files
""""""""""""""""""""""""""""""""""""""""""""""
.. tabs::

    .. tab:: Config

      .. _ecs_policy_assignment:

      .. literalinclude:: ../../../../ecs-stopped/terraform/rms.tf
        :language: hcl
        :caption: ecs-stopped/terraform/rms.tf

      .. note:: 
        - In **policy_filter** you need to adapt the **region** and **resource_id** to match your ECS instance.

        - For getting values for **resource_provider** and **resource_type**
          see :ref:`FAQ: Listing Cloud Services <sample_response_cloudservices>`.

        - The Parameter **ECSstatus** configured in **parameters = {}** is used in the FunctionGraph function for comparison.

            .. code-block:: python
              :caption: def evaluate_compliance() in index.py

                # ...
                if resource.get("properties").get("status") == parameter.get("ECSstatus").get("value"):
                # ...

          For possible values for **ECSstatus**, see the :ref:`FAQ: How to get Resource Details <sample_response_resourcedetails>`.
          Execute the script for every change in the ECS instance status and check value of **resources.properties.status**. 
           
    .. tab:: Config Agency

      .. literalinclude:: ../../../../ecs-stopped/terraform/rms-agency.tf
        :language: hcl
        :caption: ecs-stopped/terraform/rms-agency.tf


Variables
""""""""""""""""""""""""""""""""""""""""""""""

Sample variables file:

.. literalinclude:: ../../../../ecs-stopped/terraform/variables.tfvars
  :language: hcl
  :caption: ecs-stopped/terraform/variables.tfvars


You might want to adjust the variables to your need.

Makefile
""""""""""""""""""""""""""""""""""""""""""""""

Sample Makefile:

.. literalinclude:: ../../../../ecs-stopped/Makefile
  :language: make
  :caption: ecs-stopped/Makefile

You might following variables to your need:

.. code-block:: 

    # Terraform backend configuration
    BACKEND_CONFIG_BUCKET := "doc-samples-tf-backend"
    BACKEND_CONFIG_KEY := "terraform_state/python/custom-rule-ecs-stopped.tf"
    BACKEND_CONFIG_REGION := "eu-de"
    BACKEND_CONFIG_ENDPOINTS := "endpoints={s3=\"https://obs.eu-de.otc.t-systems.com\"}"


Deploy
--------------

To deploy using Terraform run:

.. code-block:: bash

    make tf_deploy

To destroy the deployed resources using Terraform run:

.. code-block:: bash

    make tf_destroy