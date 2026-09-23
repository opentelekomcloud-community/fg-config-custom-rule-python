##################################################################
# Custom role to allow FunctionGraph to update RMS policy states
##################################################################
resource "opentelekomcloud_identity_role_v3" "role" {
  display_name  = format("%s-%s-role", var.prefix, var.function_name)
  description   = "Role for FunctionGraph to update RMS policy states"
  display_layer = "project"

  statement {
    effect = "Allow"
    action = [
      "rms:policyStates:update"
    ]    
  }

}

##########################################################
# Agency for FunctionGraph
# Attention: Creating agency will take some time.
# Calls to function after creating agency will fail until
# agency is set up.
##########################################################
resource "opentelekomcloud_identity_agency_v3" "agency" {
  depends_on            = [opentelekomcloud_identity_role_v3.role]
  delegated_domain_name = "op_svc_cff"

  name        = format("%s-%s-agency", var.prefix, var.function_name)
  description = "Agency for FunctionGraph to access RMS"

  project_role {
    all_projects = true
    # project      = var.OTC_SDK_PROJECTNAME
    roles = [
      opentelekomcloud_identity_role_v3.role.display_name
    ]
  }

}