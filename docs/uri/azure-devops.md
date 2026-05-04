# Azure DevOps — CUID URI Specification

## Native Format

Azure DevOps identifies resources using **organization/project** hierarchy with a mix of **GUIDs** and **numeric IDs**:

### URL Patterns

```
https://dev.azure.com/{org}/{project}                           # Project
https://dev.azure.com/{org}/{project}/_git/{repo}               # Repository
https://dev.azure.com/{org}/{project}/_build?definitionId={id}  # Pipeline
https://dev.azure.com/{org}/{project}/_workitems/edit/{id}      # Work Item
https://dev.azure.com/{org}/{project}/_environments/{id}        # Environment
https://dev.azure.com/{org}/{project}/_artifacts/feed/{name}    # Artifact Feed
```

### Legacy URL Format

```
https://{org}.visualstudio.com/{project}/...
```

### API Paths

```
https://dev.azure.com/{org}/_apis/projects/{project-id}
https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repo-id}
https://dev.azure.com/{org}/{project}/_apis/build/definitions/{id}
https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{id}
https://dev.azure.com/{org}/{project}/_apis/pipelines/{id}
```

### Azure DevOps Quirks

- Organizations are globally unique names under `dev.azure.com`.
- Projects have both a name (display) and a GUID.
- Repositories have both a name and a GUID.
- Work items use sequential numeric IDs scoped to the organization (not project).
- Pipelines (build definitions) use numeric IDs scoped to the project.
- The legacy `{org}.visualstudio.com` format is still supported.
- Azure DevOps Server (on-premises) uses custom hostnames.

## CUID Mapping

```
azuredevops:{service}:{org}/{project}::{resource-type}/{resource-id}
```

### Field Mapping

| CUID field      | Source                                                        |
|-----------------|---------------------------------------------------------------|
| `provider`      | `azuredevops`                                                 |
| `service`       | Service area (see table below)                                |
| `account`       | `{org}/{project}`. For org-level resources: just `{org}`      |
| `region`        | Empty for Azure DevOps Services. For Server: instance hostname|
| `resource_type` | Resource type                                                 |
| `resource_id`   | Name, numeric ID, or GUID depending on resource               |

### Service Normalization

| Azure DevOps Feature | CUID `service`  |
|----------------------|-----------------|
| Repositories (Git)   | `repos`         |
| Pipelines / Builds   | `pipelines`     |
| Releases             | `releases`      |
| Work Items           | `boards`        |
| Boards               | `boards`        |
| Test Plans           | `test`          |
| Artifacts / Feeds    | `artifacts`     |
| Environments         | `environments`  |
| Projects             | `projects`      |
| Organizations        | `orgs`          |
| Wiki                 | `wiki`          |
| Service Connections  | `connections`   |

## Conversion Rules

### Native → CUID

```
dev.azure.com/my-org/my-project (project)
→ azuredevops:projects:my-org::project/my-project

dev.azure.com/my-org/my-project/_git/my-repo (repository)
→ azuredevops:repos:my-org/my-project::repository/my-repo

dev.azure.com/my-org/my-project/_build?definitionId=42 (pipeline)
→ azuredevops:pipelines:my-org/my-project::pipeline/42

dev.azure.com/my-org/my-project/_workitems/edit/1234 (work item)
→ azuredevops:boards:my-org/my-project::work-item/1234

dev.azure.com/my-org/my-project/_environments/5 (environment)
→ azuredevops:environments:my-org/my-project::environment/5

dev.azure.com/my-org/my-project/_artifacts/feed/my-feed (artifact feed)
→ azuredevops:artifacts:my-org/my-project::feed/my-feed

my-org (organization)
→ azuredevops:orgs:my-org::org/my-org
```

### Azure DevOps Server (On-Premises)

```
tfs.company.com/my-collection/my-project/_git/my-repo
→ azuredevops:repos:my-collection/my-project:tfs.company.com:repository/my-repo
```

### CUID → Native

```
azuredevops:repos:my-org/my-project::repository/my-repo
→ https://dev.azure.com/my-org/my-project/_git/my-repo

azuredevops:pipelines:my-org/my-project::pipeline/42
→ https://dev.azure.com/my-org/my-project/_build?definitionId=42

azuredevops:boards:my-org/my-project::work-item/1234
→ https://dev.azure.com/my-org/my-project/_workitems/edit/1234
```

## Resource Type Catalog

### Source Control

