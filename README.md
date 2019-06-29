# aws-s3-bucket-copy
Simple python script which let you copy objects from one bucket to another while preserving ACLs (if you have multiple objects in the bucket with mixed ACL settings then this script is for you).

# Prerequisites
* Python 3.6+
* boto3 installed
* AWS User which has a FullS3Access policy (and you've got the credentials for this user)
* S3 buckets created (both source and destination bucket)

# Usage
If you already have AWS profile configured on your local system, simply provide the profile name in the following line:
`aws = boto3.Session(profile_name='')`

or you can pass Access Key/Secret Access Key with region directly to the script:
```
aws = boto3.Session(
   aws_access_key_id='',
   aws_secret_access_key='',
   region_name=''
)
```

Next fill in the source and destination bucket (both should already exist in the S3):
```
s3_bucket_src = ""
s3_bucket_dest = ""
```

After that just simply run the script: `python3 s3.py`
