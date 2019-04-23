import boto3
import pandas as pd
import sys

from awsglue.utils import getResolvedOptions
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta

args = getResolvedOptions(sys.argv, ['TABLE_NAME', 'BUCKET_NAME'])

TABLE_NAME = args['TABLE_NAME']
BUCKET_NAME = args['BUCKET_NAME']

TARGET_DATETIME = datetime.now() - timedelta(days=1)
TARGET_DATE = TARGET_DATETIME.strftime('%Y%m%d')
TARGET_DATE_H = TARGET_DATETIME.strftime('%Y-%m-%d')

TEMP_FILE_PATH = '/tmp/output.csv'
OUTPUT_PATH = TARGET_DATE + '.csv'

dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')


def get_items_from_dynamodb_table(table_name, key_condition_expression):
    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=key_condition_expression
    )
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        data.extend(response['Items'])

    return data


def main():
    items = get_items_from_dynamodb_table(
        table_name=TABLE_NAME,
        key_condition_expression=Key('create_date').eq(TARGET_DATE_H)
    )

    df = pd.DataFrame(items)
    df.to_csv(TEMP_FILE_PATH, encoding='utf_8', index=False)

    bucket = s3.Bucket(BUCKET_NAME)
    bucket.upload_file(TEMP_FILE_PATH, OUTPUT_PATH)


if __name__ == '__main__':
    main()
