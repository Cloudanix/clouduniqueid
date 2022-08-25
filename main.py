from clouduniqueid.clouds.aws import AWSUniqueId

aws_unique_id = AWSUniqueId()
region = 'us-east-1'
accountId = '12345'
partition = 'aws'

# Unique id for S3 Bucket
unique_id = aws_unique_id.get_unique_id(
    data={'bucketName': 'b12345'}, service='s3', partition='aws', resourceType='bucket',
)
print(f"Unique id for S3 Bucket: {unique_id}")
# Output: Unique id for S3 Bucket: arn:aws:s3:::b12345


# Unique id for EC2 instance
unique_id = aws_unique_id.get_unique_id(
    service='ec2', region=region, accountId=accountId,
    partition=partition, resourceType='instance', data={'InstanceId': 'i-12345'},
)
print(f"Unique id for EC2 instance: {unique_id}")
# Output: Unique id for EC2 instance: arn:aws:ec2:us-east-1:12345:instance/i-12345


# Unique id for lambda function
unique_id = aws_unique_id.get_unique_id(
    data={'FunctionName': 'f12345'}, service='lambda', region=region,
    partition=partition, accountId=accountId, resourceType='function',
)
print(f"Unique id for lambda function: {unique_id}")
# Output: Unique id for lambda function: arn:aws:lambda:us-east-1:12345:function:f12345


# Unique id for lambda function alias
unique_id = aws_unique_id.get_unique_id(
    data={'FunctionName': 'f12345', 'name': 'a12345'}, service='lambda', region=region,
    partition=partition, accountId=accountId, resourceType='alias',
)
print(f"Unique id for lambda function alias: {unique_id}")
# Output: Unique id for lambda function alias: arn:aws:lambda:us-east-1:12345:function:f12345:a12345

# Unique id format for lambda function alias
unique_id_format = aws_unique_id.get_unique_id_format(
    service='lambda', resourceType='alias',
)
print(f"Unique id format for lambda function alias: {unique_id_format}")
# Output: Unique id format for lambda function alias:
# arn:{partition}:lambda:{region}:{accountId}:function:{FunctionName}:{Name}
