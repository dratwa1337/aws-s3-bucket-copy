#!/usr/bin/env python3

import boto3
import botocore
import json

# Use whatever you have configured
#aws = boto3.Session(profile_name='')
#aws = boto3.Session(
# aws_access_key_id='',
# aws_secret_access_key='',
# region_name=''
#
#)
s3 = aws.client('s3')

# Fill in source and destination bucket
s3_bucket_src = ""
s3_bucket_dest = ""

paginator = s3.get_paginator('list_objects')
pages = paginator.paginate(Bucket=s3_bucket_src)
for page in pages:
    for obj in page['Contents']:
        object_key = obj['Key']
        try:
             s3.get_object_acl(Bucket=s3_bucket_dest, Key=object_key)
        except botocore.exceptions.ClientError:
            s3.copy_object(
                Bucket=s3_bucket_dest,
                CopySource={
                    'Bucket': s3_bucket_src,
                    'Key': object_key
                },
                Key=object_key
            )

        try:
            object_acl = s3.get_object_acl(Bucket=s3_bucket_src, Key=object_key)
        except botocore.exceptions.ClientError:
            continue

        if len(object_acl['Grants']) == 1:
            continue

        target_acl = s3.get_object_acl(Bucket=s3_bucket_dest, Key=object_key)
        if len(object_acl['Grants']) <= len(target_acl['Grants']):
            continue

        target_acl['Grants'] += object_acl['Grants'][1:]

        data = {
            'AccessControlPolicy': {
                'Owner': target_acl['Owner'],
                'Grants': target_acl['Grants']
            }
        }
        print(object_key)
        s3.put_object_acl(**data, Bucket=s3_bucket_dest, Key=object_key)
