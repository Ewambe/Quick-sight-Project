resource "aws_sns_topic" "report_notification_topic" {
  name = "ReportNotificationTopic"
}

resource "aws_lambda_permission" "sns_permission" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.json_to_csv_lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn   = aws_sns_topic.report_notification_topic.arn
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.report_notification_topic.arn
  protocol  = "email"
  endpoint  = "your-email@example.com" # Update with your email address
}