| Resource Type       | CUID Example                                                            |
|---------------------|-------------------------------------------------------------------------|
| Repository          | `azuredevops:repos:{org}/{proj}::repository/{name}`               |
| Branch              | `azuredevops:repos:{org}/{proj}::branch/{repo}/{branch}`          |
| Tag                 | `azuredevops:repos:{org}/{proj}::tag/{repo}/{tag}`                |
| Commit              | `azuredevops:repos:{org}/{proj}::commit/{repo}/{sha}`             |
| Pull Request        | `azuredevops:repos:{org}/{proj}::pull-request/{repo}/{id}`        |
| PR Thread           | `azuredevops:repos:{org}/{proj}::thread/{repo}/{pr-id}/{id}`      |

### Pipelines & CI/CD

| Resource Type       | CUID Example                                                            |
|---------------------|-------------------------------------------------------------------------|
| Pipeline (def)      | `azuredevops:pipelines:{org}/{proj}::pipeline/{id}`               |
| Pipeline Run        | `azuredevops:pipelines:{org}/{proj}::run/{pipeline-id}/{run-id}`  |
| Release Definition  | `azuredevops:releases:{org}/{proj}::release-def/{id}`             |
| Release             | `azuredevops:releases:{org}/{proj}::release/{def-id}/{id}`        |
| Environment         | `azuredevops:environments:{org}/{proj}::environment/{id}`         |
| Variable Group      | `azuredevops:pipelines:{org}/{proj}::variable-group/{id}`         |
| Service Connection  | `azuredevops:connections:{org}/{proj}::service-connection/{id}`   |

### Work Tracking

| Resource Type       | CUID Example                                                            |
|---------------------|-------------------------------------------------------------------------|
| Work Item           | `azuredevops:boards:{org}/{proj}::work-item/{id}`                 |
| Board               | `azuredevops:boards:{org}/{proj}::board/{name}`                   |
| Sprint / Iteration  | `azuredevops:boards:{org}/{proj}::iteration/{path}`               |
| Area                | `azuredevops:boards:{org}/{proj}::area/{path}`                    |
| Query               | `azuredevops:boards:{org}/{proj}::query/{id}`                     |

### Artifacts

| Resource Type       | CUID Example                                                            |
|---------------------|-------------------------------------------------------------------------|
| Feed                | `azuredevops:artifacts:{org}/{proj}::feed/{name}`                 |
| Package             | `azuredevops:artifacts:{org}/{proj}::package/{feed}/{name}`       |
| Package Version     | `azuredevops:artifacts:{org}/{proj}::version/{feed}/{pkg}/{ver}`  |

### Organization

| Resource Type       | CUID Example                                                            |
|---------------------|-------------------------------------------------------------------------|
| Organization        | `azuredevops:orgs:{org}::org/{org}`                               |
| Project             | `azuredevops:projects:{org}::project/{name}`                      |
| Team                | `azuredevops:projects:{org}/{proj}::team/{name}`                  |
| Wiki                | `azuredevops:wiki:{org}/{proj}::wiki/{name}`                      |

### Test

| Resource Type       | CUID Example                                                            |
|---------------------|-------------------------------------------------------------------------|
| Test Plan           | `azuredevops:test:{org}/{proj}::test-plan/{id}`                   |
| Test Suite          | `azuredevops:test:{org}/{proj}::test-suite/{plan-id}/{id}`        |
| Test Case           | `azuredevops:test:{org}/{proj}::test-case/{id}`                   |

## Edge Cases

1. **Work item IDs are org-scoped** — Work item IDs are unique across the entire organization, not per project. The project in the CUID indicates where the work item is displayed, but the ID is globally unique within the org.
2. **Azure DevOps Server** — For on-premises instances, the region field contains the hostname. The account field uses `{collection}/{project}` instead of `{org}/{project}`.
3. **Legacy URLs** — `{org}.visualstudio.com` URLs map to the same CUIDs as `dev.azure.com/{org}`. The CUID is canonical regardless of URL format.
4. **TFVC repositories** — Azure DevOps supports TFVC (centralized VCS) alongside Git. TFVC repos use `$/project` paths. CUID: `azuredevops:repos:{org}/{proj}::tfvc-path/{path}`.
5. **Project renames** — Project names can change. CUIDs track the current name. GUIDs are available via the API but not used in CUIDs for readability.
6. **Cross-project references** — Work items can reference items in other projects. Each work item's CUID uses its own project context.
