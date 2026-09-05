# STUDY HUB

A premium programming-education platform built with Flask, SQLite, and vanilla
HTML/CSS/JS. Learn Python, C, C++, Java, JavaScript, HTML, CSS, SQL, PHP,
Data Structures, and Algorithms — beginner to advanced — with lessons, quizzes,
a student dashboard, and certificates.

## 1. Open the project

Unzip this folder and open it in VS Code:

```
File → Open Folder... → studyhub
```

## 2. Install Python dependencies

Open a terminal in VS Code (``Ctrl+` ``) and run:

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

## 3. Create the database and load course content

This creates `studyhub.db`, one admin account, one demo student account, and
all 11 courses with lessons and quizzes:

```bash
python seed.py
```

You'll see something like:

```
Created admin account -> username: admin / password: admin123
Created demo student -> username: demo / password: demo1234
STUDY HUB seed data loaded successfully.
```

**Change the admin password** before using this anywhere but your own machine
— open `seed.py` and edit the `seed_accounts()` function, or add your own
admin directly in a Python shell.

## 4. Run the app

```bash
python app.py
```

Visit **http://127.0.0.1:5000** in your browser.

- Student site: sign up at `/signup`, or log in with the demo account
  (`demo` / `demo1234`).
- Admin panel: go to `/admin/login` and log in with `admin` / `admin123`.
  There is no admin sign-up page anywhere, by design — only login.

## What's included

- Full student flow: sign up, log in, browse 11 courses, read lessons, mark
  lessons complete, take chapter quizzes and final exams, earn certificates,
  view a personal dashboard.
- Full admin flow: dashboard with platform stats, student list + search +
  per-student progress, course/chapter/lesson CRUD, quiz/question CRUD.
- Dark and light mode (saved per browser), fully responsive layout with a
  mobile nav, copy-to-clipboard code blocks, and a printable certificate page.
- **Python** has a complete beginner → intermediate → advanced path (16
  lessons across 5 chapters) to show the full depth the system supports.
  The other 10 courses currently ship with a solid beginner chapter (5
  lessons each) plus a final exam, so every course is usable and can earn a
  certificate today. Use the admin panel (or extend `seed.py`) to add more
  intermediate/advanced chapters to any course — the system fully supports it.

## Project structure

```
studyhub/
├── app.py              # Flask app & all routes
├── models.py            # SQLAlchemy models
├── extensions.py         # db + login_manager instances
├── seed.py               # populates the database with course content
├── requirements.txt
├── studyhub.db           # SQLite database (created by seed.py)
├── templates/
│   ├── base.html, index.html, courses.html, course.html, ...
│   └── admin/             # admin-only templates
└── static/
    ├── css/style.css
    └── js/script.js
```

## Notes

- Passwords are hashed with Werkzeug's `generate_password_hash` — never
  stored in plain text.
- Admin and student sessions are kept separate; each role is blocked from
  the other's pages at the route level.
- To reset all data, stop the server, delete `studyhub.db`, and run
  `python seed.py` again.
