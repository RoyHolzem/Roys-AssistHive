resource "aws_s3_bucket" "assist_hive_bucket" {
  bucket = "assist-hive-bucket"
}

resource "aws_lambda_function" "preprocessor" {
  function_name = "preprocessor"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"

  layers = [
    "arn:aws:lambda:eu-north-1:080732204754:layer:pymysql:1",
    "arn:aws:lambda:eu-north-1:080732204754:layer:nltk_with_data:2",
    "arn:aws:lambda:eu-north-1:080732204754:layer:regex:1"
  ]

  environment {
    variables = {
      RDS_HOST     = var.rds_host
      DB_USERNAME  = var.db_username
      DB_PASSWORD  = var.db_password
      DB_NAME      = var.db_name
    }
  }


  filename         = "lambda/preprocessor.zip"
  source_code_hash = filebase64sha256("lambda/preprocessor.zip")
}

resource "aws_lambda_function" "classifier" {
  function_name = "classifier"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"

  layers = [
    "arn:aws:lambda:eu-north-1:080732204754:layer:scikit:2"
    ]

  environment {
    variables = {
      MODEL_BUCKET_NAME = var.model_bucket_name
      MODEL_KEY         = var.model_key
      VECTORIZER_KEY    = var.vectorizer_key
    }
  }

  # Additional lambda configurations memory size, timeout, etc.
  memory_size = 512
  timeout     = 30

  filename         = "lambda/classifier.zip"
  source_code_hash = filebase64sha256("lambda/classifier.zip")
}

resource "aws_api_gateway_rest_api" "assist_hive_api" {
  name        = "assist-hive-api"
  description = "API Gateway for AssistHive project"
}

resource "aws_rds_instance" "mysql" {
  identifier              = "customerdata"
  engine                  = "mysql"
  instance_class          = "db.t2.micro"
  allocated_storage       = 20
  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids  = [aws_security_group.default.id]
  username                = var.db_username
  password                = var.db_password
  publicly_accessible     = false
  skip_final_snapshot     = true
  apply_immediately       = true
}

resource "aws_cloudwatch_dashboard" "assisthive_dashboard" {
  dashboard_name = "AssistHiveDashboard"
  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        x = 0
        y = 0
        width = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/Lambda", "Invocations", "FunctionName", aws_lambda_function.preprocessor.function_name],
            [".", "Errors", ".", "."],
            ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", aws_rds_instance.mysql.id]
          ]
          view = "timeSeries"
          stacked = false
          region = "eu-north-1"
          title = "Lambda & RDS Monitoring"
        }
      }
    ]
  })
}

resource "aws_s3_bucket" "model_bucket" {
  bucket = "assisthive-model-bucket"
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "LambdaS3AccessPolicy"
  description = "Policy for Lambda to access S3 buckets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = [
          "${aws_s3_bucket.assist_hive_bucket.arn}/*",
          "${aws_s3_bucket.model_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_access" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
