# Azure — CUID URI Specification

## Native Format

Azure uses **Resource IDs** — hierarchical paths rooted at a subscription:

```
/subscriptions/{sub-id}/resourceGroups/{rg}/providers/{namespace}/{type}/{name}
```

Examples:
```
/subscriptions/sub-123/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM
/subscriptions/sub-123/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/myStorage
/subscriptions/sub-123/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet
```

### Scope Levels

| Scope            | Format                                                              |
|------------------|---------------------------------------------------------------------|
| Tenant           | `/providers/{namespace}/{type}/{name}`                              |
| Management Group | `/providers/Microsoft.Management/managementGroups/{mg-id}`          |
| Subscription     | `/subscriptions/{sub-id}`                                           |
| Resource Group   | `/subscriptions/{sub-id}/resourceGroups/{rg}`                       |
| Resource         | `/subscriptions/{sub-id}/resourceGroups/{rg}/providers/{ns}/{t}/{n}`|
| Child Resource   | `.../{parent-type}/{parent}/.../{child-type}/{child}`               |

### Azure Quirks

- Resource IDs are case-insensitive but conventionally mixed-case.
- Child resources are nested: `.../virtualNetworks/myVNet/subnets/mySubnet`.
- The provider namespace is always `Microsoft.{Service}` or a third-party namespace.
- Some resources are subscription-level (no resource group).
- Tenant-level resources have no subscription prefix.

## CUID Mapping

```
cuid:azure:{service}:{subscription}/{resource-group}:{region}:{resource-type}/{resource-id}
```

### Field Mapping

| CUID field      | Source                                                              |
|-----------------|---------------------------------------------------------------------|
| `provider`      | `azure`                                                             |
| `service`       | Azure namespace, normalized (see table below)                       |
| `account`       | `{subscription-id}/{resource-group}`. RG omitted if sub-level      |
| `region`        | Azure region. Empty if not region-specific                          |
| `resource_type` | Resource type from the provider namespace                           |
| `resource_id`   | Resource name. Child resources use `/` hierarchy                    |

### Service Namespace Normalization

| Azure Namespace                  | CUID `service`     |
|----------------------------------|---------------------|
| `Microsoft.Compute`              | `compute`           |
| `Microsoft.Storage`              | `storage`           |
| `Microsoft.Network`              | `network`           |
| `Microsoft.Sql`                  | `sql`               |
| `Microsoft.DBforPostgreSQL`      | `postgresql`        |
| `Microsoft.DBforMySQL`           | `mysql`             |
| `Microsoft.DocumentDB`           | `cosmosdb`          |
| `Microsoft.Cache`                | `redis`             |
| `Microsoft.Web`                  | `web`               |
| `Microsoft.ContainerService`     | `aks`               |
| `Microsoft.ContainerRegistry`    | `acr`               |
| `Microsoft.KeyVault`             | `keyvault`          |
| `Microsoft.Authorization`        | `authorization`     |
| `Microsoft.ManagedIdentity`      | `identity`          |
| `Microsoft.Monitor`              | `monitor`           |
| `Microsoft.OperationalInsights`  | `loganalytics`      |
| `Microsoft.EventHub`             | `eventhub`          |
| `Microsoft.ServiceBus`           | `servicebus`        |
| `Microsoft.Logic`                | `logic`             |
| `Microsoft.ApiManagement`        | `apim`              |

## Conversion Rules

### Native → CUID

```
/subscriptions/sub-123/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM
→ cuid:azure:compute:sub-123/myRG:eastus:virtualMachines/myVM

/subscriptions/sub-123/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet
→ cuid:azure:network:sub-123/myRG:eastus:subnets/myVNet/mySubnet

/subscriptions/sub-123/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/myStorage
→ cuid:azure:storage:sub-123/myRG:eastus:storageAccounts/myStorage

/providers/Microsoft.Management/managementGroups/myMG
→ cuid:azure:management:::managementGroups/myMG
```

### CUID → Native

```
cuid:azure:compute:sub-123/myRG:eastus:virtualMachines/myVM
→ /subscriptions/sub-123/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM

cuid:azure:network:sub-123/myRG:eastus:subnets/myVNet/mySubnet
→ /subscriptions/sub-123/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet
```

## Resource Type Catalog

### Compute

| Resource Type        | CUID Example                                                          |
|----------------------|-----------------------------------------------------------------------|
| Virtual Machine      | `cuid:azure:compute:{sub}/{rg}:{region}:virtualMachines/{name}`      |
| VM Scale Set         | `cuid:azure:compute:{sub}/{rg}:{region}:virtualMachineScaleSets/{n}` |
| Availability Set     | `cuid:azure:compute:{sub}/{rg}:{region}:availabilitySets/{name}`     |
| Managed Disk         | `cuid:azure:compute:{sub}/{rg}:{region}:disks/{name}`               |
| Function App         | `cuid:azure:web:{sub}/{rg}:{region}:sites/{name}`                   |
| App Service          | `cuid:azure:web:{sub}/{rg}:{region}:sites/{name}`                   |
| AKS Cluster          | `cuid:azure:aks:{sub}/{rg}:{region}:managedClusters/{name}`         |
| Container Registry   | `cuid:azure:acr:{sub}/{rg}:{region}:registries/{name}`              |
| Container Instance   | `cuid:azure:containerinstance:{sub}/{rg}:{region}:containerGroups/{n}`|

