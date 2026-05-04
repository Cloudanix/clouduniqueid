# GitHub — CUID URI Specification

## Native Format

GitHub identifies resources using a combination of **slug paths** and **numeric IDs**:

- Organizations: `facebook` (slug), `123456` (numeric ID)
- Repositories: `facebook/react` (owner/repo slug), `10270250` (numeric ID)
- Issues/PRs: `facebook/react#1234` (share a numeric namespace per repo)
- Users: `octocat` (username), `583231` (numeric ID)
- GraphQL Node IDs: Base64-encoded global IDs (e.g., `MDQ6VXNlcjU4MzIzMQ==`)

### API Paths

```
/repos/{owner}/{repo}
/orgs/{org}
/users/{user}
/repos/{owner}/{repo}/issues/{number}
/repos/{owner}/{repo}/pulls/{number}
/repos/{owner}/{repo}/actions/workflows/{workflow_id}
```

### GitHub Quirks

- Usernames and org names share a namespace — no two can collide.
- Issues and PRs share a numeric sequence per repository.
- Repository names are case-insensitive but case-preserving.
- GitHub Enterprise Server uses custom domains.
- Forks are separate repositories with their own owner/repo path.

## CUID Mapping

```
cuid:github:{service}:{owner}::{resource-type}/{resource-id}
```

### Field Mapping

| CUID field      | Source                                                        |
|-----------------|---------------------------------------------------------------|
| `provider`      | `github`                                                      |
| `service`       | Service area (see table below)                                |
| `account`       | Owner (org or user). For user-level resources: the username   |
| `region`        | Always empty (GitHub is global). For GHES: instance hostname  |
| `resource_type` | Resource type                                                 |
| `resource_id`   | Slug, name, or number depending on resource                   |

### Service Normalization

| GitHub Feature       | CUID `service` |
|----------------------|----------------|
| Repositories         | `repos`        |
| Issues               | `issues`       |
| Pull Requests        | `pulls`        |
| Actions / Workflows  | `actions`      |
| Packages             | `packages`     |
| Security / Advisories| `security`     |
| Organizations        | `orgs`         |
| Users                | `users`        |
| Teams                | `teams`        |
| Projects (classic)   | `projects`     |
| Environments         | `environments` |
| Secrets              | `secrets`      |
| Releases             | `releases`     |

## Conversion Rules

### Native → CUID

```
facebook/react (repository)
→ cuid:github:repos:facebook::repository/react

facebook/react#1234 (issue)
→ cuid:github:issues:facebook::issue/react/1234

facebook/react#5678 (pull request)
→ cuid:github:pulls:facebook::pull/react/5678

octocat (user)
→ cuid:github:users:octocat::user/octocat

facebook (organization)
→ cuid:github:orgs:facebook::org/facebook

facebook/react/.github/workflows/ci.yml (workflow)
→ cuid:github:actions:facebook::workflow/react/ci.yml

facebook/react/environments/production (environment)
→ cuid:github:environments:facebook::environment/react/production
```

### CUID → Native

```
cuid:github:repos:facebook::repository/react
→ facebook/react

cuid:github:issues:facebook::issue/react/1234
→ facebook/react#1234

cuid:github:users:octocat::user/octocat
→ octocat
```

## Resource Type Catalog

### Source Control

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Repository          | `cuid:github:repos:{owner}::repository/{repo}`                  |
| Branch              | `cuid:github:repos:{owner}::branch/{repo}/{branch}`             |
| Tag                 | `cuid:github:repos:{owner}::tag/{repo}/{tag}`                   |
| Commit              | `cuid:github:repos:{owner}::commit/{repo}/{sha}`                |
| Release             | `cuid:github:releases:{owner}::release/{repo}/{tag}`            |

### Issues & PRs

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Issue               | `cuid:github:issues:{owner}::issue/{repo}/{number}`             |
| Pull Request        | `cuid:github:pulls:{owner}::pull/{repo}/{number}`               |
| Comment (issue)     | `cuid:github:issues:{owner}::comment/{repo}/{comment-id}`       |
| Review (PR)         | `cuid:github:pulls:{owner}::review/{repo}/{pr}/{review-id}`     |

### CI/CD

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Workflow            | `cuid:github:actions:{owner}::workflow/{repo}/{filename}`        |
| Workflow Run        | `cuid:github:actions:{owner}::run/{repo}/{run-id}`              |
| Job                 | `cuid:github:actions:{owner}::job/{repo}/{job-id}`              |
| Artifact            | `cuid:github:actions:{owner}::artifact/{repo}/{artifact-id}`    |
| Environment         | `cuid:github:environments:{owner}::environment/{repo}/{name}`   |
| Secret (repo)       | `cuid:github:secrets:{owner}::secret/{repo}/{name}`             |
| Secret (org)        | `cuid:github:secrets:{owner}::org-secret/{name}`                |

### Organization & Access

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Organization        | `cuid:github:orgs:{owner}::org/{name}`                          |
| User                | `cuid:github:users:{user}::user/{user}`                         |
| Team                | `cuid:github:teams:{org}::team/{team-slug}`                     |
| App Installation    | `cuid:github:apps:{owner}::installation/{installation-id}`      |

### Packages & Security

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Package             | `cuid:github:packages:{owner}::package/{type}/{name}`           |
| Package Version     | `cuid:github:packages:{owner}::version/{type}/{name}/{version}` |
| Advisory            | `cuid:github:security:{owner}::advisory/{repo}/{ghsa-id}`       |
| Dependabot Alert    | `cuid:github:security:{owner}::dependabot/{repo}/{number}`      |
| Code Scanning Alert | `cuid:github:security:{owner}::code-scanning/{repo}/{number}`   |

## Edge Cases

1. **Issues vs PRs** — GitHub uses the same numeric sequence for both. The CUID distinguishes them via `service` (`issues` vs `pulls`) and `resource_type` (`issue` vs `pull`).
2. **GitHub Enterprise Server** — For GHES instances, the region field contains the hostname: `cuid:github:repos:myorg:ghes.company.com:repository/myrepo`.
3. **Forks** — A fork is a separate repository under the fork owner: `cuid:github:repos:my-fork-owner::repository/react`.
4. **Renamed repos/users** — GitHub redirects old names, but the CUID uses the current canonical name. CUIDs change when resources are renamed.
5. **Nested orgs** — GitHub does not support nested organizations. The owner is always a single-level slug.
6. **GraphQL Node IDs** — Not used in CUIDs. CUIDs use human-readable slugs for portability and readability.
