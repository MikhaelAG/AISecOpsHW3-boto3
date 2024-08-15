# Create aurora serverless 
import boto3
import time

# Load boto3 client for RDS
rds = boto3.client('rds')

# Create User-defined variables for db
username = 'dctuser1'
password = '3ssldf4l'
# Grab subnet group from RDS
db_subnet_group = 'vpc-hol'
db_cluster_id = 'rds-hol-cluster-1'

# Create the DB Cluster

# try:
#     response = rds.describe_db_clusters(DBClusterIdentifier = db_cluster_id)
#     print(f"The DB cluster used '{db_cluster_id}' already exists.\n\nSkipping creation.")
# except rds.exceptions.DBClusterNotFoundFault:
#     response = rds.create_db_cluster(
#         Engine='aurora-mysql',
#         EngineVersion='5.7.mysql_aurora.2.08.3',
#         DBClusterIdentifier=db_cluster_id, 
#         MasterUsername=username,  
#         MasterUserPassword=password,  
#         DatabaseName='rds_hol_db',
#         DBSubnetGroupName=db_subnet_group,  
#         EngineMode='serverless',
#         EnableHttpEndpoint=True,
#         ScalingConfiguration={
#             'MinCapacity': 1, # Minimum ACU
#             'MaxCapacity': 8, # Maximum ACU
#             'AutoPause': True,
#             'SecondsUntilAutoPause': 3600  # Pause after 5 minutes of inactivity
#         }
#     )
    
#     print(f"The DB cluster named '{db_cluster_id}' has been created.")
    
#     # Wait for teh DB cluster to beomcm available
#     while True:
#         response = rds.describe_db_clusters(DBClusterIdentifier = db_cluster_id)
#         status = response['DBClusters'][0]['Status']
#         print(f"The status of the cluster is '{status}'")
#         if status == 'available':
#             break
        
#         print("Waiting for the DB Cluster to become available ...")
#         time.sleep(40)
        
# Modify the DB cluster. Update the scaling config for the cluster
# response = rds.modify_db_cluster(
#         DBClusterIdentifier=db_cluster_id, 
    
#         ScalingConfiguration={
#             'MinCapacity': 1, # Minimum ACU
#             'MaxCapacity': 16, # Maximum ACU
#             'AutoPause': True,
#             'SecondsUntilAutoPause': 600  # Pause after 5 minutes of inactivity
#         }
#     )
# print(f"Updated the scaling configuration for DB cluster '{db_cluster_id}'")


# # Delete the DB cluster
response = rds.delete_db_cluster(
        DBClusterIdentifier=db_cluster_id, 
        SkipFinalSnapshot = True
    )
print(f"The '{db_cluster_id}' is being deleted.")