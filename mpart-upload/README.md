# Multipart upload

No tf scripts are available for that module.
Multipart upload is performed on existing s3 bucket with aws user/cli

## Pre-requisites

- As a prequiste set the env file. Default Region is eu-west-2.
- Bucket must be created
- content must be bigger than 5MiB, add it to the repo
- set your .env file

## Does not include

Resource permissions as script performed with cli:

- S3 Bucket (ListMultiPartUpload, etc..)
- assume Role (CreateMultiPartUpload, UploadPart, CompleteMultipartUpload)
- KMS

## Scripts

### doc

https://docs.aws.amazon.com/cli/latest/reference/s3api/create-multipart-upload.html
https://docs.aws.amazon.com/cli/latest/reference/s3api/upload-part.html
https://docs.aws.amazon.com/cli/latest/reference/s3api/complete-multipart-upload.html

Limitations: https://docs.aws.amazon.com/en_us/AmazonS3/latest/userguide/qfacts.html

### steps

0. create tarball
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
aws s3api create-multipart-upload --bucket ${aws_s3_bucket} --key ${key}

```

3. Returns UploadId to be used for upload

```sh
# returns UploadId to be used for upload and completing operations
{
    "ServerSideEncryption": "AES256",
    "Bucket": "<bucket-name>",
    "Key": "<yourKey>",
    "UploadId": "<uploadIdToBeUsed>"
}
```

4. upload chunks to bucket

```sh
# upload chunks (2 parts)
aws s3api upload-part --bucket ${aws_s3_bucket} --key ${key} --part-number 1 --body mtpu_000 --upload-id ${uploadid}

aws s3api upload-part --bucket ${aws_s3_bucket} --key ${key} --part-number 2 --body mtpu_001 --upload-id ${uploadid}

```

5. will return etags to be used in `parts.json` file

```sh
# returns parts to used in the part.json for AWS to reassemble file when completing mpart upload
# part 1
{
    "ServerSideEncryption": "AES256",
    "ETag": "\"4436236917a37a61cc63ef2d96f70916\""
}

# part 2
{
    "ServerSideEncryption": "AES256",
    "ETag": "\"31062992c59103d1ed29960fa06d07f1\""
}
```

6. Complete multipart upload

```sh
# Issue mpart upload completion passing file meta for aws to reassemble chunks into one file
aws s3api complete-multipart-upload --multipart-upload file://parts.json --bucket ${aws_s3_bucket} --key ${key} --upload-id ${uploadid}
```

```sh
# Sample ok response

{
    "ServerSideEncryption": "AES256",
    "Location": "<path to s3 bucket>",
    "Bucket": "<your bucket>",
    "Key": "mixkit-going-down-a-curved-highway-through-a-mountain-range-41576-4k.mp4",
    "ETag": "\"efbecc7ce8bedda1338b7b69ca9a4b8c-2\""
}

```

![ok response from multipart upload](./ok-response.png)
