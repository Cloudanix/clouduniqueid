from clouduniqueid.clouds.aws import AWSUniqueId
from clouduniqueid.clouds.gcp import GCPUniqueId

aws_unique_id = AWSUniqueId()
region = 'us-east-1'
accountId = '12345'
partition = 'aws'

gcp_unique_id = GCPUniqueId()
projectId = 'proj-123'
location = 'us-east-a1'


# Unique id for aws S3 Bucket
unique_id = aws_unique_id.get_unique_id(
    data={'bucketName': 'b12345'}, service='s3', partition='aws', resourceType='bucket',
)
print(f"Unique id for aws S3 Bucket: {unique_id}")
# Output: Unique id for aws S3 Bucket: arn:aws:s3:::b12345


# Unique id for aws EC2 instance
unique_id = aws_unique_id.get_unique_id(
    service='ec2', region=region, accountId=accountId,
    partition=partition, resourceType='instance', data={'InstanceId': 'i-12345'},
)
print(f"Unique id for aws EC2 instance: {unique_id}")
# Output: Unique id for aws EC2 instance: arn:aws:ec2:us-east-1:12345:instance/i-12345


# Unique id for aws lambda function
unique_id = aws_unique_id.get_unique_id(
    data={'FunctionName': 'f12345'}, service='lambda', region=region,
    partition=partition, accountId=accountId, resourceType='function',
)
print(f"Unique id for aws lambda function: {unique_id}")
# Output: Unique id for aws lambda function: arn:aws:lambda:us-east-1:12345:function:f12345


# Unique id for aws lambda function alias
unique_id = aws_unique_id.get_unique_id(
    data={'FunctionName': 'f12345', 'name': 'a12345'}, service='lambda', region=region,
    partition=partition, accountId=accountId, resourceType='alias',
)
print(f"Unique id for aws lambda function alias: {unique_id}")
# Output: Unique id for aws lambda function alias: arn:aws:lambda:us-east-1:12345:function:f12345:a12345

# Unique id format for aws lambda function alias
unique_id_format = aws_unique_id.get_unique_id_format(
    service='lambda', resourceType='alias',
)
print(f"Unique id format for aws lambda function alias: {unique_id_format}")
# Output: Unique id format for aws lambda function alias:
# arn:{partition}:lambda:{region}:{accountId}:function:{FunctionName}:{Name}


# Unique id for aws iam service access
unique_id = aws_unique_id.get_unique_id(
    data={'PrincipalARN': 'p12345', 'ServiceName': 's12345'}, service='iam',
    resourceType='service-access',
)
print(f"Unique id for aws iam service access: {unique_id}")
# Output: Unique id for aws iam service access: 838a05f8ab5ad10f8c60e5b8cede85dc


# Unique id for gcp iam service account
unique_id = gcp_unique_id.get_unique_id(
    data={'email': 'saccount@demo.com'}, service='iam',
    resourceType='service-account',
)
print(f"Unique id for gcp iam service account: {unique_id}")
# Output: Unique id for gcp iam service account: saccount@demo.com


# Unique id for gcp iam role
unique_id = gcp_unique_id.get_unique_id(
    data={'name': 'roles/abcd.def'}, service='iam',
    resourceType='role', projectId=projectId,
)
print(f"Unique id for gcp iam role: {unique_id}")
# Output: Unique id for gcp iam role: projects/proj-123/roles/abcd.def


# Unique id format for gcp iam user
unique_id = gcp_unique_id.get_unique_id_format(
    service='iam', resourceType='user',
)
print(f"Unique id format for gcp iam user: {unique_id}")
# Output: Unique id format for gcp iam user: {email}
