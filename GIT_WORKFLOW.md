# Suggested Git workflow (delete this file before final submission if you like)

Work through these in order, committing after each step so your history shows real progress.

```
git init
git branch -M main
git remote add origin <your-repo-url>
```

1. Project setup:      `git add .gitignore requirements.txt app.py`  -> `git commit -m "Set up project with Flask entry point and gitignore"`
2. Database layer:     `git add campus/__init__.py campus/db.py`      -> `git commit -m "Add app factory and SQLite schema"`
3. Base templates:     `git add templates/base.html templates/index.html static/` -> `git commit -m "Add base layout, dashboard and styling"`
4. Push main:          `git push -u origin main`

Then one feature per branch:

```
git checkout -b feature/students
# add campus/validators.py (student part), campus/views.py, templates/students.html
git add . && git commit -m "Add student management with validation"
git checkout main && git merge feature/students --no-ff
git push
```

Repeat for `feature/attendance`, `feature/room-booking`, `feature/notices`, then:

- `git commit -m "Add automated tests"`        (tests/)
- `git commit -m "Add README documentation"`   (README.md)

Check your history with `git log --oneline --graph` and screenshot it, together with the merged branches.
