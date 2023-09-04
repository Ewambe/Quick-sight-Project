# Define variables for AWS account ID and other configuration values
variable "aws_account_id" {
  description = "Your AWS Account ID"
  default = "AWSAccountID"
  type        = string
}

variable "dataset_name" {
  description = "Name for the QuickSight dataset"
  default     = "MyDatasetName"
  type        = string
}

variable "analysis_name" {
  description = "Name for the QuickSight analysis"
  default     = "MyAnalysisName"
  type        = string
}

variable "analysis_id" {
  description = "ID for the QuickSight analysis"
  default     = "Update with a unique ID"
  type        = string
}

variable "dashboard_name" {
  description = "Name for the QuickSight dashboard"
  default     = "MyDashboardName"
  type        = string
}

variable "dashboard_id" {
  description = "ID for the QuickSight dashboard"
  default     = "Update with a unique ID"
  type        = string
}


variable "data_set_id" {
  description = "Unique ID"
  default     = "Update with a unique ID"
  type        = string
}

variable "SOURCE_BUCKET" {
  description = "The source bucket for your Lambda functions"
  default = "bucketname"
  type        = string
}

variable "DESTINATION_BUCKET" {
  description = "The destination bucket for your Lambda functions"
  default = "bucketname"
  type        = string
}



