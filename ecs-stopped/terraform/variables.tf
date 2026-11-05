# prefix will be prepended to all resource names
variable "prefix" {
  type    = string
  default = "set in variables.tfvars"
}

# description of the function
variable "description" {
  type    = string
  default = "set in variables.tfvars"
}

# FunctionGraph: Function name
variable "function_name" {
  type    = string
  default = "set in variables.tfvars"
}

variable "handler_name" {
  type    = string
  default = "set in variables.tfvars"
}

# Resource tag:
variable "tag_app_group" {
  type    = string
  default = "set in variables.tfvars"
}

variable "ecs_instance_id" {
  type    = string
  default = "set in variables.tfvars"
}
