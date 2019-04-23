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
    create_dates = list()
    create_dates.append((datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'))
    create_dates.append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))

    sample_id = 1

    with table.batch_writer() as batch:
        for create_date in create_dates:
            for i in range(10000):
                batch.put_item(
                    Item={
                        'create_date': create_date,
                        'sample_id': sample_id,
                        'sample_col_a': 'sample_val_a_' + str(sample_id),
                        'sample_col_b': 'sample_val_b_' + str(sample_id),
                        'sample_col_c': 'sample_val_c_' + str(sample_id)
                    }
                )

                sample_id += 1


if __name__ == '__main__':
    main()
