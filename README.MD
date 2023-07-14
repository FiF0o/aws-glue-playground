# AWS Glue playground

This repo is a quick AWS Glue playground. eu-west-2

## Pre-requisites

- An AWS Account access to the Management console is required.
- S3 buckets for source and target need to be created
- A database needs to be created
- Set your aws credentials as env variables in a shell: `export TF_VAR_AWS_REGION=<region>`, etc... Please see env file, rename it to `.env`.
- IAM Role for AWS Glue Studio created with following policies and permissions:

`AWSGlueServiceRole`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "glue:*",
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:ListAllMyBuckets",
        "s3:GetBucketAcl",
        "ec2:DescribeVpcEndpoints",
        "ec2:DescribeRouteTables",
        "ec2:CreateNetworkInterface",
        "ec2:DeleteNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeSubnets",
        "ec2:DescribeVpcAttribute",
        "iam:ListRolePolicies",
        "iam:GetRole",
        "iam:GetRolePolicy",
        "cloudwatch:PutMetricData"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:CreateBucket"],
      "Resource": ["arn:aws:s3:::aws-glue-*"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": ["arn:aws:s3:::aws-glue-*/*", "arn:aws:s3:::*/*aws-glue-*/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::crawler-public*", "arn:aws:s3:::aws-glue-*"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": ["arn:aws:logs:*:*:/aws-glue/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["ec2:CreateTags", "ec2:DeleteTags"],
      "Condition": {
        "ForAllValues:StringEquals": {
          "aws:TagKeys": ["aws-glue-service-resource"]
        }
      },
      "Resource": [
        "arn:aws:ec2:*:*:network-interface/*",
        "arn:aws:ec2:*:*:security-group/*",
        "arn:aws:ec2:*:*:instance/*"
      ]
    }
  ]
}
```

`AWSGlueConsoleFullAccess`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "glue:*",
        "redshift:DescribeClusters",
        "redshift:DescribeClusterSubnetGroups",
        "iam:ListRoles",
        "iam:ListUsers",
        "iam:ListGroups",
        "iam:ListRolePolicies",
        "iam:GetRole",
        "iam:GetRolePolicy",
        "iam:ListAttachedRolePolicies",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeSubnets",
        "ec2:DescribeVpcs",
        "ec2:DescribeVpcEndpoints",
        "ec2:DescribeRouteTables",
        "ec2:DescribeVpcAttribute",
        "ec2:DescribeKeyPairs",
        "ec2:DescribeInstances",
        "ec2:DescribeImages",
        "rds:DescribeDBInstances",
        "rds:DescribeDBClusters",
        "rds:DescribeDBSubnetGroups",
        "s3:ListAllMyBuckets",
        "s3:ListBucket",
        "s3:GetBucketAcl",
        "s3:GetBucketLocation",
        "cloudformation:ListStacks",
        "cloudformation:DescribeStacks",
        "cloudformation:GetTemplateSummary",
        "dynamodb:ListTables",
        "kms:ListAliases",
        "kms:DescribeKey",
        "cloudwatch:GetMetricData",
        "cloudwatch:ListDashboards"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": [
        "arn:aws:s3:::aws-glue-*/*",
        "arn:aws:s3:::*/*aws-glue-*/*",
        "arn:aws:s3:::aws-glue-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["tag:GetResources"],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:CreateBucket"],
      "Resource": ["arn:aws:s3:::aws-glue-*"]
    },
    {
      "Effect": "Allow",
      "Action": ["logs:GetLogEvents"],
      "Resource": ["arn:aws:logs:*:*:/aws-glue/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["cloudformation:CreateStack", "cloudformation:DeleteStack"],
      "Resource": "arn:aws:cloudformation:*:*:stack/aws-glue*/*"
    },
    {
      "Effect": "Allow",
      "Action": ["ec2:RunInstances"],
      "Resource": [
        "arn:aws:ec2:*:*:instance/*",
        "arn:aws:ec2:*:*:key-pair/*",
        "arn:aws:ec2:*:*:image/*",
        "arn:aws:ec2:*:*:security-group/*",
        "arn:aws:ec2:*:*:network-interface/*",
        "arn:aws:ec2:*:*:subnet/*",
        "arn:aws:ec2:*:*:volume/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["ec2:TerminateInstances", "ec2:CreateTags", "ec2:DeleteTags"],
      "Resource": ["arn:aws:ec2:*:*:instance/*"],
      "Condition": {
        "StringLike": {
          "ec2:ResourceTag/aws:cloudformation:stack-id": "arn:aws:cloudformation:*:*:stack/aws-glue-*/*"
        },
        "StringEquals": {
          "ec2:ResourceTag/aws:cloudformation:logical-id": "ZeppelinInstance"
        }
      }
    },
    {
      "Action": ["iam:PassRole"],
      "Effect": "Allow",
      "Resource": "arn:aws:iam::*:role/AWSGlueServiceRole*",
      "Condition": {
        "StringLike": {
          "iam:PassedToService": ["glue.amazonaws.com"]
        }
      }
    },
    {
      "Action": ["iam:PassRole"],
      "Effect": "Allow",
      "Resource": "arn:aws:iam::*:role/AWSGlueServiceNotebookRole*",
      "Condition": {
        "StringLike": {
          "iam:PassedToService": ["ec2.amazonaws.com"]
        }
      }
    },
    {
      "Action": ["iam:PassRole"],
      "Effect": "Allow",
      "Resource": ["arn:aws:iam::*:role/service-role/AWSGlueServiceRole*"],
      "Condition": {
        "StringLike": {
          "iam:PassedToService": ["glue.amazonaws.com"]
        }
      }
    }
  ]
}
```

