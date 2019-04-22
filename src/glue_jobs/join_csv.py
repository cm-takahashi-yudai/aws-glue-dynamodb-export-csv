import boto3
import pandas as pd
import io

BUCKET_NAME = 'aws-glue-dynamodb-export-csv-dev-result'

s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(BUCKET_NAME)

objs = bucket.meta.client.list_objects(
    Bucket=bucket.name,
    Prefix=''
)

header = True

for content in objs.get('Contents'):
    key = content.get('Key')
    obj = bucket.Object(key)
    response = obj.get()
    body = response['Body'].read()

    if body:
        df = pd.read_csv(io.BytesIO(body))
        df.to_csv('/tmp/output.csv', mode='a', encoding='utf_8', header=header, index=False)
        header = False

bucket.upload_file('/tmp/output.csv', 'sample.csv')
