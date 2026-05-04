# OCI — CUID URI Specification

## Native Format

Oracle Cloud Infrastructure uses **OCIDs** (Oracle Cloud Identifiers):

```
ocid1.{resource-type}.{realm}.[{region}][.{future-use}].{unique-id}
```

Examples:
```
ocid1.instance.oc1.iad.abcdefghijklmnop123456
ocid1.compartment.oc1..aaaaaaaabcdefghijklmnop
ocid1.vcn.oc1.phx.abcdefghijklmnop123456
ocid1.tenancy.oc1..aaaaaaaabcdefghijklmnop
ocid1.bucket.oc1.iad.aaaaaaaabcdefghijklmnop
```

### OCID Structure

| Field           | Description                                          |
|-----------------|------------------------------------------------------|
| `ocid1`         | Fixed prefix (version 1)                             |
| `resource-type` | Resource type (e.g., `instance`, `vcn`, `subnet`)    |
| `realm`         | Cloud realm (see table below)                        |
| `region`        | 3-letter region code. Empty for global resources     |
| `unique-id`     | Opaque unique identifier                             |

### Realms

| Realm  | Description                          |
|--------|--------------------------------------|
| `oc1`  | Commercial (public cloud)            |
| `oc2`  | US Government (FedRAMP High)         |
| `oc3`  | US Government (DoD)                  |
| `oc4`  | UK Government                        |
| `oc8`  | Dedicated Region                     |
| `oc9`  | Drcc (EU Sovereign)                  |
| `oc10` | Drcc (EU Sovereign)                  |
| `oc14` | Drcc (EU Sovereign)                  |
| `oc20` | National Security (US)               |
| `oc21` | National Security (UK)               |
| `oc24` | National Security (EU)               |
| `oc26` | Alloy                                |

### Region Codes

| Code  | Region Name          |
|-------|----------------------|
| `iad` | us-ashburn-1         |
| `phx` | us-phoenix-1         |
| `lhr` | uk-london-1          |
| `fra` | eu-frankfurt-1       |
| `nrt` | ap-tokyo-1           |
| `icn` | ap-seoul-1           |
| `syd` | ap-sydney-1          |
| `yyz` | ca-toronto-1         |
| `gru` | sa-saopaulo-1        |
| `bom` | ap-mumbai-1          |

(Partial list — OCI has 40+ regions.)

### OCID Quirks

- Global resources (tenancy, compartment) have an empty region field, resulting in `..` in the OCID.
- The unique-id portion is opaque and varies in length.
- Resource types in OCIDs are singular and lowercase (e.g., `instance`, not `instances`).

## CUID Mapping

```
cuid:oci:{service}:{tenancy-ocid}:{region}:{resource-type}/{ocid}
```

### Field Mapping

| CUID field      | Source                                                        |
|-----------------|---------------------------------------------------------------|
| `provider`      | `oci`                                                         |
| `service`       | OCI service name, normalized (see table below)                |
| `account`       | Tenancy OCID or compartment OCID                              |
| `region`        | Full region name (e.g., `us-ashburn-1`). Empty if global      |
| `resource_type` | Resource type from the OCID                                   |
| `resource_id`   | Full OCID of the resource                                     |

### Service Name Normalization

| OCI Service                | CUID `service`  |
|----------------------------|------------------|
| Core (Compute)             | `compute`        |
| Core (Networking)          | `network`        |
| Core (Block Storage)       | `blockstorage`   |
| Object Storage             | `objectstorage`  |
| File Storage               | `filestorage`    |
| Identity                   | `identity`       |
| Database                   | `database`       |
| Container Engine (OKE)     | `oke`            |
| Functions                  | `functions`      |
| Load Balancer              | `loadbalancer`   |
| DNS                        | `dns`            |
| Vault (KMS)                | `vault`          |
| Monitoring                 | `monitoring`     |
| Logging                    | `logging`        |
| Events                     | `events`         |
| Notifications              | `notifications`  |
| Streaming                  | `streaming`      |

## Conversion Rules

### Native OCID → CUID

```
ocid1.instance.oc1.iad.abcdef123456
→ cuid:oci:compute:{tenancy}:us-ashburn-1:instance/ocid1.instance.oc1.iad.abcdef123456

ocid1.vcn.oc1.phx.abcdef123456
→ cuid:oci:network:{tenancy}:us-phoenix-1:vcn/ocid1.vcn.oc1.phx.abcdef123456

ocid1.compartment.oc1..aaaaaaaabcdef
→ cuid:oci:identity:{tenancy}::compartment/ocid1.compartment.oc1..aaaaaaaabcdef

ocid1.bucket.oc1.iad.aaaaaaaabcdef
→ cuid:oci:objectstorage:{tenancy}:us-ashburn-1:bucket/ocid1.bucket.oc1.iad.aaaaaaaabcdef
```

### CUID → Native OCID

The resource_id field contains the full OCID, so conversion back is direct extraction.

```
cuid:oci:compute:{tenancy}:us-ashburn-1:instance/ocid1.instance.oc1.iad.abcdef123456
→ ocid1.instance.oc1.iad.abcdef123456
```

## Resource Type Catalog

### Compute

