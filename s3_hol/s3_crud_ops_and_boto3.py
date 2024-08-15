import boto3


# Create the bucket resource from boto3
s3 = boto3.resource('s3')
bucket_name = 'dct-crud-15631215145'

# Verify bucket exists
# Create bucket if it does not exist
all_my_buckets = [bucket.name for bucket in s3.buckets.all()]

# Case 1: Bucket does not exist
if bucket_name not in all_my_buckets:
    print(f"'{bucket_name}' Bucket Does Not Exist.\n\nCreating now . . .")
    
    # creating bucket
    s3.create_bucket(Bucket = bucket_name)
    print(f"'{bucket_name}' Bucket has been created.")
else:
# Case 2: Bucket exists
    print(f"'{bucket_name}' Bucket already exists.\n\nNo need to create a new one.")
    
# Create objects 'file_1' and 'file_2'
file_1 = 'file_1.txt'
file_2 = 'file_2.txt'

# Upload 'file_1' to the new bucket
s3.Bucket(bucket_name).upload_file(Filename = file_1, Key = file_1)

# Read and print file (object) from the bucket
obj = s3.Object(bucket_name, file_1)
body = obj.get()['Body'].read()
print(body)

# Update 'file_1' in the bucket witih new content from 'file_2'
s3.Object(bucket_name, file_1).put(Body = open(file_2, 'rb'))
obj = s3.Object(bucket_name, file_1)
body = obj.get()['Body'].read()
print(body)


# Delete objects from bucket
s3.Object(bucket_name, file_1).delete()

# Delete bucket from s3
bucket = s3.Bucket(bucket_name)
bucket.delete()