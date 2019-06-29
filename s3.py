import boto3

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
        object_acl = s3.get_object_acl(Bucket=s3_bucket_src, Key=object_key)
        print(obj['Key'])

        s3.copy_object(
            Bucket=s3_bucket_dest,
            CopySource={
                'Bucket': s3_bucket_src,
                'Key': object_key
            },
            Key=object_key
        )
        data = {
            'AccessControlPolicy': {
                'Owner': object_acl['Owner'],
                'Grants': object_acl['Grants']
            }
        }
        print(data)
        s3.put_object_acl(**data, Bucket=s3_bucket_dest, Key=object_key)
