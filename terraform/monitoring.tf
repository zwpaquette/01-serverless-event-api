resource "aws_cloudwatch_dashboard" "lambda_dashboard" {
  dashboard_name = "${var.project_name}-dashboard"
  dashboard_body = jsonencode({
    widgets = [
      {
        "type": "metric",
        "x": 0, "y": 0, "width": 12, "height": 6,
        "properties": {
          "title": "Lambda Invocations vs Errors",
          "region": var.region,
          "stat": "Sum",
          "period": 300,
          "metrics": [
            [ "AWS/Lambda", "Invocations", "FunctionName", aws_lambda_function.api_lambda.function_name ],
            [ ".",          "Errors",      ".",            "." ]
          ]
        }
      }
    ]
  })
}
