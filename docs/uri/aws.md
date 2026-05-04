# AWS — CUID URI Specification

## Native Format

AWS uses **Amazon Resource Names (ARNs)**:

```
arn:{partition}:{service}:{region}:{account-id}:{resource-type}/{resource-id}
arn:{partition}:{service}:{region}:{account-id}:{resource-type}:{resource-id}
```

### Partitions

| Partition     | Description              |
|---------------|--------------------------|
| `aws`         | Standard commercial      |
| `aws-cn`      | China (Beijing, Ningxia) |
| `aws-us-gov`  | GovCloud (US)            |

### ARN Quirks

- Some services use `:` between resource type and ID (Lambda `function:my-func`), others use `/` (EC2 `instance/i-123`).
- Some services omit region (IAM: `arn:aws:iam::123:user/name`).
- Some services omit account (S3: `arn:aws:s3:::bucket`).
- Some resources have multi-level paths (ECS: `task/cluster-name/task-id`).

## CUID Mapping

```
aws:{service}:{account-id}:{region}:{resource-type}/{resource-id}
```

### Field Mapping

| CUID field      | Source                                                    |
|-----------------|-----------------------------------------------------------|
| `provider`      | `aws`                                                     |
| `service`       | ARN service field, lowercase                              |
| `account`       | 12-digit AWS account ID. Empty if not in ARN (e.g., S3)  |
| `region`        | AWS region. Empty if global (e.g., IAM, S3, CloudFront)  |
| `resource_type` | Resource type from ARN                                    |
| `resource_id`   | Resource identifier, preserving `/` hierarchy             |

### Partition Handling

The AWS partition is **not** encoded in the CUID directly. It is inferred from the region:

| Region prefix   | Partition     |
|-----------------|---------------|
| `cn-*`          | `aws-cn`      |
| `us-gov-*`      | `aws-us-gov`  |
| All others      | `aws`         |

This keeps CUIDs shorter and avoids redundancy. The `to_native()` conversion reconstructs the correct partition from the region.

## Conversion Rules

### Native ARN → CUID

```
arn:aws:ec2:us-east-1:123456789012:instance/i-abc123
→ aws:ec2:123456789012:us-east-1:instance/i-abc123

arn:aws:s3:::my-bucket
→ aws:s3:::bucket/my-bucket

arn:aws:iam::123456789012:user/johndoe
→ aws:iam:123456789012::user/johndoe

arn:aws:lambda:us-west-2:123456789012:function:my-func
→ aws:lambda:123456789012:us-west-2:function/my-func

arn:aws:lambda:us-west-2:123456789012:function:my-func:my-alias
→ aws:lambda:123456789012:us-west-2:alias/my-func/my-alias

arn:aws:ecs:us-east-1:123456789012:task/my-cluster/abc123
→ aws:ecs:123456789012:us-east-1:task/my-cluster/abc123
```

### CUID → Native ARN

```
aws:ec2:123456789012:us-east-1:instance/i-abc123
→ arn:aws:ec2:us-east-1:123456789012:instance/i-abc123

aws:s3:::bucket/my-bucket
→ arn:aws:s3:::my-bucket

aws:iam:123456789012::user/johndoe
→ arn:aws:iam::123456789012:user/johndoe
```

## Resource Type Catalog

### Compute

| Resource Type       | CUID Example                                                        |
|---------------------|---------------------------------------------------------------------|
| EC2 Instance        | `aws:ec2:{acct}:{region}:instance/{id}`                       |
| Lambda Function     | `aws:lambda:{acct}:{region}:function/{name}`                  |
| Lambda Alias        | `aws:lambda:{acct}:{region}:alias/{func-name}/{alias-name}`   |
| Lambda Layer        | `aws:lambda:{acct}:{region}:layer/{name}`                     |
| ECS Cluster         | `aws:ecs:{acct}:{region}:cluster/{name}`                      |
| ECS Service         | `aws:ecs:{acct}:{region}:service/{cluster}/{name}`            |
| ECS Task            | `aws:ecs:{acct}:{region}:task/{cluster}/{id}`                 |
| ECS Task Definition | `aws:ecs:{acct}:{region}:task-definition/{family}:{revision}` |
| EKS Cluster         | `aws:eks:{acct}:{region}:cluster/{name}`                      |
| Auto Scaling Group  | `aws:autoscaling:{acct}:{region}:autoScalingGroup/{id}/{name}`|

