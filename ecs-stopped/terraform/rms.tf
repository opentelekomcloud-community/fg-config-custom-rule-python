#######################################################################
# Policy assignment for FunctionGraph to manage ECS stopped compliance
#######################################################################
resource "opentelekomcloud_rms_policy_assignment_v1" "my_policy_assignment" {
  name        = format("%s-%s", var.prefix, "Stopped_ECS_is_nonCompliant")
  description = "Policy assignment for FunctionGraph"

  custom_policy {
    auth_type = "agency"
    auth_value = {
      agency_name = format("\"%s\"", opentelekomcloud_identity_agency_v3.config_agency.name)
    }
    function_urn = format("%s:%s", opentelekomcloud_fgs_function_v2.MyFunction.urn, opentelekomcloud_fgs_function_v2.MyFunction.version)
  }

  parameters = {
    "ECSstatus": "\"SHUTOFF\""
  }

  period = ""
  
  policy_filter {
    region = "eu-de"
    resource_id = "cdb29bdd-1235-4e98-90d3-34bb77450393"
    resource_provider = "ecs"
    resource_type = "cloudservers"
    tag_key = ""
    tag_value = ""
  }
  status = "Enabled"

    
}