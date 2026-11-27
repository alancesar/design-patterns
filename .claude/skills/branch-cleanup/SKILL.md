---
name: branch-cleanup
description: Updates the default branch and deletes, locally and on the remote, the branches whose pull request was merged or that the default branch already contains. Use when the user says a PR was merged, asks to clean up or delete branches, or calls /branch-cleanup.
---

# Branch cleanup

Updates the default branch and removes the branches that already reached it, both locally and on `origin`. Never delete the default branch, a branch with an open pull request, or work that isn't on the default branch, unless the user confirms.

## 1. Pre-checks

1. Find the default branch: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` (fall back to `git symbolic-ref --short refs/remotes/origin/HEAD`, minus the `origin/` prefix). Below, `<default>` is that branch.
2. Run `git status --porcelain`. If there are uncommitted changes to tracked files, stop and ask the user what to do. Don't stash, reset or check out on your own. Files ignored through `.gitignore` or `.git/info/exclude` don't show up and don't block.
3. If the user mentioned a pull request, confirm with `gh pr view <n> --json state,mergedAt` that it is `MERGED`. If it isn't, say so and stop.

## 2. Update the default branch

```bash
git switch <default>
git pull --ff-only
git fetch --prune
```

If `pull --ff-only` fails, the local `<default>` has diverged from `origin`. Stop and show `git log --oneline <default>...origin/<default>`. Don't rebase or reset without the user's approval.

## 3. Classify each branch

List local branches with `git branch -vv` and remote ones with `git branch -r`. Skip `<default>`, `origin/HEAD` and any branch checked out in a worktree (`git worktree list`).

For each branch, look up its pull request with `gh pr list --head <branch> --state all --json number,state,url,headRefOid` and classify it:

| Situation | Action |
| --- | --- |
| PR `MERGED`, or branch contained in `<default>` (`git merge-base --is-ancestor <branch> <default>`) | **delete**, local and remote |
| PR `OPEN` | **keep** |
| PR `CLOSED` without merge, or no PR and commits not in `<default>` | **ask** |
| Local branch whose upstream is `[gone]`, with no PR and commits not in `<default>` | **ask** |

Squash and rebase merges leave the branch outside `<default>`'s history, so the pull request's state is the main criterion, not `git branch --merged`.

Before deleting a branch whose PR is `MERGED`, make sure it didn't get commits after the merge: compare `git rev-parse <branch>` with the PR's `headRefOid`. If they differ, move the branch to **ask**.

Without `gh` (or for a remote that isn't on GitHub), use only the ancestry check, and move every branch that isn't contained in `<default>` to **ask**.

## 4. Delete

- **delete** branches:
  - local: `git branch -d <branch>`. If `-d` refuses because of a squash or rebase merge, and the PR is `MERGED` with the same `headRefOid`, use `git branch -D <branch>`;
  - remote, if it still exists: `git push origin --delete <branch>`.
- **ask** branches: use AskUserQuestion with one item per branch, showing its last commit (`git log -1 --oneline <branch>`), the PR state and how many commits aren't in `<default>` (`git rev-list --count <default>..<branch>`). Recommend keeping it. Delete only what the user picks.
- Then run `git fetch --prune`.

Don't delete branches in other repositories or forks, and don't close pull requests.

## 5. Report

Show the final state (`git branch -a` and `git status -sb`) and report in a few lines:

- the commit `<default>` is now at;
- the branches deleted, local and remote;
- the branches kept and why (open PR, the user's answer, worktree).
