# GitLab — CUID URI Specification

## Native Format

GitLab identifies resources using **namespace paths** and **numeric IDs**:

- Projects: `gitlab-org/gitlab` (path) + numeric project ID (`278964`)
- Groups: `gitlab-org` (path) + numeric group ID (`9970`)
- Users: `username` + numeric user ID
- Issues: `gitlab-org/gitlab#1234` or `gitlab-org/gitlab/-/issues/1234`
- Merge Requests: `gitlab-org/gitlab/-/merge_requests/5678`

### API Paths

```
/api/v4/projects/:id
/api/v4/groups/:id
/api/v4/users/:id
/api/v4/projects/:id/issues/:iid
/api/v4/projects/:id/merge_requests/:iid
/api/v4/projects/:id/pipelines/:id
```

### GitLab Quirks

- Namespaces can be deeply nested: `group/subgroup/subsubgroup/project`.
- Both `.com` (SaaS) and self-managed instances exist.
- Issues and MRs use project-scoped IIDs (internal IDs), not global IDs.
- The `/-/` separator in web URLs distinguishes routes from namespace paths.
- Projects can be transferred between namespaces, changing their path.

## CUID Mapping

```
gitlab:{service}:{namespace}:{instance}:{resource-type}/{resource-id}
```

### Field Mapping

| CUID field      | Source                                                        |
|-----------------|---------------------------------------------------------------|
| `provider`      | `gitlab`                                                      |
| `service`       | Service area (see table below)                                |
| `account`       | Top-level namespace (group or user)                           |
| `region`        | Empty for gitlab.com. For self-managed: instance hostname     |
| `resource_type` | Resource type                                                 |
| `resource_id`   | Path, name, or IID depending on resource                      |

### Service Normalization

| GitLab Feature       | CUID `service`  |
|----------------------|-----------------|
| Projects             | `projects`      |
| Issues               | `issues`        |
| Merge Requests       | `merges`        |
| Pipelines / CI       | `ci`            |
| Environments         | `environments`  |
| Packages / Registry  | `packages`      |
| Container Registry   | `registry`      |
| Groups               | `groups`        |
| Users                | `users`         |
| Snippets             | `snippets`      |
| Releases             | `releases`      |
| Wiki                 | `wiki`          |
| Security             | `security`      |

## Conversion Rules

### Native → CUID

```
gitlab-org/gitlab (project)
→ gitlab:projects:gitlab-org::project/gitlab

gitlab-org/gitlab/-/issues/1234 (issue)
→ gitlab:issues:gitlab-org::issue/gitlab/1234

gitlab-org/gitlab/-/merge_requests/5678 (merge request)
→ gitlab:merges:gitlab-org::merge-request/gitlab/5678

gitlab-org/gitlab/-/pipelines/99999 (pipeline)
→ gitlab:ci:gitlab-org::pipeline/gitlab/99999

gitlab-org (group)
→ gitlab:groups:gitlab-org::group/gitlab-org

gitlab-org/subgroup (subgroup)
→ gitlab:groups:gitlab-org::group/gitlab-org/subgroup

john (user)
→ gitlab:users:john::user/john
```

### Self-Managed Instance

```
my-group/my-project (on gitlab.company.com)
→ gitlab:projects:my-group:gitlab.company.com:project/my-project
```

### CUID → Native

```
gitlab:projects:gitlab-org::project/gitlab
→ gitlab-org/gitlab

gitlab:issues:gitlab-org::issue/gitlab/1234
→ gitlab-org/gitlab/-/issues/1234

gitlab:merges:gitlab-org::merge-request/gitlab/5678
→ gitlab-org/gitlab/-/merge_requests/5678
```

## Resource Type Catalog

### Source Control

| Resource Type       | CUID Example                                                       |
|---------------------|--------------------------------------------------------------------|
| Project             | `gitlab:projects:{ns}::project/{project}`                    |
| Branch              | `gitlab:projects:{ns}::branch/{project}/{branch}`            |
| Tag                 | `gitlab:projects:{ns}::tag/{project}/{tag}`                  |
| Commit              | `gitlab:projects:{ns}::commit/{project}/{sha}`               |
| Release             | `gitlab:releases:{ns}::release/{project}/{tag}`              |

