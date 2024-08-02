variable "rds_host" {
  description = "RDS database host"
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "model_bucket_name" {
  description = "S3 bucket name for storing the model"
  type        = string
}

variable "model_key" {
  description = "S3 key for the model file"
  type        = string
}

variable "vectorizer_key" {
  description = "S3 key for the vectorizer file"
  type        = string
}
