# GCP — CUID URI Specification

## Native Format

GCP uses **hierarchical resource names** in two forms:

### Full Resource Name
```
//service.googleapis.com/{relative-resource-name}
```
Examples:
```
//compute.googleapis.com/projects/my-project/zones/us-central1-a/instances/my-vm
//storage.googleapis.com/projects/_/buckets/my-bucket
//iam.googleapis.com/projects/my-project/serviceAccounts/sa@my-project.iam.gserviceaccount.com
```

### Relative Resource Name
```
projects/{project}/locations/{location}/{collection}/{resource}
projects/{project}/zones/{zone}/{collection}/{resource}
organizations/{org}/{collection}/{resource}
```

### GCP Quirks

- No single canonical format — some APIs return full resource names, others return relative names, others return just the resource ID.
- Hierarchy varies: `projects/` vs `organizations/` vs `folders/` as root.
- Location can be a region (`us-central1`), zone (`us-central1-a`), or `global`.
- Some resources are project-scoped, some org-scoped, some global.

## CUID Mapping

```
cuid:gcp:{service}:{project}:{location}:{resource-type}/{resource-id}
```

### Field Mapping

| CUID field      | Source                                                        |
|-----------------|---------------------------------------------------------------|
| `provider`      | `gcp`                                                         |
| `service`       | GCP API service name, normalized (see table below)            |
| `account`       | GCP project ID. For org-level resources: `org/{org-id}`       |
| `region`        | Location, zone, or `global`. Empty if not applicable          |
| `resource_type` | Resource type, lowercase                                      |
| `resource_id`   | Resource name or ID                                           |

### Service Name Normalization

| GCP API Service                    | CUID `service`     |
|------------------------------------|---------------------|
| `compute.googleapis.com`           | `compute`           |
| `storage.googleapis.com`           | `storage`           |
| `iam.googleapis.com`               | `iam`               |
| `container.googleapis.com`         | `container`         |
| `sqladmin.googleapis.com`          | `sql`               |
| `cloudfunctions.googleapis.com`    | `functions`         |
| `run.googleapis.com`               | `run`               |
| `logging.googleapis.com`           | `logging`           |
| `monitoring.googleapis.com`        | `monitoring`        |
| `pubsub.googleapis.com`            | `pubsub`            |
| `bigquery.googleapis.com`          | `bigquery`          |
| `bigtable.googleapis.com`          | `bigtable`          |
| `spanner.googleapis.com`           | `spanner`           |
| `dns.googleapis.com`               | `dns`               |
| `secretmanager.googleapis.com`     | `secretmanager`     |
| `cloudkms.googleapis.com`          | `kms`               |
| `apigateway.googleapis.com`        | `apigateway`        |
| `cloudbuild.googleapis.com`        | `cloudbuild`        |
| `artifactregistry.googleapis.com`  | `artifactregistry`  |

## Conversion Rules

### Native → CUID

```
//compute.googleapis.com/projects/my-project/zones/us-central1-a/instances/my-vm
→ cuid:gcp:compute:my-project:us-central1-a:instance/my-vm

//storage.googleapis.com/projects/_/buckets/my-bucket
→ cuid:gcp:storage:::bucket/my-bucket

//iam.googleapis.com/projects/my-project/serviceAccounts/sa@proj.iam.gserviceaccount.com
→ cuid:gcp:iam:my-project::service-account/sa@proj.iam.gserviceaccount.com

projects/my-project/locations/us-central1/functions/my-func
→ cuid:gcp:functions:my-project:us-central1:function/my-func

organizations/123456/roles/myCustomRole
→ cuid:gcp:iam:org/123456::role/myCustomRole
```

### CUID → Native

```
cuid:gcp:compute:my-project:us-central1-a:instance/my-vm
→ //compute.googleapis.com/projects/my-project/zones/us-central1-a/instances/my-vm

cuid:gcp:storage:::bucket/my-bucket
→ //storage.googleapis.com/projects/_/buckets/my-bucket

cuid:gcp:iam:my-project::role/roles/editor
→ projects/my-project/roles/editor
```

## Resource Type Catalog

### Compute

