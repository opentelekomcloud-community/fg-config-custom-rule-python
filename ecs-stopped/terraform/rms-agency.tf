##################################################################
# Custom role to allow RMS to execute FunctionGraph functions
##################################################################
resource "opentelekomcloud_identity_role_v3" "fg-role" {
  display_name  = format("%s-%s-config-role", var.prefix, var.function_name)
  description   = "Role for RMS to execute FunctionGraph functions"
  display_layer = "project"

  statement {
    effect = "Allow"
    action = [
      #"functiongraph:function:invoke",
      "functiongraph:*:*",
    ]
    # resource = [
    #   format("FunctionGraph:*:%s:function:%s/%s",
    #   var.OTC_SDK_DOMAIN_ID,
    #   opentelekomcloud_fgs_function_v2.MyFunction.app,
    #   opentelekomcloud_fgs_function_v2.MyFunction.name)
    # ]
  }

}

#################################################################
# Config agency for RMS to access FunctionGraph
#################################################################
resource "opentelekomcloud_identity_agency_v3" "config_agency" {
  name        = format("%s-%s-config-agency", var.prefix, var.function_name)
  description = "Config agency for FunctionGraph access"

  delegated_domain_name = "op_svc_rms"

  project_role {
    all_projects = true
    # project      = var.OTC_SDK_PROJECTNAME
    roles = [
      #"FunctionGraph FullAccess"
      opentelekomcloud_identity_role_v3.fg-role.display_name
    ]
  }

}
