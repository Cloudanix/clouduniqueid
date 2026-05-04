# Bitbucket — CUID URI Specification

## Native Format

Bitbucket identifies resources using **workspace slugs**, **project keys**, and **repository slugs**, plus UUIDs for internal identification.

### Bitbucket Cloud

```
{workspace}/{repo-slug}                          # Repository
{workspace}/{repo-slug}/pull-requests/{id}        # Pull Request
{workspace}/{repo-slug}/issues/{id}               # Issue
{workspace}/{repo-slug}/pipelines/{uuid}          # Pipeline
{workspace}/{repo-slug}/deployments/{uuid}        # Deployment
```

API base: `https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}`

### Bitbucket Data Center (Server)

```
{project-key}/{repo-slug}                         # Repository
{project-key}/{repo-slug}/pull-requests/{id}       # Pull Request
```

API base: `https://{instance}/rest/api/latest/projects/{key}/repos/{slug}`

### Bitbucket Quirks

- Workspaces (Cloud) replaced the older team/user model.
- Every workspace, project, repo, and user has a UUID (e.g., `{a1b2c3d4-...}`).
- Project keys are uppercase short codes (e.g., `PROJ`).
- Repository slugs are lowercase, hyphenated.
- Bitbucket Cloud and Data Center have different API structures.
- Issues are optional per repository (can be disabled).

## CUID Mapping

```
cuid:bitbucket:{service}:{workspace}::{resource-type}/{resource-id}
```

### Field Mapping

| CUID field      | Source                                                        |
|-----------------|---------------------------------------------------------------|
| `provider`      | `bitbucket`                                                   |
| `service`       | Service area (see table below)                                |
| `account`       | Workspace slug (Cloud) or project key (Data Center)           |
| `region`        | Empty for Cloud. For Data Center: instance hostname           |
| `resource_type` | Resource type                                                 |
| `resource_id`   | Slug, key, or numeric ID depending on resource                |

### Service Normalization

| Bitbucket Feature    | CUID `service`  |
|----------------------|-----------------|
| Repositories         | `repos`         |
| Pull Requests        | `pulls`         |
| Issues               | `issues`        |
| Pipelines            | `pipelines`     |
| Deployments          | `deployments`   |
| Projects             | `projects`      |
| Workspaces           | `workspaces`    |
| Snippets             | `snippets`      |
| Downloads            | `downloads`     |

## Conversion Rules

### Native → CUID

```
my-workspace/my-repo (repository)
→ cuid:bitbucket:repos:my-workspace::repository/my-repo

my-workspace/my-repo/pull-requests/42 (pull request)
→ cuid:bitbucket:pulls:my-workspace::pull/my-repo/42

my-workspace/my-repo/issues/7 (issue)
→ cuid:bitbucket:issues:my-workspace::issue/my-repo/7

my-workspace/my-repo/pipelines/{uuid} (pipeline run)
→ cuid:bitbucket:pipelines:my-workspace::pipeline/my-repo/{uuid}

my-workspace (workspace)
→ cuid:bitbucket:workspaces:my-workspace::workspace/my-workspace

my-workspace/MY-PROJECT (project)
→ cuid:bitbucket:projects:my-workspace::project/MY-PROJECT
```

### CUID → Native

```
cuid:bitbucket:repos:my-workspace::repository/my-repo
→ my-workspace/my-repo

cuid:bitbucket:pulls:my-workspace::pull/my-repo/42
→ my-workspace/my-repo/pull-requests/42

cuid:bitbucket:workspaces:my-workspace::workspace/my-workspace
→ my-workspace
```

## Resource Type Catalog

### Source Control

| Resource Type       | CUID Example                                                        |
|---------------------|---------------------------------------------------------------------|
| Repository          | `cuid:bitbucket:repos:{ws}::repository/{repo}`                     |
| Branch              | `cuid:bitbucket:repos:{ws}::branch/{repo}/{branch}`                |
| Tag                 | `cuid:bitbucket:repos:{ws}::tag/{repo}/{tag}`                      |
| Commit              | `cuid:bitbucket:repos:{ws}::commit/{repo}/{sha}`                   |

### Pull Requests & Issues

| Resource Type       | CUID Example                                                        |
|---------------------|---------------------------------------------------------------------|
| Pull Request        | `cuid:bitbucket:pulls:{ws}::pull/{repo}/{id}`                      |
| PR Comment          | `cuid:bitbucket:pulls:{ws}::comment/{repo}/{pr-id}/{comment-id}`   |
| Issue               | `cuid:bitbucket:issues:{ws}::issue/{repo}/{id}`                    |

### CI/CD

| Resource Type       | CUID Example                                                        |
|---------------------|---------------------------------------------------------------------|
| Pipeline            | `cuid:bitbucket:pipelines:{ws}::pipeline/{repo}/{uuid}`            |
| Pipeline Step       | `cuid:bitbucket:pipelines:{ws}::step/{repo}/{pipeline-uuid}/{uuid}`|
| Deployment          | `cuid:bitbucket:deployments:{ws}::deployment/{repo}/{uuid}`        |
| Environment         | `cuid:bitbucket:deployments:{ws}::environment/{repo}/{uuid}`       |

### Organization

| Resource Type       | CUID Example                                                        |
|---------------------|---------------------------------------------------------------------|
| Workspace           | `cuid:bitbucket:workspaces:{ws}::workspace/{ws}`                   |
| Project             | `cuid:bitbucket:projects:{ws}::project/{key}`                      |
| Workspace Member    | `cuid:bitbucket:workspaces:{ws}::member/{username}`                |
| Group Permission    | `cuid:bitbucket:repos:{ws}::group-permission/{repo}/{group}`       |

### Other

| Resource Type       | CUID Example                                                        |
|---------------------|---------------------------------------------------------------------|
| Snippet             | `cuid:bitbucket:snippets:{ws}::snippet/{id}`                       |
| Download            | `cuid:bitbucket:downloads:{ws}::download/{repo}/{filename}`        |
| SSH Key             | `cuid:bitbucket:repos:{ws}::ssh-key/{repo}/{key-id}`              |
| Webhook             | `cuid:bitbucket:repos:{ws}::webhook/{repo}/{uuid}`                |

## Edge Cases

1. **Cloud vs Data Center** — For Bitbucket Data Center, the region field contains the instance hostname: `cuid:bitbucket:repos:MY-PROJECT:bitbucket.company.com:repository/my-repo`. The account field uses the project key instead of workspace slug.
2. **UUIDs vs slugs** — Bitbucket assigns UUIDs to all entities, but CUIDs use human-readable slugs for repositories and workspaces. UUIDs are used only for resources that lack stable slugs (pipelines, deployments).
3. **Project keys** — Project keys are uppercase (e.g., `PROJ`). They are preserved as-is in the resource_id.
4. **Personal repositories** — Repos under a personal workspace use the username as the workspace slug.
5. **Disabled features** — Issues and wikis can be disabled per repo. The CUID format is the same regardless; the resource simply won't exist.
6. **Renamed workspaces** — Workspace slugs can change. CUIDs track the current slug. Old CUIDs become stale.