| Resource Type       | CUID Example                                                       |
|---------------------|--------------------------------------------------------------------|
| VM Instance         | `cuid:gcp:compute:{proj}:{zone}:instance/{name}`                  |
| Instance Template   | `cuid:gcp:compute:{proj}:global:instance-template/{name}`         |
| Instance Group      | `cuid:gcp:compute:{proj}:{zone}:instance-group/{name}`            |
| Disk                | `cuid:gcp:compute:{proj}:{zone}:disk/{name}`                      |
| Snapshot            | `cuid:gcp:compute:{proj}:global:snapshot/{name}`                  |
| Image               | `cuid:gcp:compute:{proj}:global:image/{name}`                     |
| Cloud Function      | `cuid:gcp:functions:{proj}:{region}:function/{name}`              |
| Cloud Run Service   | `cuid:gcp:run:{proj}:{region}:service/{name}`                     |
| GKE Cluster         | `cuid:gcp:container:{proj}:{location}:cluster/{name}`             |
| GKE Node Pool       | `cuid:gcp:container:{proj}:{location}:node-pool/{cluster}/{name}` |

### Storage & Database

| Resource Type       | CUID Example                                                       |
|---------------------|--------------------------------------------------------------------|
| GCS Bucket          | `cuid:gcp:storage:::bucket/{name}`                                 |
| GCS Object          | `cuid:gcp:storage:::object/{bucket}/{path}`                        |
| Cloud SQL Instance  | `cuid:gcp:sql:{proj}:{region}:instance/{name}`                    |
| Cloud SQL Database  | `cuid:gcp:sql:{proj}:{region}:database/{instance}/{name}`         |
| Spanner Instance    | `cuid:gcp:spanner:{proj}::instance/{name}`                        |
| Spanner Database    | `cuid:gcp:spanner:{proj}::database/{instance}/{name}`             |
| Bigtable Instance   | `cuid:gcp:bigtable:{proj}::instance/{name}`                       |
| Bigtable Table      | `cuid:gcp:bigtable:{proj}::table/{instance}/{name}`               |
| BigQuery Dataset    | `cuid:gcp:bigquery:{proj}:{location}:dataset/{name}`              |
| BigQuery Table      | `cuid:gcp:bigquery:{proj}:{location}:table/{dataset}/{name}`      |

### Networking

| Resource Type       | CUID Example                                                       |
|---------------------|--------------------------------------------------------------------|
| VPC Network         | `cuid:gcp:compute:{proj}:global:network/{name}`                   |
| Subnetwork          | `cuid:gcp:compute:{proj}:{region}:subnetwork/{name}`              |
| Firewall Rule       | `cuid:gcp:compute:{proj}:global:firewall/{name}`                  |
| External IP         | `cuid:gcp:compute:{proj}:{region}:address/{name}`                 |
| Cloud DNS Zone      | `cuid:gcp:dns:{proj}::managed-zone/{name}`                        |
| Load Balancer       | `cuid:gcp:compute:{proj}:global:url-map/{name}`                   |

### Identity & Security

| Resource Type          | CUID Example                                                    |
|------------------------|-----------------------------------------------------------------|
| Service Account        | `cuid:gcp:iam:{proj}::service-account/{email}`                 |
| IAM Role (predefined)  | `cuid:gcp:iam:::role/roles/{name}`                             |
| IAM Role (project)     | `cuid:gcp:iam:{proj}::role/{name}`                             |
| IAM Role (org)         | `cuid:gcp:iam:org/{org-id}::role/{name}`                       |
| KMS Key Ring           | `cuid:gcp:kms:{proj}:{location}:key-ring/{name}`              |
| KMS Crypto Key         | `cuid:gcp:kms:{proj}:{location}:crypto-key/{ring}/{name}`     |
| Secret                 | `cuid:gcp:secretmanager:{proj}::secret/{name}`                 |

### Monitoring & Logging

| Resource Type        | CUID Example                                                     |
|----------------------|------------------------------------------------------------------|
| Log Sink             | `cuid:gcp:logging:{proj}::sink/{name}`                          |
| Log Metric           | `cuid:gcp:logging:{proj}::metric/{name}`                        |
| Alert Policy         | `cuid:gcp:monitoring:{proj}::alert-policy/{id}`                 |
| Pub/Sub Topic        | `cuid:gcp:pubsub:{proj}::topic/{name}`                          |
| Pub/Sub Subscription | `cuid:gcp:pubsub:{proj}::subscription/{name}`                   |

## Edge Cases

1. **Org-level resources** — Use `org/{org-id}` as the account field: `cuid:gcp:iam:org/123456::role/myRole`.
2. **Folder-level resources** — Use `folder/{folder-id}`: `cuid:gcp:resourcemanager:folder/456::folder/456`.
3. **Global buckets** — GCS buckets are globally unique and not project-scoped in their name. Account and region are empty.
4. **Zone vs region** — The region field contains whatever location granularity the resource uses (zone, region, or `global`).
5. **Self-links** — GCP sometimes returns full URLs (`https://compute.googleapis.com/...`). Strip the scheme and hostname before mapping.
