# Terraform variables for scratch-event sample

# prefix of all resources
prefix        = "python"

# description of the function
description = "Custom rule for ECS stopped state"

# name of the function (will be prefixed)
function_name = "custom-rule-ecs-stopped"

# handler function name defined in your code, e.g. "index.handler"
handler_name = "index.handler"

# resources will be tagged with this app_group tag
tag_app_group = "custom-rule-ecs-stopped"
