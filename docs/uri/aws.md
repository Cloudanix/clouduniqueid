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
cuid:aws:{service}:{account-id}:{region}:{resource-type}/{resource-id}
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
→ cuid:aws:ec2:123456789012:us-east-1:instance/i-abc123

arn:aws:s3:::my-bucket
→ cuid:aws:s3:::bucket/my-bucket

arn:aws:iam::123456789012:user/johndoe
→ cuid:aws:iam:123456789012::user/johndoe

arn:aws:lambda:us-west-2:123456789012:function:my-func
→ cuid:aws:lambda:123456789012:us-west-2:function/my-func

arn:aws:lambda:us-west-2:123456789012:function:my-func:my-alias
→ cuid:aws:lambda:123456789012:us-west-2:alias/my-func/my-alias

arn:aws:ecs:us-east-1:123456789012:task/my-cluster/abc123
→ cuid:aws:ecs:123456789012:us-east-1:task/my-cluster/abc123
```

### CUID → Native ARN

```
cuid:aws:ec2:123456789012:us-east-1:instance/i-abc123
→ arn:aws:ec2:us-east-1:123456789012:instance/i-abc123

cuid:aws:s3:::bucket/my-bucket
→ arn:aws:s3:::my-bucket

cuid:aws:iam:123456789012::user/johndoe
→ arn:aws:iam::123456789012:user/johndoe
```

## Resource Type Catalog

### Compute

| Resource Type       | CUID Example                                                        |
|---------------------|---------------------------------------------------------------------|
| EC2 Instance        | `cuid:aws:ec2:{acct}:{region}:instance/{id}`                       |
| Lambda Function     | `cuid:aws:lambda:{acct}:{region}:function/{name}`                  |
| Lambda Alias        | `cuid:aws:lambda:{acct}:{region}:alias/{func-name}/{alias-name}`   |
| Lambda Layer        | `cuid:aws:lambda:{acct}:{region}:layer/{name}`                     |
| ECS Cluster         | `cuid:aws:ecs:{acct}:{region}:cluster/{name}`                      |
| ECS Service         | `cuid:aws:ecs:{acct}:{region}:service/{cluster}/{name}`            |
| ECS Task            | `cuid:aws:ecs:{acct}:{region}:task/{cluster}/{id}`                 |
| ECS Task Definition | `cuid:aws:ecs:{acct}:{region}:task-definition/{family}:{revision}` |
| EKS Cluster         | `cuid:aws:eks:{acct}:{region}:cluster/{name}`                      |
| Auto Scaling Group  | `cuid:aws:autoscaling:{acct}:{region}:autoScalingGroup/{id}/{name}`|

### Storage

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| S3 Bucket           | `cuid:aws:s3:::bucket/{name}`                                    |
| EBS Volume          | `cuid:aws:ec2:{acct}:{region}:volume/{id}`                       |
| EBS Snapshot        | `cuid:aws:ec2:{acct}:{region}:snapshot/{id}`                     |
| EFS File System     | `cuid:aws:elasticfilesystem:{acct}:{region}:file-system/{id}`    |

### Networking

| Resource Type       | CUID Example                                                            |
|---------------------|-------------------------------------------------------------------------|
| VPC                 | `cuid:aws:ec2:{acct}:{region}:vpc/{id}`                                |
| Subnet              | `cuid:aws:ec2:{acct}:{region}:subnet/{id}`                             |
| Security Group      | `cuid:aws:ec2:{acct}:{region}:security-group/{id}`                     |
| Internet Gateway    | `cuid:aws:ec2:{acct}:{region}:internet-gateway/{id}`                   |
| Route Table         | `cuid:aws:ec2:{acct}:{region}:route-table/{id}`                        |
| ELB Load Balancer   | `cuid:aws:elasticloadbalancing:{acct}:{region}:loadbalancer/{name}`    |
| ELB Target Group    | `cuid:aws:elasticloadbalancing:{acct}:{region}:targetgroup/{name}/{id}`|
| CloudFront Dist     | `cuid:aws:cloudfront:{acct}::distribution/{id}`                        |
| Route 53 Hosted Zone| `cuid:aws:route53:::hostedzone/{id}`                                   |

### Identity & Security

| Resource Type        | CUID Example                                            |
|----------------------|---------------------------------------------------------|
| IAM User             | `cuid:aws:iam:{acct}::user/{name}`                     |
| IAM Role             | `cuid:aws:iam:{acct}::role/{name}`                     |
| IAM Policy           | `cuid:aws:iam:{acct}::policy/{name}`                   |
| IAM Group            | `cuid:aws:iam:{acct}::group/{name}`                    |
| IAM Instance Profile | `cuid:aws:iam:{acct}::instance-profile/{name}`         |
| KMS Key              | `cuid:aws:kms:{acct}:{region}:key/{id}`                |
| Secrets Manager      | `cuid:aws:secretsmanager:{acct}:{region}:secret/{name}`|

### Database

| Resource Type       | CUID Example                                             |
|---------------------|----------------------------------------------------------|
| RDS Instance        | `cuid:aws:rds:{acct}:{region}:db/{name}`                |
| RDS Cluster         | `cuid:aws:rds:{acct}:{region}:cluster/{name}`           |
| DynamoDB Table      | `cuid:aws:dynamodb:{acct}:{region}:table/{name}`        |
| ElastiCache Cluster | `cuid:aws:elasticache:{acct}:{region}:cluster/{id}`     |
| Redshift Cluster    | `cuid:aws:redshift:{acct}:{region}:cluster/{name}`      |

### Monitoring & Logging

| Resource Type        | CUID Example                                            |
|----------------------|---------------------------------------------------------|
| CloudWatch Alarm     | `cuid:aws:cloudwatch:{acct}:{region}:alarm/{name}`     |
| CloudWatch Log Group | `cuid:aws:logs:{acct}:{region}:log-group/{name}`       |
| CloudTrail Trail     | `cuid:aws:cloudtrail:{acct}:{region}:trail/{name}`     |
| SNS Topic            | `cuid:aws:sns:{acct}:{region}:topic/{name}`            |
| SQS Queue            | `cuid:aws:sqs:{acct}:{region}:queue/{name}`            |
| EventBridge Rule     | `cuid:aws:events:{acct}:{region}:rule/{name}`          |

## Edge Cases

1. **S3 bucket ARNs** omit both account and region. CUID preserves this: `cuid:aws:s3:::bucket/name`.
2. **Lambda qualifiers** (alias, version) are sub-resources. The function name is part of the resource ID: `alias/func-name/alias-name`.
3. **IAM paths** — IAM resources can have paths (`/engineering/devops/role-name`). The full path is preserved in the resource ID.
4. **Cross-account resources** — Some ARNs reference resources in other accounts. The CUID uses the account that owns the resource.
5. **Wildcard ARNs** (used in IAM policies) are not valid CUIDs. CUIDs identify specific resources, not patterns.
