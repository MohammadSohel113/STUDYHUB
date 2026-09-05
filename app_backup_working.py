from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from lesson_data import LESSON_CONTENT


app = Flask(__name__)
app.secret_key = "studyhub-secret-key-change-later"

DB = "studyhub.db"


# =========================================================
# LANGUAGES
# =========================================================

LANGUAGES = [
    ("Python", "🐍", "Learn Python from basics to advanced.", "python"),
    ("C", "⚙️", "Build strong programming fundamentals with C.", "c"),
    ("C++", "🚀", "Master C++ and object-oriented programming.", "cpp"),
    ("Java", "☕", "Learn Java, OOP and application development.", "java"),
    ("JavaScript", "🌐", "Learn modern JavaScript for web development.", "javascript"),
    ("SQL", "🗄️", "Learn databases, queries and SQL fundamentals.", "sql"),
    ("HTML & CSS", "🎨", "Build modern and responsive websites.", "html-css"),
]


# =========================================================
# LESSON NAMES
# =========================================================

LESSONS = {
    "python": [
        "Introduction",
        "Variables & Data Types",
        "Operators",
        "Conditions",
        "Loops",
        "Functions",
        "OOP",
        "File Handling"
    ],

    "c": [
        "Introduction",
        "Variables",
        "Data Types",
        "Operators",
        "Conditions",
        "Loops",
        "Functions",
        "Arrays"
    ],

    "cpp": [
        "Introduction",
        "Variables",
        "Functions",
        "Classes & Objects",
        "Inheritance",
        "Polymorphism",
        "STL"
    ],

    "java": [
        "Introduction",
        "Variables",
        "Methods",
        "Classes & Objects",
        "Inheritance",
        "Interfaces",
        "Exception Handling"
    ],

    "javascript": [
        "Introduction",
        "Variables",
        "Functions",
        "Arrays",
        "Objects",
        "DOM",
        "Events",
        "Async JavaScript"
    ],

    "sql": [
        "Introduction",
        "SELECT",
        "WHERE & ORDER BY",
        "INSERT",
        "UPDATE",
        "DELETE",
        "JOINs",
        "GROUP BY"
    ],

    "html-css": [
        "HTML Basics",
        "Text & Links",
        "Images & Forms",
        "CSS Basics",
        "Flexbox",
        "Grid",
        "Responsive Design"
    ]
}


