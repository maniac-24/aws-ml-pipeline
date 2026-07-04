import json
import csv
import boto3
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    print(f"New file uploaded: {file_name} in bucket: {bucket_name}")
    
    # Only process if it's a CSV file
    if file_name.endswith('.csv'):
        # Download the actual file content from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read().decode('utf-8-sig')
        
        # Parse the CSV content into rows
        csv_reader = csv.DictReader(io.StringIO(content))
        rows = list(csv_reader)
        
        print(f"CSV has {len(rows)} rows")
        for row in rows:
            print(row)
    else:
        print(f"Skipping {file_name} - not a CSV file")
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed {file_name} from {bucket_name}')
    }