### Storage

| Resource Type        | CUID Example                                                          |
|----------------------|-----------------------------------------------------------------------|
| Storage Account      | `cuid:azure:storage:{sub}/{rg}:{region}:storageAccounts/{name}`      |
| Blob Container       | `cuid:azure:storage:{sub}/{rg}:{region}:blobContainers/{acct}/{name}`|
| File Share           | `cuid:azure:storage:{sub}/{rg}:{region}:fileShares/{acct}/{name}`    |

### Networking

| Resource Type        | CUID Example                                                          |
|----------------------|-----------------------------------------------------------------------|
| Virtual Network      | `cuid:azure:network:{sub}/{rg}:{region}:virtualNetworks/{name}`      |
| Subnet               | `cuid:azure:network:{sub}/{rg}:{region}:subnets/{vnet}/{name}`      |
| Network Interface    | `cuid:azure:network:{sub}/{rg}:{region}:networkInterfaces/{name}`    |
| NSG                  | `cuid:azure:network:{sub}/{rg}:{region}:networkSecurityGroups/{n}`   |
| Public IP            | `cuid:azure:network:{sub}/{rg}:{region}:publicIPAddresses/{name}`   |
| Load Balancer        | `cuid:azure:network:{sub}/{rg}:{region}:loadBalancers/{name}`       |
| Application Gateway  | `cuid:azure:network:{sub}/{rg}:{region}:applicationGateways/{name}` |
| DNS Zone             | `cuid:azure:network:{sub}/{rg}::dnsZones/{name}`                    |

### Identity & Security

| Resource Type        | CUID Example                                                          |
|----------------------|-----------------------------------------------------------------------|
| Key Vault            | `cuid:azure:keyvault:{sub}/{rg}:{region}:vaults/{name}`             |
| Key Vault Secret     | `cuid:azure:keyvault:{sub}/{rg}:{region}:secrets/{vault}/{name}`    |
| Managed Identity     | `cuid:azure:identity:{sub}/{rg}:{region}:userAssignedIdentities/{n}`|
| Role Assignment      | `cuid:azure:authorization:{sub}::roleAssignments/{id}`              |
| Role Definition      | `cuid:azure:authorization:{sub}::roleDefinitions/{id}`              |

### Database

| Resource Type        | CUID Example                                                          |
|----------------------|-----------------------------------------------------------------------|
| SQL Server           | `cuid:azure:sql:{sub}/{rg}:{region}:servers/{name}`                 |
| SQL Database         | `cuid:azure:sql:{sub}/{rg}:{region}:databases/{server}/{name}`      |
| PostgreSQL Server    | `cuid:azure:postgresql:{sub}/{rg}:{region}:servers/{name}`          |
| Cosmos DB Account    | `cuid:azure:cosmosdb:{sub}/{rg}:{region}:databaseAccounts/{name}`   |
| Redis Cache          | `cuid:azure:redis:{sub}/{rg}:{region}:redis/{name}`                 |

### Monitoring

| Resource Type        | CUID Example                                                          |
|----------------------|-----------------------------------------------------------------------|
| Log Analytics WS     | `cuid:azure:loganalytics:{sub}/{rg}:{region}:workspaces/{name}`     |
| App Insights         | `cuid:azure:monitor:{sub}/{rg}:{region}:components/{name}`          |
| Event Hub Namespace  | `cuid:azure:eventhub:{sub}/{rg}:{region}:namespaces/{name}`         |
| Service Bus NS       | `cuid:azure:servicebus:{sub}/{rg}:{region}:namespaces/{name}`       |

## Edge Cases

1. **Child resources** — Subnets, secrets, and databases are children of parent resources. The parent name is included in the resource ID: `subnets/myVNet/mySubnet`.
2. **Tenant-level resources** — Management groups and subscriptions themselves have no subscription prefix. Account field is empty.
3. **Case insensitivity** — Azure resource IDs are case-insensitive. CUIDs normalize to the casing returned by the Azure API.
4. **Resource group in account** — The account field combines subscription and resource group with `/` since both are needed to locate a resource.
5. **Subscription-level resources** — Some resources (policies, locks) exist at subscription level without a resource group. Account field is just `{sub-id}`.
6. **Region** — Azure region is not part of the native resource ID. It must be fetched from the resource metadata or provided explicitly.
