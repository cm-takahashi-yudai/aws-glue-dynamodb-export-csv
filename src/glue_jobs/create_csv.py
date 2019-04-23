import sys
from awsglue.transforms import ApplyMapping
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
# @type: DataSource
# @args: [database = "aws-glue-dynamodb-export-csv-dev-glue-database", table_name = "aws-glue-dynamodb-export-csv-dev-glue-table", transformation_ctx = "datasource0"]
# @return: datasource0
# @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database="aws-glue-dynamodb-export-csv-dev-glue-database", table_name="aws-glue-dynamodb-export-csv-dev-glue-table", transformation_ctx="datasource0")
# @type: ApplyMapping
# @args: [mapping = [("sample_col_1", "string", "sample_col_1", "string"), ("sample_col_2", "string", "sample_col_2", "string"), ("sample_col_3", "long", "sample_col_3", "long"), ("sample_id", "string", "sample_id", "string")], transformation_ctx = "applymapping1"]
# @return: applymapping1
# @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame=datasource0, mappings=[("sample_col_1", "string", "sample_col_1", "string"), ("sample_col_2", "string", "sample_col_2", "string"), ("sample_col_3", "long", "sample_col_3", "long"), ("sample_id", "string", "sample_id", "string")], transformation_ctx="applymapping1")
# @type: DataSink
# @args: [connection_type = "s3", connection_options = {"path": "s3://aws-glue-dynamodb-export-csv-dev-result"}, format = "csv", transformation_ctx = "datasink2"]
# @return: datasink2
# @inputs: [frame = applymapping1]
datasink2 = glueContext.write_dynamic_frame.from_options(frame=applymapping1, connection_type="s3", connection_options={"path": "s3://aws-glue-dynamodb-export-csv-dev-result"}, format="csv", transformation_ctx="datasink2")
job.commit()
