import boto3
import time


#Create the VPC

# Create the ec2 client
ec2 = boto3.client('ec2')

# Add vpc name
vpc_name = 'vpc_hol'

# Confirm VPC is created
response = ec2.describe_vpcs(
    # Filter only the vpc with spefic name
    Filters=[{'Name': 'tag:Name', 'Values': [vpc_name]}]
    )

vpcs = response.get('Vpcs', [])

if vpcs:
    vpc_id = vpcs[0]['VpcId']
    print(f"VPC '{vpc_name}' with ID '{vpc_id}' already exists.")

# Pass cidr block in vpc method
vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16') ## rfc 1918 net

# Refer to the created vpc id
vpc_id = vpc_response['Vpc']['VpcId']

# pause
time.sleep(5)

# Add tags to vpc
ec2.create_tags(Resources = [vpc_id], Tags = [{'Key': 'Name', 'Value': vpc_name}])

print(f"VPC '{vpc_name}' with ID '{vpc_id}' has been created.")

# Add IGW - Internet Gateway
 
# Name igw
ig_name = 'ig-vpc-hol'

# Confirm IGW creation
response = ec2.describe_internet_gateways(
    # Filter only the vpc with spefic name
    Filters=[{'Name': 'tag:Name', 'Values': [ig_name]}]
    )

internet_gateways = response.get('InternetGateways', [])

if internet_gateways:
    ig_id = internet_gateways[0]['InternetGatewaysId']
    print(f"Internet Gateway '{ig_name}' with ID '{ig_id}' already exists.")
else:
    # Create IGW when it does NOT exist
    ig_response = ec2.create_internet_gateway()
    ig_id = ig_response['InternetGateway']['InternetGatewayId']
    
    #Create IGW tags
    ec2.create_tags(Resources=[ig_id], Tags=[{'Key': 'Name', 'Value': ig_name}])
    
    # Attach IGW to VPC
    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=ig_id)
    print(f"Internet Gateway '{ig_name}' with ID '{ig_id}' has been created.")


## Adding Route Table and Vpc Subnets


# Create a RT with public route
rt_response = ec2.create_route_table(VpcId=vpc_id)
# Associate RT with RT_ID, Destination to the Internet, and IGW ID
rt_id = rt_response['RouteTable']['RouteTableId']
route = ec2.create_route(
    RouteTableId = rt_id, 
    DestinationCidrBlock = '0.0.0.0/0',
    GatewayId = ig_id
    )
print(f"Route Table with ID '{rt_id}' has been created.")

# Create 3 public subnets in us-east region in Zones a, b, c
subnet_1 = ec2.create_subnet(VpcId=vpc_id, CidrBlock = '10.0.1.0/24', AvailabilityZone = 'us-east-1a')
subnet_2 = ec2.create_subnet(VpcId=vpc_id, CidrBlock = '10.0.2.0/24', AvailabilityZone = 'us-east-1b')
subnet_3 = ec2.create_subnet(VpcId=vpc_id, CidrBlock = '10.0.3.0/24', AvailabilityZone = 'us-east-1c')

print(f"subnet_1 ID = '{subnet_1['Subnet']['SubnetId']}',\nsubnet_2 ID = '{subnet_2['Subnet']['SubnetId']}',\nsubnet_3 ID = '{subnet_3['Subnet']['SubnetId']}'")

