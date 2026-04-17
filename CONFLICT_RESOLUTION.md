# How to Resolve the PR Merge Conflicts

If GitHub says **"This branch has conflicts that must be resolved"**, do this locally.

## 1) Sync and merge target branch

```bash
git checkout <your-branch>
git fetch origin
git merge origin/main
```

Or use the helper script:

```bash
./tools/resolve_conflicts.sh main
```

## 2) Resolve each conflicted file

Git will mark conflict areas like:

```text
<<< HEAD
...your branch...
=== SPLIT ===
...main branch...
>>> origin/main
```

For each conflicted file:
- keep the correct combined content
- remove all marker lines

The current conflict list mentioned by GitHub:
- `IMPLEMENTATION_STATUS.md`
- `backend/.env.example`
- `backend/app/api/v1/ai.py`
- `backend/app/api/v1/analytics.py`
- `backend/app/api/v1/companies.py`
- `backend/app/api/v1/dvr.py`
- `backend/app/api/v1/fleet.py`
- `backend/app/api/v1/fuel.py`
- `backend/app/api/v1/invoices.py`
- `backend/app/api/v1/notifications.py`
- `backend/app/api/v1/shipments.py`
- `backend/app/core/config.py`
- `backend/app/core/dependencies.py`
- `backend/app/schemas/invoice.py`
- `backend/app/services/crud.py`
- `backend/pyproject.toml`
- `docker-compose.yml`

## 3) Verify there are no unresolved markers

```bash
rg -n "^(<<<<<<<|=== SPLIT ===|>>>>>>>)" .
```

If this returns nothing, conflict markers are gone.

## 4) Finalize merge

```bash
git add .
git commit -m "Resolve merge conflicts with main"
git push origin <your-branch>
```

Then GitHub PR should be mergeable.

---

## Common reason this looked like "nothing changed"

You may resolve conflicts in your editor but forget to:
1. `git add` resolved files
2. create the merge commit
3. push the branch

Without those 3 steps, GitHub still shows unresolved conflicts.
