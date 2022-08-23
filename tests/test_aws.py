from clouduniqueid.clouds.aws import AWSUniqueId

aws = AWSUniqueId()


def test_aws_ec2_instance():
    resourceName = 'instance-12345'
    service = 'ec2'
    region = 'us-east-1'
    accountId = '12345'
    resourceType = 'instance'
    expected_id = "arn:aws:ec2:us-east-1:12345:instance/instance-12345"

    out_id = aws.get_unique_id(
        resourceName=resourceName, service=service, region=region,
        accountId=accountId, resourceType=resourceType
    )

    assert out_id == expected_id.replace(" ", "")


def test_aws_s3_bucket():
    resourceName = 'bucket12345'
    service = 's3'
    resourceType = 'bucket'
    expected_id = "arn:aws:s3:::bucket12345"

    out_id = aws.get_unique_id(
        resourceName=resourceName, service=service, resourceType=resourceType
    )

    assert out_id == expected_id.replace(" ", "")