| Resource Type       | CUID Example                                                          |
|---------------------|-----------------------------------------------------------------------|
| Instance            | `cuid:oci:compute:{tenancy}:{region}:instance/{ocid}`                |
| Image               | `cuid:oci:compute:{tenancy}:{region}:image/{ocid}`                   |
| Boot Volume         | `cuid:oci:blockstorage:{tenancy}:{region}:boot-volume/{ocid}`        |
| Volume              | `cuid:oci:blockstorage:{tenancy}:{region}:volume/{ocid}`             |
| Dedicated VM Host   | `cuid:oci:compute:{tenancy}:{region}:dedicated-vm-host/{ocid}`       |
| OKE Cluster         | `cuid:oci:oke:{tenancy}:{region}:cluster/{ocid}`                     |
| OKE Node Pool       | `cuid:oci:oke:{tenancy}:{region}:node-pool/{ocid}`                   |
| Function            | `cuid:oci:functions:{tenancy}:{region}:function/{ocid}`              |

### Storage

| Resource Type       | CUID Example                                                          |
|---------------------|-----------------------------------------------------------------------|
| Bucket              | `cuid:oci:objectstorage:{tenancy}:{region}:bucket/{ocid}`            |
| File System         | `cuid:oci:filestorage:{tenancy}:{region}:file-system/{ocid}`         |
| Mount Target        | `cuid:oci:filestorage:{tenancy}:{region}:mount-target/{ocid}`        |

### Networking

| Resource Type       | CUID Example                                                          |
|---------------------|-----------------------------------------------------------------------|
| VCN                 | `cuid:oci:network:{tenancy}:{region}:vcn/{ocid}`                     |
| Subnet              | `cuid:oci:network:{tenancy}:{region}:subnet/{ocid}`                  |
| Security List       | `cuid:oci:network:{tenancy}:{region}:security-list/{ocid}`           |
| NSG                 | `cuid:oci:network:{tenancy}:{region}:network-security-group/{ocid}`  |
| Route Table         | `cuid:oci:network:{tenancy}:{region}:route-table/{ocid}`             |
| Internet Gateway    | `cuid:oci:network:{tenancy}:{region}:internet-gateway/{ocid}`        |
| NAT Gateway         | `cuid:oci:network:{tenancy}:{region}:nat-gateway/{ocid}`             |
| Load Balancer       | `cuid:oci:loadbalancer:{tenancy}:{region}:load-balancer/{ocid}`      |
| DNS Zone            | `cuid:oci:dns:{tenancy}::zone/{ocid}`                                |

### Identity

| Resource Type       | CUID Example                                                          |
|---------------------|-----------------------------------------------------------------------|
| Tenancy             | `cuid:oci:identity:{tenancy}::tenancy/{ocid}`                        |
| Compartment         | `cuid:oci:identity:{tenancy}::compartment/{ocid}`                    |
| User                | `cuid:oci:identity:{tenancy}::user/{ocid}`                           |
| Group               | `cuid:oci:identity:{tenancy}::group/{ocid}`                          |
| Policy              | `cuid:oci:identity:{tenancy}::policy/{ocid}`                         |
| Dynamic Group       | `cuid:oci:identity:{tenancy}::dynamic-group/{ocid}`                  |
| Vault               | `cuid:oci:vault:{tenancy}:{region}:vault/{ocid}`                     |
| Key                 | `cuid:oci:vault:{tenancy}:{region}:key/{ocid}`                       |

### Database

| Resource Type       | CUID Example                                                          |
|---------------------|-----------------------------------------------------------------------|
| DB System           | `cuid:oci:database:{tenancy}:{region}:db-system/{ocid}`              |
| Autonomous DB       | `cuid:oci:database:{tenancy}:{region}:autonomous-database/{ocid}`    |
| MySQL DB System     | `cuid:oci:database:{tenancy}:{region}:mysql-db-system/{ocid}`        |

### Monitoring

| Resource Type       | CUID Example                                                          |
|---------------------|-----------------------------------------------------------------------|
| Alarm               | `cuid:oci:monitoring:{tenancy}:{region}:alarm/{ocid}`                |
| Log Group           | `cuid:oci:logging:{tenancy}:{region}:log-group/{ocid}`               |
| Log                 | `cuid:oci:logging:{tenancy}:{region}:log/{ocid}`                     |
| Topic               | `cuid:oci:notifications:{tenancy}:{region}:topic/{ocid}`             |
| Stream              | `cuid:oci:streaming:{tenancy}:{region}:stream/{ocid}`                |

## Edge Cases

1. **OCID as resource_id** — Unlike other providers, the full OCID is preserved as the resource_id. This ensures lossless round-tripping since OCIDs contain embedded realm and region info.
2. **Global resources** — Tenancy, compartments, users, groups, and policies are global (no region). The region field is empty.
3. **Realm inference** — The realm (`oc1`, `oc2`, etc.) is embedded in the OCID and does not need a separate CUID field. It's analogous to AWS partition inference from region.
4. **Region code mapping** — OCIDs use 3-letter region codes (`iad`, `phx`). CUIDs use the full region name (`us-ashburn-1`) for readability. The library must maintain a mapping table.
5. **Compartment hierarchy** — OCI compartments are hierarchical. The CUID uses the tenancy OCID as the account field regardless of compartment depth. Compartment context is in the resource metadata, not the CUID.
