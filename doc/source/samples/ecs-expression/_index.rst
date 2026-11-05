Sample to check if a max number of ECS instances are running
=============================================================

.. toctree::
    :maxdepth: 1
    :hidden:


This example demonstrates how to check periodically (Once per Hour) if a max number of ECSs are running.

If ten or more ECSs are in the status of SHUTOFF, **NonCompliant** is returned.
Otherwise, **Compliant** is returned.

Prerequisites
-------------

Before running this example, ensure you have the following:

- :ref:`prerequisites`
- A number of ECS instances that you want to check.

FunctionGraph function
-----------------------

.. literalinclude:: ../../../../ecs-expression/src/index.py
  :language: python
  :caption: ecs-expression/src/index.py

Terraform deployment files
--------------------------

FunctionGraph deployment files
""""""""""""""""""""""""""""""""""""""""""""""
.. tabs::

    .. tab:: Function

      .. literalinclude:: ../../../../ecs-expression/terraform/function.tf
        :language: hcl
        :caption: ecs-expression/terraform/function.tf
   
    .. tab:: Function Agency

      .. literalinclude:: ../../../../ecs-expression/terraform/function-agency.tf
        :language: hcl
        :caption: ecs-expression/terraform/function-agency.tf

    .. tab:: Function LogGroup

      .. literalinclude:: ../../../../ecs-expression/terraform/function-logging.tf
        :language: hcl
        :caption: ecs-expression/terraform/function-logging.tf

Config deployment files
""""""""""""""""""""""""""""""""""""""""""""""
.. tabs::

    .. tab:: Config

      .. literalinclude:: ../../../../ecs-expression/terraform/rms.tf
        :language: hcl
        :caption: ecs-expression/terraform/rms.tf
           
    .. tab:: Config Agency

      .. literalinclude:: ../../../../ecs-expression/terraform/rms-agency.tf
        :language: hcl
        :caption: ecs-expression/terraform/rms-agency.tf


Variables
""""""""""""""""""""""""""""""""""""""""""""""

Sample variables file:

.. literalinclude:: ../../../../ecs-expression/terraform/variables.tfvars
  :language: hcl
  :caption: ecs-expression/terraform/variables.tfvars


You might want to adjust the variables to your need.

Makefile
""""""""""""""""""""""""""""""""""""""""""""""

Sample Makefile:

.. literalinclude:: ../../../../ecs-expression/Makefile
  :language: make
  :caption: ecs-expression/Makefile

You might want to adjust the following variables to your need:

.. code-block:: make

    # Terraform backend configuration
    BACKEND_CONFIG_BUCKET := "doc-samples-tf-backend"
    BACKEND_CONFIG_KEY := "terraform_state/python/custom-rule-ecs-expression.tf"
    BACKEND_CONFIG_REGION := "eu-de"
    BACKEND_CONFIG_ENDPOINTS := "endpoints={s3=\"https://obs.eu-de.otc.t-systems.com\"}"


Deploy
--------------

To deploy using Terraform run:

.. code-block:: bash

    make tf_apply

To destroy the deployed resources using Terraform run:

.. code-block:: bash

    make tf_destroy
