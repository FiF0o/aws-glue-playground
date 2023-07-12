# Apply 1 to 1 mapping and rename some attributes
# https://docs.aws.amazon.com/glue/latest/webapi/API_Types.html

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node input s3
inputs3_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="test", table_name="input_customer_csv", transformation_ctx="inputs3_node1"
)

# Script generated for node ApplyMappingDropAndRename
ApplyMappingDropAndRename_node2 = ApplyMapping.apply(
    frame=inputs3_node1,
    mappings=[
        ("customerid", "long", "customerid_target", "long"),
        ("namestyle", "boolean", "namestyle_target", "boolean"),
        ("title", "string", "title_target", "string"),
        ("firstname", "string", "firstname_target", "string"),
        ("middlename", "string", "middlename_target", "string"),
    ],
    transformation_ctx="ApplyMappingDropAndRename_node2",
)

# Script generated for node output s3
outputs3_node3 = glueContext.write_dynamic_frame.from_options(
    frame=ApplyMappingDropAndRename_node2,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://aws-glue-playground-jon/output/first_table/",
        "partitionKeys": [],
    },
    transformation_ctx="outputs3_node3",
)

job.commit()
