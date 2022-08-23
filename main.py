from clouduniqueid.clouds.aws import AWSUniqueId

aws_unique_id = AWSUniqueId()

# Unique id for S3 Bucket
unique_id = aws_unique_id.get_unique_id(
    resourceName='bucket12345', service='s3', partition='aws', resourceType='bucket')
print(f"Unique id for S3 Bucket: {unique_id}")
# Outpute: Unique id for S3 Bucket: arn:aws:s3:::bucket12345


# Unique id for EC2 instance
unique_id = aws_unique_id.get_unique_id(
    resourceName='instance-12345', service='ec2', region='us-east-1',
    partition='aws', accountId='12345', resourceType='instance')
print(f"Unique id for EC2 instance: {unique_id}")
# Outpute: Unique id for EC2 instance: arn:aws:ec2:us-east-1:12345:instance/instance-12345
