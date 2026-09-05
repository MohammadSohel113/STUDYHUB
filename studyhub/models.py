import secrets
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

LEVELS = ["beginner", "intermediate", "advanced"]


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class Student(UserMixin, db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    progress = db.relationship("Progress", backref="student", lazy=True, cascade="all, delete-orphan")
    attempts = db.relationship("QuizAttempt", backref="student", lazy=True, cascade="all, delete-orphan")
    certificates = db.relationship("Certificate", backref="student", lazy=True, cascade="all, delete-orphan")

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

    def get_id(self):
        # Prefix so Flask-Login can tell students and admins apart in the session.
        return f"student-{self.id}"

    def progress_for_course(self, course):
        lessons = [l for ch in course.chapters for l in ch.lessons]
        if not lessons:
            return 0
        completed_ids = {p.lesson_id for p in self.progress}
        done = sum(1 for l in lessons if l.id in completed_ids)
        return round(done / len(lessons) * 100)

    def has_completed_lesson(self, lesson_id):
        return any(p.lesson_id == lesson_id for p in self.progress)


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

    def get_id(self):
        return f"admin-{self.id}"


# ---------------------------------------------------------------------------
# Courses
# ---------------------------------------------------------------------------

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    icon = db.Column(db.String(10), default="💻")
    tagline = db.Column(db.String(160), default="")
    description = db.Column(db.Text, default="")
    order = db.Column(db.Integer, default=0)

    chapters = db.relationship("Chapter", backref="course", lazy=True,
                                order_by="Chapter.order", cascade="all, delete-orphan")

    def chapters_for_level(self, level):
        return [c for c in self.chapters if c.level == level]

    def lesson_count(self):
        return sum(len(c.lessons) for c in self.chapters)

    def final_exam(self):
        return Quiz.query.filter_by(course_id=self.id, kind="exam").first()


class Chapter(db.Model):
    __tablename__ = "chapters"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    level = db.Column(db.String(20), nullable=False)  # beginner / intermediate / advanced
    title = db.Column(db.String(120), nullable=False)
    order = db.Column(db.Integer, default=0)

    lessons = db.relationship("Lesson", backref="chapter", lazy=True,
                               order_by="Lesson.order", cascade="all, delete-orphan")
    quiz = db.relationship("Quiz", backref="chapter", lazy=True, uselist=False,
                            cascade="all, delete-orphan")


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(160), nullable=False)
    order = db.Column(db.Integer, default=0)

    explanation = db.Column(db.Text, default="")
    syntax = db.Column(db.Text, default="")
    code_example = db.Column(db.Text, default="")
    output_example = db.Column(db.Text, default="")
    notes = db.Column(db.Text, default="")
    common_mistakes = db.Column(db.Text, default="")
    practice_questions = db.Column(db.Text, default="")  # newline separated

    def practice_list(self):
        return [q for q in (self.practice_questions or "").split("\n") if q.strip()]

    def next_lesson(self):
        siblings = self.chapter.lessons
        idx = siblings.index(self)
        if idx + 1 < len(siblings):
            return siblings[idx + 1]
        # move to next chapter in the same course
        chapters = self.chapter.course.chapters
        cidx = chapters.index(self.chapter)
        if cidx + 1 < len(chapters) and chapters[cidx + 1].lessons:
            return chapters[cidx + 1].lessons[0]
        return None

    def previous_lesson(self):
        siblings = self.chapter.lessons
        idx = siblings.index(self)
        if idx - 1 >= 0:
            return siblings[idx - 1]
        chapters = self.chapter.course.chapters
        cidx = chapters.index(self.chapter)
        if cidx - 1 >= 0 and chapters[cidx - 1].lessons:
            return chapters[cidx - 1].lessons[-1]
        return None


class Progress(db.Model):
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    lesson = db.relationship("Lesson")

    __table_args__ = (db.UniqueConstraint("student_id", "lesson_id", name="uq_student_lesson"),)


# ---------------------------------------------------------------------------
# Quizzes / exams
# ---------------------------------------------------------------------------

class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=True)
    title = db.Column(db.String(140), nullable=False)
    kind = db.Column(db.String(10), default="quiz")  # "quiz" or "exam"
    pass_percent = db.Column(db.Integer, default=60)

    questions = db.relationship("Question", backref="quiz", lazy=True,
                                 order_by="Question.order", cascade="all, delete-orphan")

    course = db.relationship("Course", backref="exams", foreign_keys=[course_id])

    def best_attempt(self, student_id):
        return (QuizAttempt.query
                .filter_by(quiz_id=self.id, student_id=student_id)
                .order_by(QuizAttempt.score.desc()).first())


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)

    choices = db.relationship("Choice", backref="question", lazy=True,
                               order_by="Choice.id", cascade="all, delete-orphan")


class Choice(db.Model):
    __tablename__ = "choices"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    score = db.Column(db.Integer, default=0)          # percent
    passed = db.Column(db.Boolean, default=False)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    answers_json = db.Column(db.Text, default="{}")   # {question_id: choice_id}

    quiz = db.relationship("Quiz")


# ---------------------------------------------------------------------------
# Certificates
# ---------------------------------------------------------------------------

class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    issued_at = db.Column(db.Date, default=date.today)

    course = db.relationship("Course")

    @staticmethod
    def generate_code():
        return "SH-" + secrets.token_hex(4).upper()
