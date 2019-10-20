# Reset files from staging
git checkout HEAD -- <files>

# Undo a public commit with git revert
git revert <SHA_ID>

# Undo a commit with git reset
git reset --hard <SHA_ID>

# Undoing the last commit
git add .
git commit --amend -m""

# Archive git repository as zip file
git archive --format zip --output /full/path/to/zipfile.zip master

# Rebase
git rebase <branch name to be rebased on>
git rebase --continue
git rebase --abort