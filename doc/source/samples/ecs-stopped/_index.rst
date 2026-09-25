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

      .. literalinclude:: ../../../../ecs-stopped/terraform/rms.tf
        :language: hcl
        :caption: ecs-stopped/terraform/rms.tf

      .. note:: 
        In **policy_filter** you need to adapt the **region** and **resource_id** to match your ECS instance.
   
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