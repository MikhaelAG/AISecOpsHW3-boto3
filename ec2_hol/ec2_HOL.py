import boto3

# Create ec2 resource & instance name
ec2 = boto3.resource('ec2')
instance_name = 'dct-ec2-hol'

# Store the instance id
instance_id = None # null


# Verify if the EC2 exists
# only work in an ec2 that is NOT terminated
instances = ec2.instances.all()
instance_exists = False

for instance in instances:
    if instance.tags:    
        for tag in instance.tags:
            if tag['Key'] == 'Name' and tag['Value'] == instance_name:
                instance_exists = True
                instance_id = instance.id
                print(f"An instance named '{instance_name}' with id '{instance_id}' already exists.")
                break
    if instance_exists:
        break


if not instance_exists:
    # Launch new EC2 if it does NOT exist
    new_instance = ec2.create_instances(
            ImageId='ami-0ae8f15ae66fe8cda',  # replace with a valid AMI ID
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='ec2-hol-080920241124',  # replace with your key pair name
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ]
        )
    
    instance_id = new_instance[0].id
    print(f"Instance named '{instance_name}' with id '{instance_id}' created.")
    
# Stop an instance
# ec2.Instance(instance_id).stop()
# print(f"Instance '{instance_name}'-'{instance_id}' stopped.")

# Start an instance
# ec2.Instance(instance_id).start()
# print(f"Instance '{instance_name}'-'{instance_id}' started.")

# Terminate an instance
# ec2.Instance(instance_id).terminate()
# print(f"Instance '{instance_name}'-'{instance_id}' is terminated.")