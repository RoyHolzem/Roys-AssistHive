output "lambda_preprocessor_arn" {
  description = "ARN of the preprocessor Lambda function"
  value       = aws_lambda_function.preprocessor.arn
}

output "lambda_classifier_arn" {
  description = "ARN of the classifier Lambda function"
  value       = aws_lambda_function.classifier.arn
}

output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = aws_api_gateway_rest_api.assist_hive_api.execution_arn
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_rds_instance.mysql.endpoint
}
