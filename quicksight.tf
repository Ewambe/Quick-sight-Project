resource "aws_quicksight_data_set" "my_dataset" {
  name    = "var.dataset_name"
  data_set_id = "var.dataset_id" # Update with a unique ID
  aws_account_id = "var.aws_account_id" # Replace with your AWS account ID
  physical_table_map  {
    physical_table_map_id = "example-id"
    s3_source = {
        data_source_arn = "arn:aws:s3:::your-source-bucket/your-source-key"
        upload_settings = {
          format = "CSV"
          start_from_row = 2
          contains_header = true
        }
        input_columns = [
          {
            name = "item_name"
            type = "STRING"
          },
          {
            name = "revenue"
            type = "DECIMAL"
          },
          {
            name = "cogs"
            type = "DECIMAL"
          }
        ]
    }
  }
  import_mode = "SPICE"
}

resource "aws_quicksight_analysis" "my_analysis" {
  name            = "var.analysis.name"
  analysis_id     = "var.analysis.id" # Update with a unique ID
  aws_account_id  = "var.aws_account_id" # Replace with your AWS account ID

  source_entity {
    source_template {
      data_set_references {
        data_set_arn         = aws_quicksight_data_set.my_dataset
        data_set_placeholder = "ds"
      }
      arn = "arn:aws:quicksight:us-east-1:YOUR_ACCOUNT_ID:template/YOUR_TEMPLATE_ID" # Replace with your template ARN
    }
  }
}

resource "aws_quicksight_dashboard" "my_dashboard" {
  name            = "var.dashboard_name"
  dashboard_id    = "var.dashboard_id" # Update with a unique ID
  aws_account_id  = "var.aws_account_id" # Replace with your AWS account ID
  version_description = "Dashboard version description"
    source_entity {
    source_template {
      arn = aws_quicksight_template.source.arn
      data_set_references {
        data_set_arn         = aws_quicksight_data_set.dataset.arn
        data_set_placeholder = "1"
      }
    }
    }
}