# =========================================================
# DATABASE
# =========================================================

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS progress(
            user_id INTEGER NOT NULL,
            language TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            exam_score INTEGER DEFAULT 0,
            exam_passed INTEGER DEFAULT 0,
            PRIMARY KEY(user_id, language)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS lesson_progress(
            user_id INTEGER NOT NULL,
            language TEXT NOT NULL,
            lesson_id INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            PRIMARY KEY(user_id, language, lesson_id)
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(f):

    @wraps(f)
    def wrapped(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("signin"))

        return f(*args, **kwargs)

    return wrapped


# =========================================================
# GET COURSE PROGRESS
# =========================================================

def get_progress(user_id, slug):

    conn = db()

    row = conn.execute(
        """
        SELECT *
        FROM progress
        WHERE user_id=? AND language=?
        """,
        (user_id, slug)
    ).fetchone()

    conn.close()

    if row:
        return dict(row)

    return {
        "completed": 0,
        "exam_score": 0,
        "exam_passed": 0
    }


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        languages=LANGUAGES
    )


# =========================================================
# SIGN UP
# =========================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not name or not email or not password:

            flash(
                "Please fill all fields.",
                "error"
            )

        elif password != confirm:

            flash(
                "Passwords do not match.",
                "error"
            )

        elif len(password) < 6:

            flash(
                "Password must be at least 6 characters.",
                "error"
            )

        else:

            conn = db()

            try:

                conn.execute(
                    """
                    INSERT INTO users(name,email,password)
                    VALUES(?,?,?)
                    """,
                    (
                        name,
                        email,
                        generate_password_hash(password)
                    )
                )

                conn.commit()

                flash(
                    "Account created! Please sign in.",
                    "success"
                )

                return redirect(
                    url_for("signin")
                )

            except sqlite3.IntegrityError:

                flash(
                    "This email is already registered.",
                    "error"
                )

            finally:

                conn.close()

    return render_template("signup.html")


# =========================================================
# SIGN IN
# =========================================================

@app.route("/signin", methods=["GET", "POST"])
def signin():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        conn = db()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["name"] = user["name"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template("signin.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    data = []

    for name, icon, desc, slug in LANGUAGES:

        p = get_progress(
            session["user_id"],
            slug
        )

        data.append(
            (
                name,
                icon,
                desc,
                slug,
                p
            )
        )

    completed = sum(
        1
        for x in data
        if x[4]["exam_passed"]
    )

    average = round(
        sum(
            x[4]["completed"]
            for x in data
        ) / len(data)
    ) if data else 0

    return render_template(
        "dashboard.html",
        languages=data,
        completed=completed,
        average=average
    )


# =========================================================
# COURSE PAGE
# =========================================================

@app.route("/course/<slug>")
@login_required
def course(slug):

    if slug not in LESSONS:

        return redirect(
            url_for("dashboard")
        )

    language = next(
        (
            x
            for x in LANGUAGES
            if x[3] == slug
        ),
        None
    )

    progress = get_progress(
        session["user_id"],
        slug
    )

    # Lesson completion status
    conn = db()

    completed_lessons = conn.execute(
        """
        SELECT lesson_id
        FROM lesson_progress
        WHERE user_id=?
        AND language=?
        AND completed=1
        """,
        (
            session["user_id"],
            slug
        )
    ).fetchall()

    conn.close()

    completed_ids = [
        row["lesson_id"]
        for row in completed_lessons
    ]

    return render_template(
        "course.html",
        language=language,
        slug=slug,
        lessons=LESSONS[slug],
        progress=progress,
        completed_lessons=completed_ids
    )


# =========================================================
# OPEN LESSON
# =========================================================

@app.route("/lesson/<slug>/<int:lesson_id>")
@login_required
def lesson(slug, lesson_id):

    # -----------------------------------------------------
    # CHECK COURSE
    # -----------------------------------------------------

    if slug not in LESSONS:

        return redirect(
            url_for("dashboard")
        )

    # -----------------------------------------------------
    # GET LANGUAGE
    # IMPORTANT: DEFINE BEFORE RENDER_TEMPLATE
    # -----------------------------------------------------

    language = next(
        (
            x
            for x in LANGUAGES
            if x[3] == slug
        ),
        None
    )

    if language is None:

        return redirect(
            url_for("dashboard")
        )

    # -----------------------------------------------------
    # CHECK LESSON DATA
    # -----------------------------------------------------

    if slug not in LESSON_CONTENT:

        flash(
            "Lessons for this course are coming soon.",
            "error"
        )

        return redirect(
            url_for(
                "course",
                slug=slug
            )
        )

    # -----------------------------------------------------
    # CHECK LESSON NUMBER
    # -----------------------------------------------------

    course_data = LESSON_CONTENT[slug]

    # lesson_data can be dictionary OR list
    if isinstance(course_data, dict):

        lesson_keys = list(
            course_data.keys()
        )

        if lesson_id >= len(lesson_keys):

            flash(
                "This lesson does not exist.",
                "error"
            )

            return redirect(
                url_for(
                    "course",
                    slug=slug
                )
            )

        lesson_key = lesson_keys[lesson_id]
        lesson_content = course_data[lesson_key]

    elif isinstance(course_data, list):

        if lesson_id >= len(course_data):

            flash(
                "This lesson does not exist.",
                "error"
            )

            return redirect(
                url_for(
                    "course",
                    slug=slug
                )
            )

        lesson_content = course_data[lesson_id]

    else:

        flash(
            "Invalid lesson data.",
            "error"
        )

        return redirect(
            url_for(
                "course",
                slug=slug
            )
        )

    # -----------------------------------------------------
    # SAVE CURRENT LESSON AS VIEWED
    # -----------------------------------------------------

    conn = db()

    conn.execute(
        """
        INSERT INTO lesson_progress(
            user_id,
            language,
            lesson_id,
            completed
        )
        VALUES(?,?,?,0)
        ON CONFLICT(
            user_id,
            language,
            lesson_id
        )
        DO NOTHING
        """,
        (
            session["user_id"],
            slug,
            lesson_id
        )
    )

    conn.commit()
    conn.close()

    # -----------------------------------------------------
    # RENDER LESSON
    # -----------------------------------------------------

    return render_template(
        "lesson.html",
        language=language,
        slug=slug,
        lesson_id=lesson_id,
        lesson=lesson_content,
        lesson_title=LESSONS[slug][lesson_id],
        total_lessons=len(LESSONS[slug])
    )


# =========================================================
# COMPLETE LESSON
# =========================================================

@app.route(
    "/lesson/<slug>/<int:lesson_id>/complete",
    methods=["POST"]
)
@login_required
def complete_lesson(slug, lesson_id):

    if slug not in LESSONS:

        return redirect(
            url_for("dashboard")
        )

    if lesson_id < 0 or lesson_id >= len(LESSONS[slug]):

        return redirect(
            url_for(
                "course",
                slug=slug
            )
        )

    conn = db()

    # Mark lesson completed
    conn.execute(
        """
        INSERT INTO lesson_progress(
            user_id,
            language,
            lesson_id,
            completed
        )
        VALUES(?,?,?,1)
        ON CONFLICT(
            user_id,
            language,
            lesson_id
        )
        DO UPDATE SET completed=1
        """,
        (
            session["user_id"],
            slug,
            lesson_id
        )
    )

    # Count completed lessons
    completed_count = conn.execute(
        """
        SELECT COUNT(*)
        FROM lesson_progress
        WHERE user_id=?
        AND language=?
        AND completed=1
        """,
        (
            session["user_id"],
            slug
        )
    ).fetchone()[0]

    total_lessons = len(
        LESSONS[slug]
    )

    percentage = round(
        completed_count /
        total_lessons *
        100
    )

    # Update course progress
    conn.execute(
        """
        INSERT INTO progress(
            user_id,
            language,
            completed
        )
        VALUES(?,?,?)
        ON CONFLICT(
            user_id,
            language
        )
        DO UPDATE SET completed=?
        """,
        (
            session["user_id"],
            slug,
            percentage,
            percentage
        )
    )

    conn.commit()
    conn.close()

    # Go to next lesson
    next_lesson = lesson_id + 1

    if next_lesson < total_lessons:

        return redirect(
            url_for(
                "lesson",
                slug=slug,
                lesson_id=next_lesson
            )
        )

    return redirect(
        url_for(
            "course",
            slug=slug
        )
    )


# =========================================================
# COURSE COMPLETE BUTTON
# =========================================================

@app.route(
    "/course/<slug>/complete",
    methods=["POST"]
)
@login_required
def complete_course(slug):

    if slug not in LESSONS:

        return redirect(
            url_for("dashboard")
        )

    conn = db()

    conn.execute(
        """
        INSERT INTO progress(
            user_id,
            language,
            completed
        )
        VALUES(?,?,100)
        ON CONFLICT(
            user_id,
            language
        )
        DO UPDATE SET completed=100
        """,
        (
            session["user_id"],
            slug
        )
    )

    conn.commit()
    conn.close()

    return redirect(
        url_for(
            "course",
            slug=slug
        )
    )


# =========================================================
# CERTIFICATE
# =========================================================

@app.route("/certificate/<slug>")
@login_required
def certificate(slug):

    if slug not in LESSONS:

        return redirect(
            url_for("dashboard")
        )

    language = next(
        (
            x
            for x in LANGUAGES
            if x[3] == slug
        ),
        None
    )

    progress = get_progress(
        session["user_id"],
        slug
    )

    # Certificate allowed after course completion
    if progress["completed"] < 100:

        flash(
            "Complete the course first to get your certificate.",
            "error"
        )

        return redirect(
            url_for(
                "course",
                slug=slug
            )
        )

    return render_template(
        "certificate.html",
        language=language,
        slug=slug,
        user_name=session.get(
            "name",
            "Student"
        )
    )


# =========================================================
# EXAM
# =========================================================

@app.route(
    "/exam/<slug>",
    methods=["GET", "POST"]
)
@login_required
def exam(slug):

    language = next(
        (
            x
            for x in LANGUAGES
            if x[3] == slug
        ),
        None
    )

    if not language:

        return redirect(
            url_for("dashboard")
        )

    questions = {

        "python": [
            (
                "Which keyword defines a function in Python?",
                ["func", "def", "function", "define"],
                1
            ),
            (
                "Which type stores True or False?",
                ["str", "bool", "int", "list"],
                1
            ),
            (
                "Which symbol starts a comment?",
                ["//", "#", "/*", "--"],
                1
            ),
            (
                "What is len([1,2,3])?",
                ["2", "3", "4", "1"],
                1
            ),
            (
                "Which is a Python loop?",
                ["repeat", "foreach", "for", "loop"],
                2
            )
        ],

        "c": [
            (
                "Which function is the C entry point?",
                ["start", "main", "run", "begin"],
                1
            ),
            (
                "Which symbol ends a C statement?",
                [".", ":", ";", ","],
                2
            )
        ],

        "cpp": [
            (
                "Which language is C++ based on?",
                ["C", "Python", "Java", "Ruby"],
                0
            ),
            (
                "Which feature belongs to OOP?",
                ["Class", "Markup", "Query", "Selector"],
                0
            )
        ],

        "java": [
            (
                "Which keyword creates a class?",
                ["object", "class", "newclass", "define"],
                1
            ),
            (
                "Java source files commonly use which extension?",
                [".py", ".cpp", ".java", ".js"],
                2
            )
        ],

        "javascript": [
            (
                "Which keyword declares a constant?",
                ["constant", "let", "const", "fixed"],
                2
            ),
            (
                "Which symbol commonly ends a JS statement?",
                [";", "#", "$", "@"],
                0
            )
        ],

        "sql": [
            (
                "Which command reads data?",
                ["SELECT", "PULL", "READ", "FETCHALL"],
                0
            ),
            (
                "Which command adds a row?",
                ["ADD", "INSERT", "PUSH", "CREATE"],
                1
            )
        ],

        "html-css": [
            (
                "Which tag creates a heading?",
                ["<h1>", "<head>", "<title>", "<heading>"],
                0
            ),
            (
                "Which CSS property changes text color?",
                ["font-color", "text-color", "color", "foreground"],
                2
            )
        ]
    }

    exam_questions = questions.get(
        slug,
        []
    )

    score = None
    passed = False

    if request.method == "POST":

        score = sum(
            int(
                request.form.get(
                    f"q{i}",
                    -1
                )
            ) == q[2]
            for i, q in enumerate(
                exam_questions
            )
        )

        passed = (
            score /
            len(exam_questions)
            >= 0.6
        )

        percentage = round(
            score /
            len(exam_questions)
            * 100
        )

        conn = db()

        conn.execute(
            """
            INSERT INTO progress(
                user_id,
                language,
                exam_score,
                exam_passed
            )
            VALUES(?,?,?,?)

            ON CONFLICT(
                user_id,
                language
            )

            DO UPDATE SET
                exam_score=?,
                exam_passed=?
            """,
            (
                session["user_id"],
                slug,
                percentage,
                int(passed),
                percentage,
                int(passed)
            )
        )

        conn.commit()
        conn.close()

    return render_template(
        "exam.html",
        language=language,
        slug=slug,
        questions=exam_questions,
        score=score,
        passed=passed
    )


# =========================================================
# START APP
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )