import boto3
import json
import uuid
import os

from datetime import datetime, timedelta

PROJECT_NAME = os.environ['PROJECT_NAME']
STAGE_NAME = os.environ['STAGE_NAME']
TABLE_NAME = PROJECT_NAME + '-' + STAGE_NAME + '-target'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def main() -> None:
    create_date = datetime.now() - timedelta(days=1)

    with table.batch_writer() as batch:
        for i in range(1000):
            batch.put_item(
                Item={
                    'create_date': create_date.strftime('%Y-%m-%d'),
                    'sample_id': str(uuid.uuid4()),
                    'sample_col_a': 'sample_val_a_' + str(i),
                    'sample_col_b': 'sample_val_b_' + str(i),
                    'sample_col_c': 'sample_val_c_' + str(i)
                }
            )


if __name__ == '__main__':
    main()