### Issues & Merge Requests

| Resource Type       | CUID Example                                                       |
|---------------------|--------------------------------------------------------------------|
| Issue               | `gitlab:issues:{ns}::issue/{project}/{iid}`                  |
| Merge Request       | `gitlab:merges:{ns}::merge-request/{project}/{iid}`          |
| Issue Note          | `gitlab:issues:{ns}::note/{project}/{issue-iid}/{note-id}`   |
| MR Note             | `gitlab:merges:{ns}::note/{project}/{mr-iid}/{note-id}`      |
| Milestone           | `gitlab:projects:{ns}::milestone/{project}/{id}`             |
| Label               | `gitlab:projects:{ns}::label/{project}/{id}`                 |

### CI/CD

| Resource Type       | CUID Example                                                       |
|---------------------|--------------------------------------------------------------------|
| Pipeline            | `gitlab:ci:{ns}::pipeline/{project}/{id}`                    |
| Job                 | `gitlab:ci:{ns}::job/{project}/{id}`                         |
| Schedule            | `gitlab:ci:{ns}::schedule/{project}/{id}`                    |
| Environment         | `gitlab:environments:{ns}::environment/{project}/{name}`     |
| Runner (project)    | `gitlab:ci:{ns}::runner/{project}/{id}`                      |
| Runner (instance)   | `gitlab:ci:::runner/{id}`                                    |
| Variable (project)  | `gitlab:ci:{ns}::variable/{project}/{key}`                   |
| Variable (group)    | `gitlab:ci:{ns}::group-variable/{key}`                       |

### Packages & Registry

| Resource Type       | CUID Example                                                       |
|---------------------|--------------------------------------------------------------------|
| Package             | `gitlab:packages:{ns}::package/{project}/{id}`               |
| Container Image     | `gitlab:registry:{ns}::image/{project}/{name}`               |
| Container Tag       | `gitlab:registry:{ns}::tag/{project}/{image}/{tag}`          |

### Organization & Access

| Resource Type       | CUID Example                                                       |
|---------------------|--------------------------------------------------------------------|
| Group               | `gitlab:groups:{ns}::group/{path}`                           |
| Subgroup            | `gitlab:groups:{ns}::group/{parent}/{child}`                 |
| User                | `gitlab:users:{user}::user/{user}`                           |
| Group Member        | `gitlab:groups:{ns}::member/{group}/{user-id}`               |
| Deploy Key          | `gitlab:projects:{ns}::deploy-key/{project}/{id}`            |
| Deploy Token        | `gitlab:projects:{ns}::deploy-token/{project}/{id}`          |

### Security

| Resource Type       | CUID Example                                                       |
|---------------------|--------------------------------------------------------------------|
| Vulnerability       | `gitlab:security:{ns}::vulnerability/{project}/{id}`         |
| SAST Finding        | `gitlab:security:{ns}::sast/{project}/{id}`                  |
| Dependency Scan     | `gitlab:security:{ns}::dependency-scan/{project}/{id}`       |

## Edge Cases

1. **Nested namespaces** — GitLab supports deeply nested groups (`a/b/c/d/project`). The account field uses only the top-level namespace. The full subgroup path is part of the resource_id: `gitlab:projects:a::project/b/c/d/project`.
2. **Self-managed instances** — The region field contains the hostname: `gitlab:projects:mygroup:gitlab.company.com:project/myrepo`. For gitlab.com, region is empty.
3. **IIDs vs global IDs** — Issues and MRs use project-scoped IIDs in CUIDs (matching what users see in the UI), not global database IDs.
4. **Project transfers** — When a project is transferred to a new namespace, its CUID changes. The old CUID becomes stale.
5. **Personal namespaces** — User-owned projects use the username as the namespace: `gitlab:projects:john::project/my-project`.
6. **Forked projects** — Forks are separate projects under the fork owner's namespace with their own CUID.
