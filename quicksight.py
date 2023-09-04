import json
import boto3
import botocore
import time
import os  # Import the 'os' module to work with environment variables

# Initialize QuickSight client
quicksight_client = boto3.client('quicksight', region_name=os.environ.get('AWS_REGION'))  # Use environment variable for the region

def lambda_handler(event, context):
    try:
        # Parse the S3 event triggered by the CSV file upload
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        s3_key = event['Records'][0]['s3']['object']['key']

        # Define a unique dataset and analysis name
        dataset_name = os.environ.get('DATASET_NAME', 'MyDatasetName')
        analysis_name = os.environ.get('ANALYSIS_NAME', 'MyAnalysisName')

        # Create a dataset
        dataset_response = create_dataset(s3_bucket, s3_key, dataset_name)

        # Create an analysis
        analysis_response = create_analysis(dataset_name, analysis_name)

        # Optionally, create a dashboard
        dashboard_name = os.environ.get('DASHBOARD_NAME', 'MyDashboardName')
        dashboard_response = create_dashboard(analysis_name, dashboard_name)

        return {
            'statusCode': 200,
            'body': json.dumps('CSV file successfully sent to QuickSight for analysis and dashboard creation.')
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def create_dataset(s3_bucket, s3_key, dataset_name):
    # Define dataset configuration
    dataset_config = {
        'DataSetId': dataset_name,
        'Name': dataset_name,
        'PhysicalTableMap': {
            'csv': {
                'S3Source': {
                    'DataSourceArn': f'arn:aws:s3:::{s3_bucket}/{s3_key}',
                    'UploadSettings': {
                        'Format': 'CSV',
                        'StartFromRow': int(os.environ.get('START_FROM_ROW', '2')),  # Use environment variable
                        'ContainsHeader': bool(os.environ.get('CONTAINS_HEADER', 'True'))  # Use environment variable
                    },
                    'InputColumns': [  # Define your input columns here
                        {
                            'Name': 'item_name',  # Replace with your column name
                            'Type': os.environ.get('ITEM_NAME_TYPE', 'STRING')  # Use environment variable
                        },
                        {
                            'Name': 'revenue',
                            'Type': os.environ.get('REVENUE_TYPE', 'DECIMAL')  # Use environment variable
                        },
                        {
                            'Name': 'cogs',
                            'Type': os.environ.get('COGS_TYPE', 'DECIMAL')  # Use environment variable
                        }
                        # Add more columns as needed
                    ]
                }
            }
        },
        'ImportMode': os.environ.get('IMPORT_MODE', 'SPICE')  # Use environment variable
    }

    # Create dataset
    response = quicksight_client.create_data_set(
        AwsAccountId=os.environ.get('AWS_ACCOUNT_ID'),  # Use environment variable
        DataSetId=dataset_name,
        Name=dataset_name,
        PhysicalTableMap=dataset_config['PhysicalTableMap'],
        ImportMode=dataset_config['ImportMode']
    )

    return response

def create_analysis(dataset_name, analysis_name):
    # Define analysis configuration
    analysis_config = {
        'Name': analysis_name,
        'SourceEntity': {
            'SourceTemplate': {
                'DataSetReferences': [
                    {
                        'DataSetArn': f'arn:aws:quicksight:{os.environ.get("AWS_REGION")}:dataset/{dataset_name}',
                        'DataSetPlaceholder': 'ds'
                    }
                ],
                'Arn': os.environ.get('TEMPLATE_ARN', 'arn:aws:quicksight:template/YOUR_TEMPLATE_ID')  # Use environment variable
            }
        }
    }

    # Create analysis
    response = quicksight_client.create_analysis(
        AwsAccountId=os.environ.get('AWS_ACCOUNT_ID'),  # Use environment variable
        AnalysisId=analysis_name,
        Name=analysis_name,
        SourceEntity=analysis_config['SourceEntity']
    )

    return response

def create_dashboard(analysis_name, dashboard_name):
    # Define dashboard configuration
    dashboard_config = {
        'Name': dashboard_name,
        'SourceEntity': {
            'Analysis': {
                'Arn': f'arn:aws:quicksight:{os.environ.get("AWS_REGION")}:analysis/{analysis_name}',
                'DataSetArns': []
            }
        }
    }

    # Create dashboard
    response = quicksight_client.create_dashboard(
        AwsAccountId=os.environ.get('AWS_ACCOUNT_ID'),  # Use environment variable
        DashboardId=dashboard_name,
        Name=dashboard_name,
        SourceEntity=dashboard_config['SourceEntity']
    )

    return response

def generate_presigned_url(s3_bucket, s3_key):
    # Generate a pre-signed URL for the QuickSight report
    expiration_time = 3600  # Set the expiration time for the URL (in seconds)
    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': os.environ.get('S3_BUCKET_NAME', 'YOUR_S3_BUCKET_NAME'),  # Use environment variable
            'Key': os.environ.get('REPORT_OBJECT_KEY', 'reports/my_report.pdf')  # Use environment variable
        },
        ExpiresIn=expiration_time
    )

    return presigned_url

