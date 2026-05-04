# Cloud Unique ID (CUID) — URI Specification

## Purpose

Every cloud and SCM provider has its own resource identifier format — AWS has ARNs, Azure has resource IDs, GCP has resource names, OCI has OCIDs, and SCM providers use slug paths or numeric IDs. There is no uniform way to reference a resource across providers.

**Cloud Unique ID (CUID)** defines a canonical URI scheme that uniquely identifies any resource across any supported provider. It enables:

- Cross-cloud inventory and asset management
- Unified policy engines and compliance rules
- Consistent logging, alerting, and correlation
- Bidirectional mapping: `native_id ↔ cuid`

## Universal Format

```
cuid:{provider}:{service}:{account}:{region}:{resource_type}/{resource_id}
```

| Field           | Description                                                  | Required |
|-----------------|--------------------------------------------------------------|----------|
| `cuid`          | Fixed scheme prefix                                          | Yes      |
| `provider`      | Provider identifier (see table below)                        | Yes      |
| `service`       | Service name, normalized to lowercase                        | Yes      |
| `account`       | Account/subscription/project/org scope                       | Varies   |
| `region`        | Region or location. Empty string if global                   | Varies   |
| `resource_type` | Resource type within the service                             | Yes      |
| `resource_id`   | Resource identifier, may contain `/` for hierarchical resources | Yes   |

### Provider Identifiers

| Provider    | `provider` value | Native ID format          |
|-------------|------------------|---------------------------|
| AWS         | `aws`            | ARN                       |
| GCP         | `gcp`            | Resource name             |
| Azure       | `azure`          | Resource ID               |
| OCI         | `oci`            | OCID                      |
| GitHub      | `github`         | Owner/repo paths          |
| Bitbucket   | `bitbucket`      | Workspace/repo slugs      |
| GitLab      | `gitlab`         | Namespace/project paths   |
| Azure DevOps| `azuredevops`    | Org/project paths + GUIDs |

### Partitions

Some providers operate in isolated partitions (e.g., AWS GovCloud, Azure Government). The `account` field encodes partition context where applicable. See each provider spec for details.

## Design Principles

1. **Deterministic** — The same resource always produces the same CUID. No randomness.
2. **Parseable** — Every CUID can be split on `:` to extract its components. The `resource_type/resource_id` portion uses `/` as a sub-delimiter.
3. **Reversible** — A CUID can be converted back to the provider's native ID format.
4. **Case-normalized** — All fields are lowercase except `resource_id`, which preserves the provider's casing rules.
5. **Stable** — Renaming a resource (where the provider allows it) changes the CUID. The CUID tracks the logical identity, not an internal database key.

## Encoding Rules

- Fields are separated by `:` (colon).
- Resource type and resource ID are separated by `/` (slash).
- Empty optional fields are represented as empty strings between delimiters: `cuid:aws:s3:::bucket/my-bucket`.
- Characters outside `[a-zA-Z0-9._\-/@ ]` in resource IDs are percent-encoded.
- The scheme prefix `cuid:` is always lowercase.

## Examples

```
# AWS EC2 instance
cuid:aws:ec2:123456789012:us-east-1:instance/i-1234567890abcdef0

# AWS S3 bucket (global, no account in native ARN)
cuid:aws:s3:::bucket/my-bucket

# GCP Compute Engine VM
cuid:gcp:compute:my-project:us-central1-a:instance/my-vm

# Azure Virtual Machine
cuid:azure:compute:sub-123/my-rg::virtualMachines/my-vm

# OCI Compute Instance
cuid:oci:compute:ocid1.tenancy.oc1..aaa:us-ashburn-1:instance/ocid1.instance.oc1.iad.abc123

# GitHub repository
cuid:github:repos:facebook::repository/react

# Bitbucket repository
cuid:bitbucket:repos:my-workspace::repository/my-project/my-repo

# GitLab project
cuid:gitlab:projects:gitlab-org::project/gitlab

# Azure DevOps repository
cuid:azuredevops:repos:my-org/my-project::repository/my-repo
```

## Provider Specs

Each provider has a detailed specification documenting the mapping between native IDs and CUIDs:

| Provider     | Spec                              |
|--------------|-----------------------------------|
| AWS          | [docs/uri/aws.md](aws.md)        |
| GCP          | [docs/uri/gcp.md](gcp.md)        |
| Azure        | [docs/uri/azure.md](azure.md)    |
| OCI          | [docs/uri/oci.md](oci.md)        |
| GitHub       | [docs/uri/github.md](github.md)  |
| Bitbucket    | [docs/uri/bitbucket.md](bitbucket.md) |
| GitLab       | [docs/uri/gitlab.md](gitlab.md)  |
| Azure DevOps | [docs/uri/azure-devops.md](azure-devops.md) |

## Versioning

This spec is **v0.1.0** (draft). Breaking changes are expected before v1.0.
