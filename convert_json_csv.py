import json
import csv
import boto3
import os  # Added import for environment variables

# Initialize S3 clients for source and destination buckets
s3_client_source = boto3.client('s3')
s3_client_destination = boto3.client('s3')

# Retrieve environment variables
SOURCE_BUCKET = os.environ['SOURCE_BUCKET']
DESTINATION_BUCKET = os.environ['DESTINATION_BUCKET']

def lambda_handler(event, context):
    # Get the S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Check if the file is a JSON file
    if key.endswith('.json'):
        # Download the JSON file from S3
        try:
            response = s3_client_source.get_object(Bucket=bucket, Key=key)
            json_content = response['Body'].read().decode('utf-8')
            json_data = json.loads(json_content)

            # Extract the data and write to a CSV file
            extracted_data = extract_json_data(json_data)
            csv_filename = key.replace('.json', '.csv')
            csv_path = '/tmp/' + csv_filename
            with open(csv_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['item_name', 'revenue', 'cogs'])  # Write header
                csv_writer.writerows(extracted_data)  # Write data rows

            # Upload the CSV file to the destination S3 bucket
            s3_client_destination.upload_file(csv_path, DESTINATION_BUCKET, csv_filename)
            return f'CSV file created and uploaded to S3: s3://{DESTINATION_BUCKET}/{csv_filename}'
        except Exception as e:
            return f'Error: {str(e)}'
    else:
        return f'File {key} is not a JSON file, no action taken.'

def extract_json_data(json_data):
    extracted_data = []
    for item in json_data['sales_data']:
        item_name = item['item_name']
        revenue = item['revenue']
        cogs = item['cogs']
        extracted_data.append([item_name, revenue, cogs])
    return extracted_data

