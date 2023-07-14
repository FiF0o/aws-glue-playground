
# Playground code, not to be used in prod. Only quick POC

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.27.0"
    }
  }
}

provider "aws" {
  region     = var.AWS_REGION
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

locals {
  glue-arn = "arn:aws:iam::${var.aws_account_id}:role/aws-glue-gluestudio-role"
}

############# Variables ############# 
# will be default by default when setting your AWS acc, replace accordingly with access key/id if necessary
variable "aws_access_key" {
  type = string
}

variable "AWS_REGION" {
  type = string
}

variable "aws_account_id" {
  type = string
}

variable "aws_secret_key" {
  type = string
}

variable "job-language" {
  default = "python"
}

variable "bucket-name" {
  default = "etl-script-deploy"
}

variable "job-name" {
  default = "etl-job-glue-job-tf"
}

variable "file-name" {
  default = "etl-job-glue.py"
}

variable "s3-data" {
  default = "etl-glue-playground-jon"
}

variable "customer-table" {
  default = "customer.csv"
}



################## Resources ##################

// Bucket for script
resource "aws_s3_bucket" "glue-bucket" {
  bucket = var.bucket-name
}

resource "aws_s3_bucket" "s3-data-input" {
  bucket = var.s3-data
}

resource "aws_s3_bucket_object" "upload-table" {
  bucket = aws_s3_bucket.s3-data-input.id
  key    = "/input/customers/${var.customer-table}"
  source = "../tables/${var.customer-table}"
}

resource "aws_s3_bucket_object" "upload-glue-script" {
  bucket = aws_s3_bucket.glue-bucket.id
  key    = "scripts/${var.file-name}"
  source = "../scripts/${var.file-name}"
}

// aws glue Data Catalogue table

resource "aws_glue_catalog_database" "database" {
  name = "test-etl"
  create_table_default_permission {
    permissions = ["SELECT"]

    principal {
      data_lake_principal_identifier = "IAM_ALLOWED_PRINCIPALS"
    }
  }
}

resource "aws_glue_catalog_table" "aws_glue_catalog_table" {
  name          = "customers"
  database_name = aws_glue_catalog_database.database.name
  parameters = {
    "classification" = "csv"
  }
  storage_descriptor {
    location = "s3://etl-glue-playground-jon/input/customers/customer.csv"
  }
}

// crawlers
resource "aws_glue_crawler" "crawler_customer" {
  database_name = aws_glue_catalog_database.database.name
  name          = "crawler-etl"
  role          = local.glue-arn

  // Update
  s3_target {
    path = "s3://etl-glue-playground-jon/input/customers/customer.csv"
  }
}
// data-catalogue

// glue job
resource "aws_glue_job" "glue-job" {
  name        = var.job-name
  role_arn    = local.glue-arn
  description = "Script to do one to mapping from source to target"
  max_retries = "0"
  timeout     = 2880
  command {
    script_location = "s3://${var.bucket-name}/scripts/${var.file-name}"
    python_version  = "3"
  }
  execution_property {
    max_concurrent_runs = 2
  }
}
