# Multipart upload

No tf scripts are available for that module.
Multipart upload is performed on existing s3 bucket with aws user/cli

## Pre-requisites

- As a prequiste set the env file. Default Region is eu-west-2.
- Bucket, KMS Key, User must be created
- content must be bigger than 5MiB, add it to the repo
- set your .env file
- Permissions/Policies:

### user policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "kmsAndMultipartUpload",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucketMultipartUploads",
        "kms:Decrypt",
        "s3:GetObjectVersionTagging",
        "s3:ListBucket",
        "s3:GetBucketVersioning",
        "s3:ListMultipartUploadParts",
        "s3:PutObject",
        "s3:GetObject",
        "s3:AbortMultipartUpload",
        "kms:Encrypt",
        "s3:GetObjectVersionAcl",
        "kms:GenerateDataKey",
        "s3:GetObjectTagging",
        "kms:DescribeKey",
        "s3:GetObjectVersion"
      ],
      "Resource": [
        "arn:aws:s3:::<aws_s3_bucket>",
        "arn:aws:s3:::<aws_s3_bucket>/*",
        "arn:aws:kms:eu-west-2:<account>:key/<kms_key>"
      ]
    }
  ]
}
```

### kms key

_(Shortened policy for brevity)_

```json
{
            "Sid": "Allow use of the key",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::<account>:user/<aws_user>"
                ]
            },
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:ReEncrypt*",
                "kms:GenerateDataKey*",
                "kms:DescribeKey"
            ],
            "Resource": "*"
        },
```

### Bucket

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BucketForUser",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account>:user/<aws_user>"
      },
      "Action": [
        "s3:PutObject",
        "s3:ListBucketMultipartUploads",
        "s3:ListMultipartUploadParts",
        "s3:GetObject",
        "s3:AbortMultipartUpload",
        "s3:GetBucketTagging",
        "s3:PutObjectTagging"
      ],
      "Resource": [
        "arn:aws:s3:::<aws_s3_bucket>",
        "arn:aws:s3:::<aws_s3_bucket>/*"
      ]
    }
  ]
}
```

## Does not include

script currently performed by a user and does not include assumeRole permission - cli is used as POC.

## Scripts

### doc

https://docs.aws.amazon.com/cli/latest/reference/s3api/create-multipart-upload.html
https://docs.aws.amazon.com/cli/latest/reference/s3api/upload-part.html
https://docs.aws.amazon.com/cli/latest/reference/s3api/complete-multipart-upload.html

Limitations: https://docs.aws.amazon.com/en_us/AmazonS3/latest/userguide/qfacts.html

### steps

0. create tarball - `tar -czvf archive-name.tar.gz tarball`
1. split file into chunks
2. request multipart upload id
3. upload chunks
4. Complete multipart upload

### commands

1. Get file info

```sh
# size
ls -lh ${key}

# number of rows
wc -l ${key}
```

2. Split file and request multipart upload

```sh
man split

# split by chunk into a separate folder to set multipart upload with prefix
split -d -a3 -n 2 ${key} mtpu_
# or split by size/line

# request multipart upload (UploadId) to bucket
aws s3api create-multipart-upload --bucket ${aws_s3_bucket} --key ${key} --server-side-encryption aws:kms --ssekms-key-id ${kms_key} --profile ${aws_user}

```

3. Returns UploadId to be used for upload

```sh
# returns UploadId to be used for upload and completing operations
{
    "ServerSideEncryption": "aws:kms",
    "SSEKMSKeyId": "<kmsKey>",
    "BucketKeyEnabled": true,
    "Bucket": "<bucketName>",
    "Key": "archive-name.tar.gz",
    "UploadId": "<uploadId>"
}
```

4. upload chunks to bucket

```sh
# upload chunks (2 parts)
aws s3api upload-part --bucket ${aws_s3_bucket} --key ${key} --part-number 1 --body mtpu_000 --upload-id ${uploadid} --profile ${aws_user}

aws s3api upload-part --bucket ${aws_s3_bucket} --key ${key} --part-number 2 --body mtpu_001 --upload-id ${uploadid} --profile ${aws_user}

```

5. will return etags to be used in `parts.json` file

```sh
# returns parts to used in the part.json for AWS to reassemble file when completing mpart upload
# part 1
{
    "ServerSideEncryption": "aws:kms",
    "ETag": "\"df64803ab538dd59fff3e032a0d23383\"",
    "SSEKMSKeyId": "<kmsKey>",
    "BucketKeyEnabled": true
}

# part 2
{
    "ServerSideEncryption": "aws:kms",
    "ETag": "\"df64803ab538dd59fff3e032a0d23383\"",
    "SSEKMSKeyId": "<kmsKey>",
    "BucketKeyEnabled": true
}
```

6. Complete multipart upload

```sh
# Issue mpart upload completion passing file meta for aws to reassemble chunks into one file
aws s3api complete-multipart-upload --multipart-upload file://parts.json --bucket ${aws_s3_bucket} --key ${key} --upload-id ${uploadid} --profile ${aws_user}
```

```sh
# Sample ok response

{
    "ServerSideEncryption": "aws:kms",
    "SSEKMSKeyId": "<kmsKey>",
    "BucketKeyEnabled": true,
    "Location": "<bucketLocation>",
    "Bucket": "<bucketName>",
    "Key": "archive-name.tar.gz",
    "ETag": "\"7078ecf608717cc12d8d3e6afe8babe6-2\""
}

```

![ok response from multipart upload](./ok-response.png)
