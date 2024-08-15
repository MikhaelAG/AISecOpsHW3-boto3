import boto3

# List buckets by creating S3 resource

s3 = boto3.resource('s3')

# get all buckets from the resource
for bucket in s3.buckets.all():

# prints out all available buckets
    print(bucket.name)
