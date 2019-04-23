import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initalize
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# DataSource
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="aws-glue-dynamodb-export-csv-dev-glue-database",
    table_name="aws-glue-dynamodb-export-csv-dev-glue-table",
    transformation_ctx="datasource",
    push_down_predicate="create_date='2019-04-22'"
)

# Transform
applymapping = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("create_date", "string", "create_date", "string"),
        ("sample_id", "int", "sample_id", "int"),
        ("sample_col_a", "string", "sample_col_a", "string"),
        ("sample_col_b", "string", "sample_col_b", "string"),
        ("sample_col_c", "string", "sample_col_c", "string")
    ],
    transformation_ctx="applymapping"
)

# DataSink
datasink = glueContext.write_dynamic_frame.from_options(
    frame=applymapping,
    connection_type="s3",
    connection_options={
        "path": "s3://aws-glue-dynamodb-export-csv-dev-result"
    },
    format="csv",
    transformation_ctx="datasink"
)

# Terminate
job.commit()
