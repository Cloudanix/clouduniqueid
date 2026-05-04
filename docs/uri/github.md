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
github:{service}:{owner}::{resource-type}/{resource-id}
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
→ github:repos:facebook::repository/react

facebook/react#1234 (issue)
→ github:issues:facebook::issue/react/1234

facebook/react#5678 (pull request)
→ github:pulls:facebook::pull/react/5678

octocat (user)
→ github:users:octocat::user/octocat

facebook (organization)
→ github:orgs:facebook::org/facebook

facebook/react/.github/workflows/ci.yml (workflow)
→ github:actions:facebook::workflow/react/ci.yml

facebook/react/environments/production (environment)
→ github:environments:facebook::environment/react/production
```

### CUID → Native

```
github:repos:facebook::repository/react
→ facebook/react

github:issues:facebook::issue/react/1234
→ facebook/react#1234

github:users:octocat::user/octocat
→ octocat
```

## Resource Type Catalog

### Source Control

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Repository          | `github:repos:{owner}::repository/{repo}`                  |
| Branch              | `github:repos:{owner}::branch/{repo}/{branch}`             |
| Tag                 | `github:repos:{owner}::tag/{repo}/{tag}`                   |
| Commit              | `github:repos:{owner}::commit/{repo}/{sha}`                |
| Release             | `github:releases:{owner}::release/{repo}/{tag}`            |

### Issues & PRs

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Issue               | `github:issues:{owner}::issue/{repo}/{number}`             |
| Pull Request        | `github:pulls:{owner}::pull/{repo}/{number}`               |
| Comment (issue)     | `github:issues:{owner}::comment/{repo}/{comment-id}`       |
| Review (PR)         | `github:pulls:{owner}::review/{repo}/{pr}/{review-id}`     |

### CI/CD

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Workflow            | `github:actions:{owner}::workflow/{repo}/{filename}`        |
| Workflow Run        | `github:actions:{owner}::run/{repo}/{run-id}`              |
| Job                 | `github:actions:{owner}::job/{repo}/{job-id}`              |
| Artifact            | `github:actions:{owner}::artifact/{repo}/{artifact-id}`    |
| Environment         | `github:environments:{owner}::environment/{repo}/{name}`   |
| Secret (repo)       | `github:secrets:{owner}::secret/{repo}/{name}`             |
| Secret (org)        | `github:secrets:{owner}::org-secret/{name}`                |

### Organization & Access

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Organization        | `github:orgs:{owner}::org/{name}`                          |
| User                | `github:users:{user}::user/{user}`                         |
| Team                | `github:teams:{org}::team/{team-slug}`                     |
| App Installation    | `github:apps:{owner}::installation/{installation-id}`      |

### Packages & Security

| Resource Type       | CUID Example                                                     |
|---------------------|------------------------------------------------------------------|
| Package             | `github:packages:{owner}::package/{type}/{name}`           |
| Package Version     | `github:packages:{owner}::version/{type}/{name}/{version}` |
| Advisory            | `github:security:{owner}::advisory/{repo}/{ghsa-id}`       |
| Dependabot Alert    | `github:security:{owner}::dependabot/{repo}/{number}`      |
| Code Scanning Alert | `github:security:{owner}::code-scanning/{repo}/{number}`   |

## Edge Cases

1. **Issues vs PRs** — GitHub uses the same numeric sequence for both. The CUID distinguishes them via `service` (`issues` vs `pulls`) and `resource_type` (`issue` vs `pull`).
2. **GitHub Enterprise Server** — For GHES instances, the region field contains the hostname: `github:repos:myorg:ghes.company.com:repository/myrepo`.
3. **Forks** — A fork is a separate repository under the fork owner: `github:repos:my-fork-owner::repository/react`.
4. **Renamed repos/users** — GitHub redirects old names, but the CUID uses the current canonical name. CUIDs change when resources are renamed.
5. **Nested orgs** — GitHub does not support nested organizations. The owner is always a single-level slug.
6. **GraphQL Node IDs** — Not used in CUIDs. CUIDs use human-readable slugs for portability and readability.
