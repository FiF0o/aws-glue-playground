# Merge 2 tables
# https://docs.aws.amazon.com/glue/latest/webapi/API_Types.html

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame


def sparkUnion(glueContext, unionType, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(
        "(select * from source1) UNION " + unionType + " (select * from source2)"
    )
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node source s3 2
sources32_node1689177514396 = glueContext.create_dynamic_frame.from_catalog(
    database="test",
    table_name="input_customer_csv",
    transformation_ctx="sources32_node1689177514396",
)

# Script generated for node source s3 1
sources31_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="test",
    table_name="input_customer_csv",
    transformation_ctx="sources31_node1",
)

# Script generated for node Amazon S3
AmazonS3_node1689184749396 = glueContext.create_dynamic_frame.from_catalog(
    database="test",
    table_name="input_customer_csv",
    transformation_ctx="AmazonS3_node1689184749396",
)

# Script generated for node Amazon S3
AmazonS3_node1689184796008 = glueContext.create_dynamic_frame.from_catalog(
    database="test",
    table_name="input_customer_csv",
    transformation_ctx="AmazonS3_node1689184796008",
)

# Script generated for node JoinTable1AndTable2
JoinTable1AndTable2_node1689181135875 = sparkUnion(
    glueContext,
    unionType="ALL",
    mapping={"source1": sources31_node1, "source2": sources32_node1689177514396},
    transformation_ctx="JoinTable1AndTable2_node1689181135875",
)

# Script generated for node Union
Union_node1689183458650 = sparkUnion(
    glueContext,
    unionType="ALL",
    mapping={
        "source1": AmazonS3_node1689184796008,
        "source2": AmazonS3_node1689184749396,
    },
    transformation_ctx="Union_node1689183458650",
)

# Script generated for node Amazon S3
AmazonS3_node1689180791812 = glueContext.write_dynamic_frame.from_options(
    frame=JoinTable1AndTable2_node1689181135875,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://aws-glue-playground-jon/output/second_table/",
        "partitionKeys": [],
    },
    transformation_ctx="AmazonS3_node1689180791812",
)

# Script generated for node Amazon S3
AmazonS3_node1689183713448 = glueContext.write_dynamic_frame.from_options(
    frame=Union_node1689183458650,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://aws-glue-playground-jon/output/second_table/",
        "partitionKeys": [],
    },
    transformation_ctx="AmazonS3_node1689183713448",
)

job.commit()