### Storage

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| S3 Bucket           | `aws:s3:::bucket/{name}`                                    |
| EBS Volume          | `aws:ec2:{acct}:{region}:volume/{id}`                       |
| EBS Snapshot        | `aws:ec2:{acct}:{region}:snapshot/{id}`                     |
| EFS File System     | `aws:elasticfilesystem:{acct}:{region}:file-system/{id}`    |

### Networking

| Resource Type       | CUID Example                                                            |
|---------------------|-------------------------------------------------------------------------|
| VPC                 | `aws:ec2:{acct}:{region}:vpc/{id}`                                |
| Subnet              | `aws:ec2:{acct}:{region}:subnet/{id}`                             |
| Security Group      | `aws:ec2:{acct}:{region}:security-group/{id}`                     |
| Internet Gateway    | `aws:ec2:{acct}:{region}:internet-gateway/{id}`                   |
| Route Table         | `aws:ec2:{acct}:{region}:route-table/{id}`                        |
| ELB Load Balancer   | `aws:elasticloadbalancing:{acct}:{region}:loadbalancer/{name}`    |
| ELB Target Group    | `aws:elasticloadbalancing:{acct}:{region}:targetgroup/{name}/{id}`|
| CloudFront Dist     | `aws:cloudfront:{acct}::distribution/{id}`                        |
| Route 53 Hosted Zone| `aws:route53:::hostedzone/{id}`                                   |

### Identity & Security

| Resource Type        | CUID Example                                            |
|----------------------|---------------------------------------------------------|
| IAM User             | `aws:iam:{acct}::user/{name}`                     |
| IAM Role             | `aws:iam:{acct}::role/{name}`                     |
| IAM Policy           | `aws:iam:{acct}::policy/{name}`                   |
| IAM Group            | `aws:iam:{acct}::group/{name}`                    |
| IAM Instance Profile | `aws:iam:{acct}::instance-profile/{name}`         |
| KMS Key              | `aws:kms:{acct}:{region}:key/{id}`                |
| Secrets Manager      | `aws:secretsmanager:{acct}:{region}:secret/{name}`|

### Database

| Resource Type       | CUID Example                                             |
|---------------------|----------------------------------------------------------|
| RDS Instance        | `aws:rds:{acct}:{region}:db/{name}`                |
| RDS Cluster         | `aws:rds:{acct}:{region}:cluster/{name}`           |
| DynamoDB Table      | `aws:dynamodb:{acct}:{region}:table/{name}`        |
| ElastiCache Cluster | `aws:elasticache:{acct}:{region}:cluster/{id}`     |
| Redshift Cluster    | `aws:redshift:{acct}:{region}:cluster/{name}`      |

### Monitoring & Logging

| Resource Type        | CUID Example                                            |
|----------------------|---------------------------------------------------------|
| CloudWatch Alarm     | `aws:cloudwatch:{acct}:{region}:alarm/{name}`     |
| CloudWatch Log Group | `aws:logs:{acct}:{region}:log-group/{name}`       |
| CloudTrail Trail     | `aws:cloudtrail:{acct}:{region}:trail/{name}`     |
| SNS Topic            | `aws:sns:{acct}:{region}:topic/{name}`            |
| SQS Queue            | `aws:sqs:{acct}:{region}:queue/{name}`            |
| EventBridge Rule     | `aws:events:{acct}:{region}:rule/{name}`          |

## Edge Cases

1. **S3 bucket ARNs** omit both account and region. CUID preserves this: `aws:s3:::bucket/name`.
2. **Lambda qualifiers** (alias, version) are sub-resources. The function name is part of the resource ID: `alias/func-name/alias-name`.
3. **IAM paths** — IAM resources can have paths (`/engineering/devops/role-name`). The full path is preserved in the resource ID.
4. **Cross-account resources** — Some ARNs reference resources in other accounts. The CUID uses the account that owns the resource.
5. **Wildcard ARNs** (used in IAM policies) are not valid CUIDs. CUIDs identify specific resources, not patterns.
