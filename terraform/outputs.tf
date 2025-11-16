output "api_endpoint" {
  value = aws_apigatewayv2_api.api.api_endpoint
}

output "dynamodb_table" {
  value = aws_dynamodb_table.items.name
}

