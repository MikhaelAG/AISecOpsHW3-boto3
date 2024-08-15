import boto3

def create_ec2_instance(ami_id, instance_type, key_name, user_data, instance_name):
    ec2 = boto3.resource('ec2')

    # Launch the instance
    instance = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        UserData=user_data,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    }
                ]
            }
        ]
    )[0]

    # Wait for the instance to be running
    instance.wait_until_running()
    
    # Reload the instance attributes
    instance.reload()

    return instance

def main():
    ami_id = 'ami-0ae8f15ae66fe8cda'
    instance_type = 't2.micro'
    key_name = 'dack_key'
    user_data = '''#!/bin/bash
echo "hello world" > /home/ec2-user/hello_world.txt
'''

    # Create the first instance
    instance1 = create_ec2_instance(ami_id, instance_type, key_name, user_data, 'My Linux Instance 1')
    print(f'Instance 1 created with ID: {instance1.id}')

    # Create the second instance
    instance2 = create_ec2_instance(ami_id, instance_type, key_name, user_data, 'My Linux Instance 2')
    print(f'Instance 2 created with ID: {instance2.id}')

if __name__ == '__main__':
    main()