`AwsGlueDataBrewFullAccessPolicy`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "databrew:CreateDataset",
        "databrew:DescribeDataset",
        "databrew:ListDatasets",
        "databrew:UpdateDataset",
        "databrew:DeleteDataset",
        "databrew:CreateProject",
        "databrew:DescribeProject",
        "databrew:ListProjects",
        "databrew:StartProjectSession",
        "databrew:SendProjectSessionAction",
        "databrew:UpdateProject",
        "databrew:DeleteProject",
        "databrew:CreateRecipe",
        "databrew:DescribeRecipe",
        "databrew:ListRecipes",
        "databrew:ListRecipeVersions",
        "databrew:PublishRecipe",
        "databrew:UpdateRecipe",
        "databrew:BatchDeleteRecipeVersion",
        "databrew:DeleteRecipeVersion",
        "databrew:CreateRecipeJob",
        "databrew:CreateProfileJob",
        "databrew:DescribeJob",
        "databrew:DescribeJobRun",
        "databrew:ListJobRuns",
        "databrew:ListJobs",
        "databrew:StartJobRun",
        "databrew:StopJobRun",
        "databrew:UpdateProfileJob",
        "databrew:UpdateRecipeJob",
        "databrew:DeleteJob",
        "databrew:CreateSchedule",
        "databrew:DescribeSchedule",
        "databrew:ListSchedules",
        "databrew:UpdateSchedule",
        "databrew:DeleteSchedule",
        "databrew:CreateRuleset",
        "databrew:DeleteRuleset",
        "databrew:DescribeRuleset",
        "databrew:ListRulesets",
        "databrew:UpdateRuleset",
        "databrew:ListTagsForResource",
        "databrew:TagResource",
        "databrew:UntagResource"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "appflow:DescribeFlow",
        "appflow:DescribeFlowExecutionRecords",
        "appflow:ListFlows",
        "glue:GetConnection",
        "glue:GetConnections",
        "glue:GetDatabases",
        "glue:GetPartitions",
        "glue:GetTable",
        "glue:GetTables",
        "glue:GetDataCatalogEncryptionSettings",
        "dataexchange:ListDataSets",
        "dataexchange:ListDataSetRevisions",
        "dataexchange:ListRevisionAssets",
        "dataexchange:CreateJob",
        "dataexchange:StartJob",
        "dataexchange:GetJob",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeVpcs",
        "ec2:DescribeSubnets",
        "kms:DescribeKey",
        "kms:ListKeys",
        "kms:ListAliases",
        "redshift:DescribeClusters",
        "redshift:DescribeClusterSubnetGroups",
        "redshift-data:DescribeStatement",
        "redshift-data:ListDatabases",
        "redshift-data:ListSchemas",
        "redshift-data:ListTables",
        "s3:ListAllMyBuckets",
        "s3:GetBucketCORS",
        "s3:GetBucketLocation",
        "s3:GetEncryptionConfiguration",
        "s3:GetLifecycleConfiguration",
        "secretsmanager:ListSecrets",
        "secretsmanager:DescribeSecret",
        "sts:GetCallerIdentity",
        "cloudtrail:LookupEvents",
        "iam:ListRoles",
        "iam:GetRole"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": ["glue:CreateConnection"],
      "Resource": [
        "arn:aws:glue:*:*:catalog",
        "arn:aws:glue:*:*:connection/AwsGlueDataBrew-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["glue:GetDatabases"],
      "Resource": ["arn:aws:glue:*:*:catalog", "arn:aws:glue:*:*:database/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["glue:CreateTable"],
      "Resource": [
        "arn:aws:glue:*:*:catalog",
        "arn:aws:glue:*:*:database/*",
        "arn:aws:glue:*:*:table/*/awsgluedatabrew*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket", "s3:GetObject"],
      "Resource": ["arn:aws:s3:::databrew-public-datasets-*"]
    },
    {
      "Effect": "Allow",
      "Action": ["kms:GenerateDataKey"],
      "Resource": ["*"],
      "Condition": {
        "StringLike": {
          "kms:ViaService": "s3.*.amazonaws.com"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:CreateSecret"],
      "Resource": "arn:aws:secretsmanager:*:*:secret:AwsGlueDataBrew-*"
    },
    {
      "Effect": "Allow",
      "Action": ["kms:GenerateRandom"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": "arn:aws:secretsmanager:*:*:secret:databrew!default-*",
      "Condition": {
        "ForAnyValue:StringEquals": {
          "aws:CalledVia": ["databrew.amazonaws.com"]
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:CreateSecret"],
      "Resource": "arn:aws:secretsmanager:*:*:secret:databrew!default-*",
      "Condition": {
        "StringLike": {
          "secretsmanager:Name": "databrew!default"
        },
        "ForAnyValue:StringEquals": {
          "aws:CalledVia": ["databrew.amazonaws.com"]
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": ["iam:PassRole"],
      "Resource": "arn:aws:iam::*:role/*",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": ["databrew.amazonaws.com"]
        }
      }
    }
  ]
}
```

`AWSGlueSchemaRegistryFullAccess`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSGlueSchemaRegistryFullAccess",
      "Effect": "Allow",
      "Action": [
        "glue:CreateRegistry",
        "glue:UpdateRegistry",
        "glue:DeleteRegistry",
        "glue:GetRegistry",
        "glue:ListRegistries",
        "glue:CreateSchema",
        "glue:UpdateSchema",
        "glue:DeleteSchema",
        "glue:GetSchema",
        "glue:ListSchemas",
        "glue:RegisterSchemaVersion",
        "glue:DeleteSchemaVersions",
        "glue:GetSchemaByDefinition",
        "glue:GetSchemaVersion",
        "glue:GetSchemaVersionsDiff",
        "glue:ListSchemaVersions",
        "glue:CheckSchemaVersionValidity",
        "glue:PutSchemaVersionMetadata",
        "glue:RemoveSchemaVersionMetadata",
        "glue:QuerySchemaVersionMetadata"
      ],
      "Resource": ["*"]
    },
    {
      "Sid": "AWSGlueSchemaRegistryTagsFullAccess",
      "Effect": "Allow",
      "Action": ["glue:GetTags", "glue:TagResource", "glue:UnTagResource"],
      "Resource": ["arn:aws:glue:*:*:schema/*", "arn:aws:glue:*:*:registry/*"]
    }
  ]
}
```

`AWSGlueDataBrewServiceRole`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetDatabases",
        "glue:GetPartitions",
        "glue:GetTable",
        "glue:GetTables",
        "glue:GetConnection"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": ["glue:BatchGetCustomEntityTypes"],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket", "s3:GetObject"],
      "Resource": ["arn:aws:s3:::databrew-public-datasets-*"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeVpcEndpoints",
        "ec2:DescribeRouteTables",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeSubnets",
        "ec2:DescribeVpcAttribute",
        "ec2:CreateNetworkInterface"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": "ec2:DeleteNetworkInterface",
      "Condition": {
        "StringLike": {
          "aws:ResourceTag/aws-glue-service-resource": "*"
        }
      },
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": ["ec2:CreateTags", "ec2:DeleteTags"],
      "Condition": {
        "ForAllValues:StringEquals": {
          "aws:TagKeys": ["aws-glue-service-resource"]
        }
      },
      "Resource": [
        "arn:aws:ec2:*:*:network-interface/*",
        "arn:aws:ec2:*:*:security-group/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": ["arn:aws:logs:*:*:log-group:/aws-glue-databrew/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["lakeformation:GetDataAccess"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": "arn:aws:secretsmanager:*:*:secret:databrew!default-*"
    }
  ]
}
```

## Architecture

```sh
# test database is created
s3/
__aws-glue-playground/
____inputs/
______customers/
________customer.csv
____outputs/
______first_table/
________<run-job-transform-output>

```

## Running the project

- Create crawlers and run crawlers for every tables to generate Data Catalogue metadata to be used in ETL
- Create a Data Catalogue database, currently accepts `.csv` extentions.
- Create Data Catalogue tables - `input_customer_csv`.
- Create your ETl Jobs scripts against the Data Catalogues
- Run the ETL Jobs
- Monitor ETL Job
- Query your data, in your s3 `output/` bucket with "Query with S3 Select" (json option). e.g. `SELECT * FROM s3object s LIMIT 5`
