##########################################################
# Python event function to handle ECS stopped compliance
##########################################################
resource "opentelekomcloud_fgs_function_v2" "MyFunction" {

  name   = format("%s_%s", var.prefix, var.function_name)
  app    = "default"
  
  handler =  var.handler_name

  runtime   = "Python3.10"

  agency = opentelekomcloud_identity_agency_v3.agency.name  

  code_type = "inline"
  func_code     = filebase64(format("${path.module}/../%s", "src/index.py"))
  code_filename = "index.py"

  description      = var.description
  memory_size      = 128
  timeout          = 30
  max_instance_num = 10

  log_group_id   = opentelekomcloud_lts_group_v2.MyLogGroup.id
  log_group_name = opentelekomcloud_lts_group_v2.MyLogGroup.group_name

  log_topic_id   = opentelekomcloud_lts_stream_v2.MyLogStream.id
  log_topic_name = opentelekomcloud_lts_stream_v2.MyLogStream.stream_name

  # set some environment variables
  user_data = jsonencode({
    "RMS_ENDPOINT_URL" : "https://rms.eu-de.otc.t-systems.com"
  })

  tags = {
    "app_group" = var.tag_app_group
  }

}

output "MY_FUNCTION_URN" {
  value = opentelekomcloud_fgs_function_v2.MyFunction.urn
}

output "MY_FUNCTION_VERSION" {
  value = opentelekomcloud_fgs_function_v2.MyFunction.version
}