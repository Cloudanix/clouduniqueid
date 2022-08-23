from clouduniqueid.clouds.aws import AWSUniqueId

aws = AWSUniqueId()
region = 'us-east-1'
accountId = '12345'


def test_aws_ec2_instance():
    resource = 'i-12345'
    service = 'ec2'
    resourceType = 'instance'
    expected_id = "arn:aws:ec2:us-east-1:12345:instance/i-12345"

    out_id = aws.get_unique_id(
        resource=resource, service=service, region=region,
        accountId=accountId, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")


def test_aws_s3_bucket():
    resource = 'b12345'
    service = 's3'
    resourceType = 'bucket'
    expected_id = "arn:aws:s3:::b12345"

    out_id = aws.get_unique_id(
        resource=resource, service=service, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")


def test_aws_lambda_function():
    resource = 'f12345'
    service = 'lambda'
    resourceType = 'function'
    expected_id = "arn:aws:lambda:us-east-1:12345:function:f12345"

    out_id = aws.get_unique_id(
        resource=resource, service=service, region=region,
        accountId=accountId, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")


def test_aws_lambda_function_alias():
    parent = 'f12345'
    resource = 'a12345'
    service = 'lambda'
    resourceType = 'alias'
    expected_id = "arn:aws:lambda:us-east-1:12345:function:f12345:a12345"

    out_id = aws.get_unique_id(
        resource=resource, service=service, region=region,
        parent=parent, accountId=accountId, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")
