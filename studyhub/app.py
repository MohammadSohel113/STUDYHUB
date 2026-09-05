import os
import json
from functools import wraps
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import (login_user, logout_user, login_required,
                          current_user, LoginManager)

from extensions import db, login_manager
from models import (Student, Admin, Course, Chapter, Lesson, Progress,
                     Quiz, Question, Choice, QuizAttempt, Certificate, LEVELS)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-this-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "studyhub.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """user_id is prefixed e.g. 'student-3' or 'admin-1' so we know which table to hit."""
    if user_id.startswith("student-"):
        return Student.query.get(int(user_id.split("-", 1)[1]))
    if user_id.startswith("admin-"):
        return Admin.query.get(int(user_id.split("-", 1)[1]))
    return None


# ---------------------------------------------------------------------------
# Access-control decorators
# ---------------------------------------------------------------------------

def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Student):
            flash("Please log in to your student account to continue.", "error")
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            flash("Admin login required.", "error")
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_globals():
    return {"current_year": datetime.utcnow().year}


# ---------------------------------------------------------------------------
# Public pages
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    courses = Course.query.order_by(Course.order).all()
    return render_template("index.html", courses=courses)


@app.route("/courses")
def courses():
    all_courses = Course.query.order_by(Course.order).all()
    return render_template("courses.html", courses=all_courses)


@app.route("/courses/<slug>")
def course_detail(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    progress_pct = None
    completed_lesson_ids = set()
    if isinstance(current_user, Student):
        progress_pct = current_user.progress_for_course(course)
        completed_lesson_ids = {p.lesson_id for p in current_user.progress}
    return render_template("course.html", course=course, levels=LEVELS,
                            progress_pct=progress_pct,
                            completed_lesson_ids=completed_lesson_ids)


@app.route("/about")
def about():
    return render_template("about.html")


# ---------------------------------------------------------------------------
# Student authentication
# ---------------------------------------------------------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if isinstance(current_user, Student):
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = []
        if not full_name or not email or not username or not password:
            errors.append("Please fill in every field.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if Student.query.filter_by(email=email).first():
            errors.append("An account with this email already exists.")
        if Student.query.filter_by(username=username).first():
            errors.append("That username is already taken.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("signup.html", form=request.form)

        student = Student(full_name=full_name, email=email, username=username)
        student.set_password(password)
        db.session.add(student)
        db.session.commit()
        login_user(student)
        flash(f"Welcome to STUDY HUB, {student.full_name.split()[0]}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("signup.html", form={})


@app.route("/login", methods=["GET", "POST"])
def login():
    if isinstance(current_user, Student):
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "")
        student = (Student.query.filter_by(email=identifier).first()
                   or Student.query.filter_by(username=identifier).first())
        if student and student.check_password(password):
            login_user(student)
            flash(f"Welcome back, {student.full_name.split()[0]}!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard"))
        flash("Incorrect email/username or password.", "error")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Student dashboard / profile / learning
# ---------------------------------------------------------------------------

@app.route("/dashboard")
@student_required
def dashboard():
    courses_all = Course.query.order_by(Course.order).all()
    enrolled = [c for c in courses_all if current_user.progress_for_course(c) > 0]
    course_progress = [(c, current_user.progress_for_course(c)) for c in courses_all]
    course_progress = [cp for cp in course_progress if cp[1] > 0] or course_progress[:4]

    last_progress = (Progress.query.filter_by(student_id=current_user.id)
                      .order_by(Progress.completed_at.desc()).first())
    continue_lesson = None
    if last_progress:
        continue_lesson = last_progress.lesson.next_lesson()
    if not continue_lesson and courses_all and courses_all[0].chapters and courses_all[0].chapters[0].lessons:
        continue_lesson = courses_all[0].chapters[0].lessons[0]

    attempts = (QuizAttempt.query.filter_by(student_id=current_user.id)
                .order_by(QuizAttempt.attempted_at.desc()).limit(6).all())
    certificates = Certificate.query.filter_by(student_id=current_user.id).all()
    total_completed = Progress.query.filter_by(student_id=current_user.id).count()

    return render_template("student_dashboard.html",
                            course_progress=course_progress,
                            continue_lesson=continue_lesson,
                            attempts=attempts,
                            certificates=certificates,
                            total_completed=total_completed)


@app.route("/profile")
@student_required
def profile():
    certificates = Certificate.query.filter_by(student_id=current_user.id).all()
    total_completed = Progress.query.filter_by(student_id=current_user.id).count()
    attempts = QuizAttempt.query.filter_by(student_id=current_user.id).count()
    return render_template("profile.html", certificates=certificates,
                            total_completed=total_completed, attempts=attempts)


@app.route("/lesson/<int:lesson_id>")
@student_required
def lesson_view(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    completed = current_user.has_completed_lesson(lesson.id)
    return render_template("lesson.html", lesson=lesson, completed=completed,
                            course=lesson.chapter.course)


@app.route("/lesson/<int:lesson_id>/complete", methods=["POST"])
@student_required
def lesson_complete(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if not current_user.has_completed_lesson(lesson.id):
        db.session.add(Progress(student_id=current_user.id, lesson_id=lesson.id))
        db.session.commit()
        flash("Lesson marked as completed. Great job!", "success")
    nxt = lesson.next_lesson()
    if nxt:
        return redirect(url_for("lesson_view", lesson_id=nxt.id))
    return redirect(url_for("course_detail", slug=lesson.chapter.course.slug))


@app.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
@student_required
def quiz_view(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == "POST":
        total = len(quiz.questions)
        correct = 0
        answers = {}
        for q in quiz.questions:
            chosen = request.form.get(f"question-{q.id}")
            answers[q.id] = chosen
            if chosen:
                choice = Choice.query.get(int(chosen))
                if choice and choice.is_correct:
                    correct += 1
        score = round((correct / total) * 100) if total else 0
        passed = score >= quiz.pass_percent

        attempt = QuizAttempt(student_id=current_user.id, quiz_id=quiz.id,
                               score=score, passed=passed,
                               answers_json=json.dumps(answers))
        db.session.add(attempt)

        # Award a certificate for a passed final exam.
        if passed and quiz.kind == "exam" and quiz.course_id:
            existing = Certificate.query.filter_by(student_id=current_user.id,
                                                     course_id=quiz.course_id).first()
            if not existing:
                cert = Certificate(student_id=current_user.id, course_id=quiz.course_id,
                                    code=Certificate.generate_code())
                db.session.add(cert)
        db.session.commit()
        return render_template("quiz_result.html", quiz=quiz, score=score,
                                passed=passed, correct=correct, total=total)

    return render_template("quiz.html", quiz=quiz)


@app.route("/certificates")
@student_required
def certificates():
    certs = Certificate.query.filter_by(student_id=current_user.id).all()
    return render_template("certificates.html", certificates=certs)


@app.route("/certificate/<code>")
def certificate_view(code):
    cert = Certificate.query.filter_by(code=code).first_or_404()
    return render_template("certificate.html", cert=cert)


# ---------------------------------------------------------------------------
# Admin authentication (login only — no public registration)
# ---------------------------------------------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if isinstance(current_user, Admin):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash("Welcome back, admin.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Incorrect admin username or password.", "error")
    return render_template("admin/login.html")


@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    flash("Admin logged out.", "success")
    return redirect(url_for("admin_login"))


# ---------------------------------------------------------------------------
# Admin dashboard
# ---------------------------------------------------------------------------

@app.route("/admin")
@admin_required
def admin_dashboard():
    stats = {
        "students": Student.query.count(),
        "courses": Course.query.count(),
        "lessons": Lesson.query.count(),
        "attempts": QuizAttempt.query.count(),
        "certificates": Certificate.query.count(),
    }
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats, recent_students=recent_students)


@app.route("/admin/students")
@admin_required
def admin_students():
    q = request.args.get("q", "").strip()
    query = Student.query
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Student.full_name.ilike(like),
                                     Student.email.ilike(like),
                                     Student.username.ilike(like)))
    students = query.order_by(Student.created_at.desc()).all()
    return render_template("admin/students.html", students=students, q=q)


@app.route("/admin/students/<int:student_id>")
@admin_required
def admin_student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    courses_all = Course.query.order_by(Course.order).all()
    course_progress = [(c, student.progress_for_course(c)) for c in courses_all]
    attempts = (QuizAttempt.query.filter_by(student_id=student.id)
                .order_by(QuizAttempt.attempted_at.desc()).all())
    certs = Certificate.query.filter_by(student_id=student.id).all()
    return render_template("admin/student_detail.html", student=student,
                            course_progress=course_progress, attempts=attempts, certs=certs)


# ---- Course management ----

@app.route("/admin/courses")
@admin_required
def admin_courses():
    all_courses = Course.query.order_by(Course.order).all()
    return render_template("admin/courses.html", courses=all_courses)


@app.route("/admin/courses/add", methods=["POST"])
@admin_required
def admin_course_add():
    name = request.form.get("name", "").strip()
    slug = request.form.get("slug", "").strip().lower().replace(" ", "-")
    icon = request.form.get("icon", "💻").strip() or "💻"
    tagline = request.form.get("tagline", "").strip()
    if not name or not slug:
        flash("Course name and slug are required.", "error")
    elif Course.query.filter_by(slug=slug).first():
        flash("A course with that slug already exists.", "error")
    else:
        order = (db.session.query(db.func.max(Course.order)).scalar() or 0) + 1
        db.session.add(Course(name=name, slug=slug, icon=icon, tagline=tagline, order=order))
        db.session.commit()
        flash(f"Course '{name}' added.", "success")
    return redirect(url_for("admin_courses"))


@app.route("/admin/courses/<int:course_id>/edit", methods=["POST"])
@admin_required
def admin_course_edit(course_id):
    course = Course.query.get_or_404(course_id)
    course.name = request.form.get("name", course.name).strip()
    course.icon = request.form.get("icon", course.icon).strip() or course.icon
    course.tagline = request.form.get("tagline", course.tagline).strip()
    db.session.commit()
    flash("Course updated.", "success")
    return redirect(url_for("admin_courses"))


@app.route("/admin/courses/<int:course_id>/delete", methods=["POST"])
@admin_required
def admin_course_delete(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted.", "success")
    return redirect(url_for("admin_courses"))


# ---- Chapter management ----

@app.route("/admin/courses/<int:course_id>/chapters")
@admin_required
def admin_chapters(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template("admin/chapters.html", course=course, levels=LEVELS)


@app.route("/admin/courses/<int:course_id>/chapters/add", methods=["POST"])
@admin_required
def admin_chapter_add(course_id):
    course = Course.query.get_or_404(course_id)
    title = request.form.get("title", "").strip()
    level = request.form.get("level", "beginner")
    if not title:
        flash("Chapter title is required.", "error")
    else:
        order = len(course.chapters_for_level(level)) + 1
        db.session.add(Chapter(course_id=course.id, title=title, level=level, order=order))
        db.session.commit()
        flash("Chapter added.", "success")
    return redirect(url_for("admin_chapters", course_id=course.id))


@app.route("/admin/chapters/<int:chapter_id>/edit", methods=["POST"])
@admin_required
def admin_chapter_edit(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    chapter.title = request.form.get("title", chapter.title).strip()
    db.session.commit()
    flash("Chapter updated.", "success")
    return redirect(url_for("admin_chapters", course_id=chapter.course_id))


@app.route("/admin/chapters/<int:chapter_id>/delete", methods=["POST"])
@admin_required
def admin_chapter_delete(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    course_id = chapter.course_id
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter deleted.", "success")
    return redirect(url_for("admin_chapters", course_id=course_id))


# ---- Lesson management ----

@app.route("/admin/chapters/<int:chapter_id>/lessons")
@admin_required
def admin_lessons(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template("admin/lessons.html", chapter=chapter)


@app.route("/admin/chapters/<int:chapter_id>/lessons/add", methods=["POST"])
@admin_required
def admin_lesson_add(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    title = request.form.get("title", "").strip()
    if not title:
        flash("Lesson title is required.", "error")
        return redirect(url_for("admin_lessons", chapter_id=chapter.id))
    lesson = Lesson(
        chapter_id=chapter.id, title=title,
        slug=title.lower().replace(" ", "-"), order=len(chapter.lessons) + 1,
        explanation=request.form.get("explanation", ""),
        syntax=request.form.get("syntax", ""),
        code_example=request.form.get("code_example", ""),
        output_example=request.form.get("output_example", ""),
        notes=request.form.get("notes", ""),
        common_mistakes=request.form.get("common_mistakes", ""),
        practice_questions=request.form.get("practice_questions", ""),
    )
    db.session.add(lesson)
    db.session.commit()
    flash("Lesson added.", "success")
    return redirect(url_for("admin_lessons", chapter_id=chapter.id))


@app.route("/admin/lessons/<int:lesson_id>/edit", methods=["POST"])
@admin_required
def admin_lesson_edit(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    for field in ["title", "explanation", "syntax", "code_example", "output_example",
                  "notes", "common_mistakes", "practice_questions"]:
        if field in request.form:
            setattr(lesson, field, request.form.get(field))
    db.session.commit()
    flash("Lesson updated.", "success")
    return redirect(url_for("admin_lessons", chapter_id=lesson.chapter_id))


@app.route("/admin/lessons/<int:lesson_id>/delete", methods=["POST"])
@admin_required
def admin_lesson_delete(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    chapter_id = lesson.chapter_id
    db.session.delete(lesson)
    db.session.commit()
    flash("Lesson deleted.", "success")
    return redirect(url_for("admin_lessons", chapter_id=chapter_id))


# ---- Quiz management ----

@app.route("/admin/quizzes")
@admin_required
def admin_quizzes():
    quizzes = Quiz.query.all()
    courses_all = Course.query.order_by(Course.order).all()
    return render_template("admin/quizzes.html", quizzes=quizzes, courses=courses_all)


@app.route("/admin/quizzes/add", methods=["POST"])
@admin_required
def admin_quiz_add():
    title = request.form.get("title", "").strip()
    kind = request.form.get("kind", "quiz")
    course_id = request.form.get("course_id") or None
    chapter_id = request.form.get("chapter_id") or None
    pass_percent = int(request.form.get("pass_percent", 60) or 60)
    if not title:
        flash("Quiz title is required.", "error")
    else:
        db.session.add(Quiz(title=title, kind=kind, course_id=course_id,
                             chapter_id=chapter_id, pass_percent=pass_percent))
        db.session.commit()
        flash("Quiz created. Now add questions to it.", "success")
    return redirect(url_for("admin_quizzes"))


@app.route("/admin/quizzes/<int:quiz_id>")
@admin_required
def admin_quiz_detail(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template("admin/quiz_detail.html", quiz=quiz)


@app.route("/admin/quizzes/<int:quiz_id>/delete", methods=["POST"])
@admin_required
def admin_quiz_delete(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted.", "success")
    return redirect(url_for("admin_quizzes"))


@app.route("/admin/quizzes/<int:quiz_id>/questions/add", methods=["POST"])
@admin_required
def admin_question_add(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    text = request.form.get("text", "").strip()
    options = [request.form.get(f"option{i}", "").strip() for i in range(1, 5)]
    correct_index = int(request.form.get("correct_index", 0))
    if not text or not any(options):
        flash("Question text and at least one option are required.", "error")
        return redirect(url_for("admin_quiz_detail", quiz_id=quiz.id))
    question = Question(quiz_id=quiz.id, text=text, order=len(quiz.questions) + 1)
    db.session.add(question)
    db.session.flush()
    for i, opt in enumerate(options):
        if opt:
            db.session.add(Choice(question_id=question.id, text=opt,
                                   is_correct=(i == correct_index)))
    db.session.commit()
    flash("Question added.", "success")
    return redirect(url_for("admin_quiz_detail", quiz_id=quiz.id))


@app.route("/admin/questions/<int:question_id>/delete", methods=["POST"])
@admin_required
def admin_question_delete(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted.", "success")
    return redirect(url_for("admin_quiz_detail", quiz_id=quiz_id))


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
