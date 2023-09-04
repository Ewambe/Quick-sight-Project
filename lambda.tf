

resource "aws_lambda_function" "json_to_csv_lambda" {
  function_name = "json-to-csv-lambda"
  handler = "index.lambda_handler"
  runtime = "python3.9"
  role    = aws_iam_role.lambda_role.arn
  filename = "path/to/your/deployment-package.zip" # Update with your deployment package
  source_code_hash = filebase64sha256("path/to/your/deployment-package.zip")

  environment {
     variables = {
      SOURCE_BUCKET      = var.SOURCE_BUCKET
      DESTINATION_BUCKET = var.DESTINATION_BUCKET
    }
  }
}

resource "aws_lambda_function" "quicksight_integration_lambda" {
  function_name = "quicksight-integration-lambda"
  handler = "index.lambda_handler"
  runtime = "python3.9"
  role    = aws_iam_role.lambda_role.arn
  filename = "path/to/your/deployment-package.zip" # Update with your deployment package
  source_code_hash = filebase64sha256("path/to/your/deployment-package.zip")

   environment {
    variables = {
      AWS_REGION          = "your region"
      DATASET_NAME        = "MyDatasetName"
      ANALYSIS_NAME       = "MyAnalysisName"
      DASHBOARD_NAME      = "MyDashboardName"
      START_FROM_ROW      = "2"
      CONTAINS_HEADER     = "True"
      ITEM_NAME_TYPE      = "STRING"
      REVENUE_TYPE        = "DECIMAL"
      COGS_TYPE           = "DECIMAL"
      IMPORT_MODE         = "SPICE"
      AWS_ACCOUNT_ID      = "YourAWSAccountID"
      TEMPLATE_ARN        = "arn:aws:quicksight:template/YOUR_TEMPLATE_ID"
      S3_BUCKET_NAME      = "YOUR_S3_BUCKET_NAME"
      REPORT_OBJECT_KEY   = "reports/my_report.pdf"
    }
  }
}

