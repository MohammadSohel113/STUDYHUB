"""
Populates STUDY HUB with an admin account, a demo student, and course content.

Run once after installing dependencies:
    python seed.py

Safe to re-run: it skips anything that already exists.
"""
from app import app
from extensions import db
from models import (Admin, Student, Course, Chapter, Lesson, Quiz, Question, Choice)


def add_course(name, slug, icon, tagline, description):
    course = Course.query.filter_by(slug=slug).first()
    if course:
        return course
    course = Course(name=name, slug=slug, icon=icon, tagline=tagline,
                     description=description, order=Course.query.count())
    db.session.add(course)
    db.session.flush()
    return course


def add_chapter(course, level, title, order):
    chapter = Chapter(course_id=course.id, level=level, title=title, order=order)
    db.session.add(chapter)
    db.session.flush()
    return chapter


def add_lesson(chapter, order, title, explanation, syntax="", code="", output="",
                notes="", mistakes="", practice=None):
    lesson = Lesson(
        chapter_id=chapter.id, order=order, title=title,
        slug=title.lower().replace(" ", "-"),
        explanation=explanation, syntax=syntax, code_example=code,
        output_example=output, notes=notes, common_mistakes=mistakes,
        practice_questions="\n".join(practice or []),
    )
    db.session.add(lesson)
    return lesson


def add_quiz(title, kind, questions, course_id=None, chapter_id=None, pass_percent=60):
    quiz = Quiz(title=title, kind=kind, course_id=course_id, chapter_id=chapter_id,
                pass_percent=pass_percent)
    db.session.add(quiz)
    db.session.flush()
    for i, (text, options, correct_index) in enumerate(questions):
        q = Question(quiz_id=quiz.id, text=text, order=i)
        db.session.add(q)
        db.session.flush()
        for j, opt in enumerate(options):
            db.session.add(Choice(question_id=q.id, text=opt, is_correct=(j == correct_index)))
    return quiz


def seed_accounts():
    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        print("Created admin account -> username: admin / password: admin123")

    if not Student.query.filter_by(username="demo").first():
        demo = Student(full_name="Demo Student", email="demo@studyhub.dev", username="demo")
        demo.set_password("demo1234")
        db.session.add(demo)
        print("Created demo student -> username: demo / password: demo1234")

    db.session.commit()


def seed_python():
    c = add_course("Python", "python", "🐍",
                    "The friendliest first language — clean syntax, huge community.",
                    "Python is a beginner-friendly, general-purpose language used for web "
                    "development, automation, data science, and more. Its simple, readable "
                    "syntax makes it one of the best languages to learn programming with.")
    if c.chapters:
        return

    ch1 = add_chapter(c, "beginner", "Getting Started with Python", 1)
    add_lesson(ch1, 1, "Introduction & Installation",
        "Python is an interpreted, high-level programming language known for its clean, "
        "readable syntax. It is used for websites, automation scripts, data analysis, "
        "artificial intelligence, and much more. To start writing Python code, download "
        "Python from python.org and install it on your computer, or use an online editor "
        "to practice without installing anything.",
        syntax="python --version          # check installed version\npython script.py         # run a Python file",
        code='print("Hello, World!")',
        output="Hello, World!",
        notes="On Windows, make sure to tick 'Add Python to PATH' during installation, or "
              "the python command won't work in your terminal.",
        mistakes="Forgetting the parentheses in print() — this is a very common mistake "
                  "for beginners coming from Python 2 tutorials, where print worked without them.",
        practice=["Install Python on your computer and confirm the version in your terminal.",
                  "Write a program that prints your name."])
    add_lesson(ch1, 2, "Variables & Data Types",
        "A variable is a name that stores a value so you can use it later in your program. "
        "Python is dynamically typed, meaning you don't need to declare a variable's type — "
        "Python figures it out automatically based on the value you assign. Common data "
        "types include integers, floats, strings, and booleans.",
        syntax="name = value",
        code='age = 20\nprice = 9.99\ncity = "Kolkata"\nis_student = True\nprint(age, price, city, is_student)',
        output="20 9.99 Kolkata True",
        notes="Use type(variable) to check the data type of any variable at runtime.",
        mistakes="Using a number as the first character of a variable name (e.g. 1name) — "
                  "this is not allowed in Python.",
        practice=["Create variables for your name, age, and favorite number, then print them.",
                  "Use type() to print the data type of each variable you created."])
    add_lesson(ch1, 3, "Operators",
        "Operators let you perform actions on values and variables. Python supports "
        "arithmetic operators (+, -, *, /), comparison operators (==, !=, >, <), and "
        "logical operators (and, or, not).",
        syntax="result = value1 operator value2",
        code='a = 10\nb = 3\nprint(a + b)\nprint(a % b)\nprint(a > b and b > 0)',
        output="13\n1\nTrue",
        notes="The // operator performs floor (integer) division, while / always returns a float.",
        mistakes="Confusing = (assignment) with == (comparison) — this is one of the most "
                  "common beginner bugs.",
        practice=["Write a program that calculates the area of a rectangle using * .",
                  "Predict the output of 17 % 5 before running it, then check your answer."])

    ch2 = add_chapter(c, "beginner", "Control Flow & Functions", 2)
    add_lesson(ch2, 1, "Input & Output",
        "The input() function lets your program ask the user for information, and print() "
        "displays information back to them. Input from input() is always returned as text "
        "(a string), so you may need to convert it using int() or float().",
        syntax='variable = input("prompt text")',
        code='name = input("What is your name? ")\nprint("Hello, " + name + "!")',
        output="What is your name? Asha\nHello, Asha!",
        notes="Use int(input(...)) directly when you expect the user to type a whole number.",
        mistakes="Trying to do math on input() without converting it first, e.g. "
                  "input() + 5 will raise an error because input() returns a string.",
        practice=["Write a program that asks for two numbers and prints their sum.",
                  "Ask the user for their age and print how old they'll be in 10 years."])
    add_lesson(ch2, 2, "Conditional Statements",
        "Conditional statements let your program make decisions. The if statement runs a "
        "block of code only when a condition is True. You can chain conditions with elif "
        "and provide a fallback with else.",
        syntax="if condition:\n    # code\nelif condition:\n    # code\nelse:\n    # code",
        code='marks = 72\nif marks >= 90:\n    print("Grade A")\nelif marks >= 60:\n    print("Grade B")\nelse:\n    print("Grade C")',
        output="Grade B",
        notes="Python uses indentation (usually 4 spaces) instead of curly braces to define "
              "blocks of code — this is not optional, it's part of the syntax.",
        mistakes="Mixing tabs and spaces for indentation, which causes an IndentationError.",
        practice=["Write a program that checks if a number is positive, negative, or zero.",
                  "Write a program that checks if a year is a leap year."])
    add_lesson(ch2, 3, "Loops",
        "Loops let you repeat a block of code multiple times. A for loop is used to "
        "iterate over a sequence (like a range of numbers), while a while loop repeats "
        "as long as a condition stays True.",
        syntax="for item in sequence:\n    # code\n\nwhile condition:\n    # code",
        code='for i in range(1, 6):\n    print(i)\n\ncount = 0\nwhile count < 3:\n    print("Counting:", count)\n    count += 1',
        output="1\n2\n3\n4\n5\nCounting: 0\nCounting: 1\nCounting: 2",
        notes="range(1, 6) generates numbers from 1 up to (but not including) 6.",
        mistakes="Forgetting to update the loop variable in a while loop, which creates an "
                  "infinite loop that never stops.",
        practice=["Print all even numbers between 1 and 20 using a for loop.",
                  "Use a while loop to print the multiplication table of 7."])
    add_lesson(ch2, 4, "Functions",
        "A function is a reusable block of code that performs a specific task. You define "
        "a function once with the def keyword, and call it as many times as you need. "
        "Functions can accept parameters and return values.",
        syntax="def function_name(parameters):\n    # code\n    return value",
        code='def add(a, b):\n    return a + b\n\nresult = add(4, 7)\nprint(result)',
        output="11",
        notes="A function without a return statement automatically returns None.",
        mistakes="Forgetting the return keyword and expecting print() inside a function to "
                  "send the value back to the caller — printing and returning are different things.",
        practice=["Write a function that returns the square of a number.",
                  "Write a function that checks whether a number is even or odd."])

    ch3 = add_chapter(c, "intermediate", "Intermediate Python", 1)
    add_lesson(ch3, 1, "Lists & Tuples",
        "A list is an ordered, changeable collection of items, written with square "
        "brackets. A tuple is similar but immutable — once created, it cannot be changed. "
        "Both can hold items of different types.",
        syntax="my_list = [item1, item2, item3]\nmy_tuple = (item1, item2)",
        code='fruits = ["apple", "banana", "cherry"]\nfruits.append("mango")\nprint(fruits[1])\nprint(len(fruits))',
        output="banana\n4",
        notes="List indexing starts at 0, and negative indices count from the end (-1 is the last item).",
        mistakes="Trying to modify a tuple after creating it, e.g. my_tuple[0] = 5 raises a TypeError.",
        practice=["Create a list of 5 numbers and print their sum using sum().",
                  "Create a tuple of your favorite colors and print the second one."])
    add_lesson(ch3, 2, "Dictionaries",
        "A dictionary stores data as key-value pairs, letting you look up a value quickly "
        "using its key instead of a numeric index. Dictionaries are extremely useful for "
        "representing structured, real-world data.",
        syntax='my_dict = {"key1": value1, "key2": value2}',
        code='student = {"name": "Riya", "age": 21, "course": "Python"}\nprint(student["name"])\nstudent["age"] = 22\nprint(student)',
        output="Riya\n{'name': 'Riya', 'age': 22, 'course': 'Python'}",
        notes="Use .get('key') instead of ['key'] to avoid an error when the key might not exist.",
        mistakes="Accessing a key that doesn't exist with square brackets, which raises a KeyError.",
        practice=["Create a dictionary of 3 countries and their capitals, then print one value.",
                  "Loop through a dictionary and print each key and value."])
    add_lesson(ch3, 3, "String Manipulation",
        "Strings have many built-in methods for searching, formatting, and transforming "
        "text — such as changing case, splitting into a list, or replacing substrings.",
        syntax="string.method()",
        code='text = "Hello, Study Hub!"\nprint(text.lower())\nprint(text.replace("Hub", "World"))\nprint(text.split(", "))',
        output="hello, study hub!\nHello, Study World!\n['Hello', 'Study Hub!']",
        notes="Strings are immutable in Python — every string method returns a new string "
              "rather than changing the original.",
        mistakes="Assuming .replace() or .upper() modifies the string in place — you must "
                  "assign the result to a variable to keep it.",
        practice=["Write a program that reverses a string using slicing.",
                  "Count how many times the letter 'a' appears in a given sentence."])
    add_lesson(ch3, 4, "File Handling",
        "Python can read from and write to files on your computer using the built-in "
        "open() function. Using a with block automatically closes the file for you, even "
        "if an error occurs.",
        syntax='with open("file.txt", "mode") as f:\n    # read or write',
        code='with open("notes.txt", "w") as f:\n    f.write("Learning Python!")\n\nwith open("notes.txt", "r") as f:\n    print(f.read())',
        output="Learning Python!",
        notes="Common modes are 'r' (read), 'w' (write, overwrites), and 'a' (append).",
        mistakes="Forgetting to close a file when not using 'with', which can leave the "
                  "file locked or cause data not to be saved.",
        practice=["Write a program that saves a list of 3 tasks to a text file, one per line.",
                  "Read that file back and print each task with a number in front of it."])
    add_lesson(ch3, 5, "Exception Handling",
        "Exceptions are errors that occur while a program runs. Using try/except blocks "
        "lets you catch these errors gracefully instead of letting your program crash.",
        syntax="try:\n    # risky code\nexcept ExceptionType:\n    # handle the error",
        code='try:\n    number = int(input("Enter a number: "))\n    print(10 / number)\nexcept ZeroDivisionError:\n    print("You can\'t divide by zero!")\nexcept ValueError:\n    print("That wasn\'t a valid number.")',
        output="Enter a number: 0\nYou can't divide by zero!",
        notes="You can catch multiple exception types with separate except blocks, and use "
              "a final block to run cleanup code regardless of whether an error happened.",
        mistakes="Using a bare except: that catches every possible error, which can hide "
                  "real bugs in your program.",
        practice=["Write a program that safely divides two numbers entered by the user.",
                  "Handle the case where the user enters text instead of a number."])

    ch4 = add_chapter(c, "intermediate", "Object-Oriented Python", 2)
    add_lesson(ch4, 1, "Classes & Objects",
        "Object-oriented programming (OOP) organizes code around objects that bundle data "
        "(attributes) and behavior (methods) together. A class is a blueprint, and an "
        "object is a specific instance created from that blueprint.",
        syntax="class ClassName:\n    def __init__(self, param):\n        self.attribute = param\n\n    def method(self):\n        # code",
        code='class Student:\n    def __init__(self, name, course):\n        self.name = name\n        self.course = course\n\n    def introduce(self):\n        return f"Hi, I\'m {self.name}, learning {self.course}."\n\ns1 = Student("Kabir", "Python")\nprint(s1.introduce())',
        output="Hi, I'm Kabir, learning Python.",
        notes="__init__ is a special method that runs automatically when a new object is created.",
        mistakes="Forgetting the self parameter in method definitions, which causes a "
                  "TypeError when the method is called.",
        practice=["Create a Car class with brand and speed attributes and a method that describes it.",
                  "Create two different Car objects and call the method on each."])
    add_lesson(ch4, 2, "Inheritance",
        "Inheritance lets a class (the child) reuse and extend the attributes and methods "
        "of another class (the parent), avoiding duplicate code and modeling real-world "
        "relationships between things.",
        syntax="class Child(Parent):\n    def __init__(self, ...):\n        super().__init__(...)",
        code='class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return "..."\n\nclass Dog(Animal):\n    def speak(self):\n        return f"{self.name} says Woof!"\n\nd = Dog("Rex")\nprint(d.speak())',
        output="Rex says Woof!",
        notes="Use super().__init__() inside a child class to call the parent class's constructor.",
        mistakes="Overriding a method completely and forgetting to reuse the parent's "
                  "version with super() when it's still needed.",
        practice=["Create a Shape parent class and a Circle child class that overrides an area() method.",
                  "Explain in a comment why inheritance avoids repeating code."])

    ch5 = add_chapter(c, "advanced", "Advanced Python", 1)
    add_lesson(ch5, 1, "Advanced OOP: Encapsulation & Polymorphism",
        "Encapsulation restricts direct access to an object's internal data (often using a "
        "leading underscore convention), while polymorphism allows different classes to "
        "define methods with the same name that behave differently for each class.",
        syntax="class ClassName:\n    def __init__(self):\n        self._protected = value\n        self.__private = value",
        code='class Shape:\n    def area(self):\n        return 0\n\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n    def area(self):\n        return self.side ** 2\n\nclass Circle(Shape):\n    def __init__(self, radius):\n        self.radius = radius\n    def area(self):\n        return 3.14 * self.radius ** 2\n\nfor shape in [Square(4), Circle(3)]:\n    print(shape.area())',
        output="16\n28.26",
        notes="Python doesn't enforce true private variables — a double underscore just "
              "triggers name-mangling, it's a convention rather than a hard restriction.",
        mistakes="Assuming double-underscore attributes are completely inaccessible from "
                  "outside the class — they can still be reached with extra effort.",
        practice=["Create three shape classes that each implement area() differently.",
                  "Write a function that accepts any shape object and prints its area — that's polymorphism in action."])
    add_lesson(ch5, 2, "Data Structures in Python",
        "Beyond lists and dictionaries, Python can implement classic data structures like "
        "stacks (last in, first out) and queues (first in, first out) using lists or the "
        "built-in collections.deque for better performance.",
        syntax="from collections import deque\nqueue = deque()",
        code='stack = []\nstack.append(1)\nstack.append(2)\nstack.append(3)\nprint(stack.pop())   # last in, first out\n\nfrom collections import deque\nqueue = deque()\nqueue.append("a")\nqueue.append("b")\nprint(queue.popleft())  # first in, first out',
        output="3\na",
        notes="Use collections.deque instead of a plain list for queues — removing from the "
              "front of a list is much slower than removing from a deque.",
        mistakes="Using list.pop(0) to simulate a queue on large data — this is inefficient "
                  "because every remaining item has to shift over.",
        practice=["Implement a simple stack-based function that checks if brackets in a string are balanced.",
                  "Implement a queue that simulates people waiting in line."])
    add_lesson(ch5, 3, "Algorithms & Complexity",
        "An algorithm is a step-by-step procedure for solving a problem. Big O notation "
        "describes how an algorithm's running time grows as the input size grows, which "
        "helps you compare the efficiency of different approaches.",
        syntax="# Big O examples: O(1), O(n), O(log n), O(n^2)",
        code='def linear_search(items, target):\n    for i, value in enumerate(items):\n        if value == target:\n            return i\n    return -1\n\ndef binary_search(sorted_items, target):\n    low, high = 0, len(sorted_items) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if sorted_items[mid] == target:\n            return mid\n        elif sorted_items[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n\nprint(binary_search([1,3,5,7,9,11], 7))',
        output="3",
        notes="Binary search runs in O(log n) time but only works on sorted data — always "
              "check that precondition before using it.",
        mistakes="Using binary search on unsorted data, which produces incorrect results silently.",
        practice=["Implement linear search and time how many comparisons it takes on a 100-item list.",
                  "Explain in your own words why binary search is faster than linear search."])
    add_lesson(ch5, 4, "Decorators & Generators",
        "A decorator is a function that wraps another function to add extra behavior "
        "without changing its code. A generator is a special function that yields values "
        "one at a time, which is memory-efficient for large sequences.",
        syntax="@decorator_name\ndef function():\n    ...\n\ndef generator():\n    yield value",
        code='def logger(func):\n    def wrapper(*args):\n        print(f"Calling {func.__name__}")\n        return func(*args)\n    return wrapper\n\n@logger\ndef greet(name):\n    return f"Hello, {name}"\n\nprint(greet("Dev"))\n\ndef countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nfor num in countdown(3):\n    print(num)',
        output="Calling greet\nHello, Dev\n3\n2\n1",
        notes="Generators don't compute all their values upfront — each value is produced "
              "only when requested, which saves memory for large or infinite sequences.",
        mistakes="Calling a generator function and expecting it to return a list directly — "
                  "it returns a generator object that must be iterated over.",
        practice=["Write a decorator that measures how long a function takes to run.",
                  "Write a generator that yields the first n Fibonacci numbers."])

    quiz1 = add_quiz("Getting Started with Python — Chapter Quiz", "quiz", chapter_id=ch1.id, pass_percent=60, questions=[
        ("Which function is used to display output in Python?",
         ["print()", "echo()", "display()", "output()"], 0),
        ("What data type is the value True?",
         ["Boolean", "String", "Integer", "Float"], 0),
        ("What does the % operator do?",
         ["Returns the remainder of a division", "Multiplies two numbers", "Raises to a power", "Divides two numbers"], 0),
        ("Which of these is a valid variable name?",
         ["student_1", "1student", "student-1", "student 1"], 0),
    ])

    exam = add_quiz("Python Final Exam", "exam", course_id=c.id, pass_percent=60, questions=[
        ("What keyword is used to define a function in Python?",
         ["def", "function", "func", "define"], 0),
        ("Which loop is best when you know exactly how many times to repeat?",
         ["for", "while", "do-while", "repeat"], 0),
        ("What does len([1,2,3]) return?",
         ["3", "2", "1", "Error"], 0),
        ("Which collection type is immutable?",
         ["Tuple", "List", "Dictionary", "Set"], 0),
        ("What is used to catch errors in Python?",
         ["try/except", "catch/throw", "error/handle", "if/else"], 0),
        ("What does OOP stand for?",
         ["Object-Oriented Programming", "Order Of Precedence", "Open Output Protocol", "Object Output Path"], 0),
    ])


def seed_simple_course(name, slug, icon, tagline, description, lessons, quiz_questions):
    """Helper for courses that only need a single, solid beginner chapter for now."""
    c = add_course(name, slug, icon, tagline, description)
    if c.chapters:
        return
    chapter = add_chapter(c, "beginner", f"{name} Fundamentals", 1)
    for i, l in enumerate(lessons, start=1):
        add_lesson(chapter, i, **l)
    add_quiz(f"{name} Final Exam", "exam", course_id=c.id, pass_percent=60, questions=quiz_questions)


def seed_c():
    seed_simple_course(
        "C", "c", "🅲",
        "The foundational language behind operating systems and compilers.",
        "C is a powerful, low-level language that teaches you how computers really work — "
        "memory, pointers, and performance. It remains the foundation for operating "
        "systems, embedded devices, and countless other languages.",
        lessons=[
            dict(title="Introduction & Setup", explanation=
                 "C is a compiled, procedural language created in the 1970s that gives you "
                 "close control over memory and hardware. To run C code, you need a compiler "
                 "such as GCC, which turns your source file into an executable program.",
                 syntax="gcc program.c -o program\n./program",
                 code='#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
                 output="Hello, World!",
                 notes="Every C program must have a main() function — it's the entry point where execution begins.",
                 mistakes="Forgetting the semicolon at the end of a statement, which causes a compiler error.",
                 practice=["Install GCC and compile a Hello World program.", "Modify the program to print your name."]),
            dict(title="Variables & Data Types", explanation=
                 "Unlike Python, C requires you to declare a variable's type before using it. "
                 "Common types include int (whole numbers), float (decimals), char (a single "
                 "character), and double (double-precision decimals).",
                 syntax="type variableName = value;",
                 code='int age = 20;\nfloat price = 9.99;\nchar grade = \'A\';\nprintf("%d %f %c", age, price, grade);',
                 output="20 9.990000 A",
                 notes="Format specifiers like %d, %f, and %c tell printf() how to display each data type.",
                 mistakes="Using the wrong format specifier for a type, which prints garbage values.",
                 practice=["Declare variables for your age and height and print them.", "Try printing an int using the %f specifier and observe what happens."]),
            dict(title="Operators & Expressions", explanation=
                 "C supports arithmetic, relational, and logical operators similar to most "
                 "languages, plus increment/decrement operators (++ and --) that are "
                 "especially common in C.",
                 syntax="result = value1 operator value2;",
                 code='int a = 10, b = 3;\nprintf("%d\\n", a + b);\nprintf("%d\\n", a % b);\na++;\nprintf("%d", a);',
                 output="13\n1\n11",
                 notes="++a increments before use, while a++ increments after the current value is used.",
                 mistakes="Confusing = with == inside an if condition, which silently assigns instead of comparing.",
                 practice=["Write a program that swaps two numbers using a temporary variable.", "Predict the output of a++ vs ++a in a print statement."]),
            dict(title="Conditions & Loops", explanation=
                 "C uses if/else for decisions and for, while, and do-while loops for "
                 "repetition, all controlled with curly braces {} rather than indentation.",
                 syntax="if (condition) { }\nfor (init; condition; update) { }",
                 code='for (int i = 1; i <= 5; i++) {\n    printf("%d ", i);\n}',
                 output="1 2 3 4 5",
                 notes="A do-while loop always runs its body at least once, since the condition is checked after the first run.",
                 mistakes="Forgetting curly braces for a multi-line if block, which causes only the first line to be conditional.",
                 practice=["Write a program that prints all even numbers from 1 to 20.", "Write a program using do-while that runs at least once even if the condition is false."]),
            dict(title="Functions & Pointers", explanation=
                 "Functions in C let you organize code into reusable blocks with a specific "
                 "return type. Pointers are variables that store the memory address of "
                 "another variable — a defining feature of C that gives you direct memory control.",
                 syntax="returnType functionName(parameters) { }\nint *ptr = &variable;",
                 code='int square(int n) {\n    return n * n;\n}\n\nint main() {\n    int x = 5;\n    int *p = &x;\n    printf("%d %d", square(x), *p);\n    return 0;\n}',
                 output="25 5",
                 notes="The & operator gets a variable's address, and * dereferences a pointer to access its value.",
                 mistakes="Using an uninitialized pointer, which points to a random memory location and can crash your program.",
                 practice=["Write a function that returns the cube of a number.", "Declare a pointer to an int variable and print the value it points to."]),
        ],
        quiz_questions=[
            ("Which function is the entry point of every C program?", ["main()", "start()", "run()", "init()"], 0),
            ("What symbol ends most statements in C?", [";", ":", ".", ","], 0),
            ("What does the & operator do with a variable?", ["Gets its memory address", "Adds one to it", "Compares two values", "Declares a constant"], 0),
            ("Which loop always executes at least once?", ["do-while", "for", "while", "if"], 0),
        ])


def seed_cpp():
    seed_simple_course(
        "C++", "cpp", "➕",
        "C, plus object-oriented programming and the standard library.",
        "C++ extends C with object-oriented features, making it a popular choice for game "
        "engines, high-performance software, and competitive programming, while still "
        "giving you low-level control over memory.",
        lessons=[
            dict(title="Introduction & Setup", explanation=
                 "C++ is a compiled language that builds on C by adding classes, objects, "
                 "and a rich standard library. You'll typically compile C++ with g++ and run "
                 "the resulting executable.",
                 syntax="g++ program.cpp -o program\n./program",
                 code='#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}',
                 output="Hello, World!",
                 notes="cout is used for output and cin for input, both from the <iostream> library.",
                 mistakes="Forgetting to #include <iostream> before using cout, which causes a compiler error.",
                 practice=["Compile and run a Hello World C++ program.", "Modify it to print two lines of text."]),
            dict(title="Variables & Data Types", explanation=
                 "Like C, C++ requires explicit type declarations. It supports the same "
                 "core types (int, float, double, char, bool) with added conveniences like "
                 "the string type from the standard library.",
                 syntax="type variableName = value;",
                 code='#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    int age = 20;\n    string name = "Aarav";\n    cout << name << " is " << age;\n    return 0;\n}',
                 output="Aarav is 20",
                 notes="Include <string> to use the convenient string type instead of raw character arrays.",
                 mistakes="Using = for string comparison instead of ==, or forgetting to include <string>.",
                 practice=["Declare variables of each core type and print them with cout.", "Store your full name in a string variable and print its length using .length()."]),
            dict(title="Conditions & Loops", explanation=
                 "C++ conditions and loops work the same way as C: if/else statements and "
                 "for, while, and do-while loops, using curly braces to define code blocks.",
                 syntax="if (condition) { } else { }",
                 code='int marks = 85;\nif (marks >= 90) {\n    cout << "A";\n} else if (marks >= 75) {\n    cout << "B";\n} else {\n    cout << "C";\n}',
                 output="B",
                 notes="C++ also supports the ternary operator: condition ? valueIfTrue : valueIfFalse.",
                 mistakes="Missing braces around multi-statement blocks, causing only the first statement to run conditionally.",
                 practice=["Write a program that classifies a number as positive, negative, or zero.", "Rewrite one of your if/else statements using the ternary operator."]),
            dict(title="Functions", explanation=
                 "Functions in C++ are declared with a return type, name, and parameters, "
                 "just like C, but C++ also supports function overloading — multiple "
                 "functions with the same name but different parameter types.",
                 syntax="returnType functionName(parameters) { return value; }",
                 code='int add(int a, int b) { return a + b; }\ndouble add(double a, double b) { return a + b; }\n\nint main() {\n    cout << add(2, 3) << " " << add(2.5, 1.5);\n    return 0;\n}',
                 output="5 4",
                 notes="Overloaded functions must differ in the number or type of their parameters, not just the return type.",
                 mistakes="Trying to overload two functions that differ only by return type, which C++ does not allow.",
                 practice=["Write an overloaded function called multiply that works for both int and double.", "Write a function that returns the larger of two numbers."]),
            dict(title="Classes & Objects", explanation=
                 "A class bundles data (member variables) and behavior (member functions) "
                 "into a single blueprint. Objects are created from a class, and this is the "
                 "core idea behind object-oriented programming in C++.",
                 syntax="class ClassName {\npublic:\n    type memberVariable;\n    returnType memberFunction() { }\n};",
                 code='class Car {\npublic:\n    string brand;\n    void honk() {\n        cout << brand << " says Beep!";\n    }\n};\n\nint main() {\n    Car myCar;\n    myCar.brand = "Toyota";\n    myCar.honk();\n    return 0;\n}',
                 output="Toyota says Beep!",
                 notes="Members are private by default in C++ classes — use the public: keyword to make them accessible from outside.",
                 mistakes="Forgetting the public: access specifier and then being unable to access members from outside the class.",
                 practice=["Create a Student class with a name and a method that introduces the student.", "Create two Student objects with different names and call the method on each."]),
        ],
        quiz_questions=[
            ("Which header is needed for cout and cin?", ["<iostream>", "<stdio.h>", "<string.h>", "<cstdlib>"], 0),
            ("What C++ feature lets multiple functions share a name with different parameters?", ["Function overloading", "Inheritance", "Polymorphism", "Encapsulation"], 0),
            ("What is the default access level of class members in C++?", ["Private", "Public", "Protected", "Global"], 0),
            ("Which symbol is used to output data with cout?", ["<<", ">>", "->", "::"], 0),
        ])


def seed_java():
    seed_simple_course(
        "Java", "java", "☕",
        "Write once, run anywhere — a top choice for enterprise software.",
        "Java is a class-based, object-oriented language used heavily in enterprise "
        "software, Android apps, and large-scale backend systems, known for its "
        "portability across platforms via the Java Virtual Machine.",
        lessons=[
            dict(title="Introduction & Setup", explanation=
                 "Java code is compiled into bytecode that runs on the Java Virtual Machine "
                 "(JVM), which is why Java programs can run on any device with a JVM "
                 "installed. Every Java program lives inside a class.",
                 syntax="javac Program.java\njava Program",
                 code='public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
                 output="Hello, World!",
                 notes="The file name must exactly match the public class name, including capitalization.",
                 mistakes="Naming the file differently from the public class, which causes a compiler error.",
                 practice=["Install the JDK and run a Hello World Java program.", "Print your name and course on two separate lines."]),
            dict(title="Variables & Data Types", explanation=
                 "Java is statically typed, so every variable must be declared with a "
                 "specific type such as int, double, char, or boolean before it's used.",
                 syntax="type variableName = value;",
                 code='int age = 21;\ndouble price = 49.99;\nboolean isActive = true;\nSystem.out.println(age + " " + price + " " + isActive);',
                 output="21 49.99 true",
                 notes="Java has both primitive types (int, double) and object types (String, Integer).",
                 mistakes="Trying to assign a decimal value to an int variable without casting, which causes a compile error.",
                 practice=["Declare variables of each primitive type and print them.", "Try assigning 9.5 to an int variable and observe the compiler error."]),
            dict(title="Conditions & Loops", explanation=
                 "Java's if/else statements and for/while loops closely resemble C and "
                 "C++, using curly braces for code blocks and standard comparison operators.",
                 syntax="if (condition) { } \nfor (int i = 0; i < n; i++) { }",
                 code='for (int i = 1; i <= 5; i++) {\n    if (i % 2 == 0) {\n        System.out.println(i + " is even");\n    }\n}',
                 output="2 is even\n4 is even",
                 notes="Java also has an enhanced for-each loop for iterating over arrays and collections directly.",
                 mistakes="Using = instead of == inside an if condition, which in Java causes a compile-time type error (a helpful safety net).",
                 practice=["Print all numbers from 1 to 10 that are divisible by 3.", "Rewrite a for loop over an array using the enhanced for-each syntax."]),
            dict(title="Methods", explanation=
                 "Methods (Java's term for functions) are defined inside a class and must "
                 "specify a return type. The static keyword means a method belongs to the "
                 "class itself rather than to an object instance.",
                 syntax="returnType methodName(parameters) { return value; }",
                 code='public class Main {\n    static int add(int a, int b) {\n        return a + b;\n    }\n    public static void main(String[] args) {\n        System.out.println(add(4, 5));\n    }\n}',
                 output="9",
                 notes="A method that returns nothing must be declared with the void return type.",
                 mistakes="Forgetting static on a helper method called directly from main(), which causes a compile error.",
                 practice=["Write a static method that returns the maximum of two numbers.", "Write a static method that checks whether a number is prime."]),
            dict(title="Classes & Objects", explanation=
                 "Java is fundamentally object-oriented — classes define blueprints with "
                 "fields and methods, and objects are created from them using the new "
                 "keyword, with a constructor to initialize their state.",
                 syntax="class ClassName {\n    ClassName(parameters) { }\n}\nClassName obj = new ClassName(args);",
                 code='class Student {\n    String name;\n    Student(String name) {\n        this.name = name;\n    }\n    void introduce() {\n        System.out.println("Hi, I\'m " + name);\n    }\n}\n\npublic class Main {\n    public static void main(String[] args) {\n        Student s = new Student("Priya");\n        s.introduce();\n    }\n}',
                 output="Hi, I'm Priya",
                 notes="The this keyword refers to the current object, and is used to distinguish fields from parameters with the same name.",
                 mistakes="Forgetting the new keyword when creating an object, which causes a compile error.",
                 practice=["Create a Book class with a title and author, plus a method to describe it.", "Create two Book objects and call the describe method on each."]),
        ],
        quiz_questions=[
            ("What must the Java file name match?", ["The public class name", "The package name", "The main method name", "Anything you like"], 0),
            ("What keyword creates a new object in Java?", ["new", "create", "make", "object"], 0),
            ("What does the JVM stand for?", ["Java Virtual Machine", "Java Variable Method", "Java Verified Module", "Java Visual Manager"], 0),
            ("Which method is the entry point of a Java application?", ["main()", "start()", "run()", "init()"], 0),
        ])


def seed_javascript():
    seed_simple_course(
        "JavaScript", "javascript", "🟨",
        "The language of the web — runs in every browser.",
        "JavaScript brings web pages to life, handling everything from simple button "
        "clicks to complex, interactive applications. It runs natively in every web "
        "browser and, via Node.js, on servers too.",
        lessons=[
            dict(title="Introduction & Setup", explanation=
                 "JavaScript runs directly in the browser, so you can start writing it with "
                 "nothing more than a text editor and your browser's developer console — no "
                 "installation required to get started.",
                 syntax="<script>\n  // your code here\n</script>",
                 code='console.log("Hello, World!");',
                 output="Hello, World!",
                 notes="Open your browser's developer tools (F12) and go to the Console tab to run JavaScript instantly.",
                 mistakes="Forgetting that browser console output and a webpage's visible content are different things — console.log only prints to the console.",
                 practice=["Open your browser console and print your name with console.log.", "Create an HTML file with a <script> tag that prints a message."]),
            dict(title="Variables & Data Types", explanation=
                 "JavaScript variables are declared with let (changeable), const (constant), "
                 "or var (older syntax). Common data types include numbers, strings, "
                 "booleans, arrays, and objects.",
                 syntax="let variableName = value;\nconst constantName = value;",
                 code='let age = 22;\nconst name = "Meera";\nlet isStudent = true;\nconsole.log(name, age, isStudent);',
                 output="Meera 22 true",
                 notes="Prefer const by default, and use let only when you know the variable's value will change.",
                 mistakes="Trying to reassign a const variable, which throws a TypeError.",
                 practice=["Declare a let variable and reassign it to a new value.", "Try reassigning a const variable and read the error message you get."]),
            dict(title="Conditions & Loops", explanation=
                 "JavaScript uses if/else statements and for/while loops similar to other "
                 "C-style languages, plus the very useful strict equality operator === "
                 "which checks both value and type.",
                 syntax="if (condition) { } \nfor (let i = 0; i < n; i++) { }",
                 code='let score = 85;\nif (score >= 90) {\n    console.log("A");\n} else if (score >= 75) {\n    console.log("B");\n} else {\n    console.log("C");\n}',
                 output="B",
                 notes="Always prefer === over == — the loose == operator performs type coercion, which can cause unexpected bugs.",
                 mistakes="Using == instead of ===, e.g. '5' == 5 is true but '5' === 5 is false.",
                 practice=["Write a program that checks if a number is even or odd.", "Compare '0' == 0 and '0' === 0 and explain the difference."]),
            dict(title="Functions", explanation=
                 "Functions in JavaScript can be declared in several ways, including "
                 "traditional function declarations and modern arrow functions, which offer "
                 "a shorter syntax.",
                 syntax="function name(params) { return value; }\nconst name = (params) => value;",
                 code='function add(a, b) {\n    return a + b;\n}\n\nconst multiply = (a, b) => a * b;\n\nconsole.log(add(2, 3), multiply(2, 3));',
                 output="5 6",
                 notes="Arrow functions with a single expression automatically return that expression's value, without needing the return keyword.",
                 mistakes="Forgetting parentheses around parameters in an arrow function when there are zero or multiple parameters.",
                 practice=["Write an arrow function that returns the square of a number.", "Rewrite a traditional function as an arrow function."]),
            dict(title="Arrays & Objects", explanation=
                 "Arrays store ordered lists of values, while objects store data as "
                 "key-value pairs — together they're the two most important data "
                 "structures for organizing information in JavaScript.",
                 syntax="let arr = [item1, item2];\nlet obj = { key: value };",
                 code='const fruits = ["apple", "banana", "mango"];\nfruits.push("kiwi");\nconsole.log(fruits[1]);\n\nconst student = { name: "Dev", age: 20 };\nconsole.log(student.name);',
                 output="banana\nDev",
                 notes="Use array methods like .map(), .filter(), and .forEach() to work with lists of data cleanly.",
                 mistakes="Confusing dot notation (obj.key) with bracket notation on arrays, or accessing an array index that doesn't exist and getting undefined.",
                 practice=["Create an array of 5 numbers and use .filter() to get only the even ones.", "Create an object representing yourself with 3 properties and print each one."]),
        ],
        quiz_questions=[
            ("Which keyword declares a constant that can't be reassigned?", ["const", "let", "var", "final"], 0),
            ("Which operator checks both value and type?", ["===", "==", "=", "!=="], 0),
            ("Which method adds an item to the end of an array?", [".push()", ".add()", ".append()", ".insert()"], 0),
            ("What does console.log() do?", ["Prints output to the browser console", "Saves data to a file", "Creates a new variable", "Sends data to a server"], 0),
        ])


def seed_html():
    seed_simple_course(
        "HTML", "html", "🌐",
        "The building blocks of every web page.",
        "HTML (HyperText Markup Language) structures the content of every web page — "
        "headings, paragraphs, links, images, and more — using a system of nested tags.",
        lessons=[
            dict(title="Introduction & Document Structure", explanation=
                 "Every HTML document follows a standard structure: a doctype declaration, "
                 "an html root element, a head for metadata, and a body for visible content.",
                 syntax="<!DOCTYPE html>\n<html>\n<head></head>\n<body></body>\n</html>",
                 code='<!DOCTYPE html>\n<html>\n<head>\n    <title>My Page</title>\n</head>\n<body>\n    <h1>Hello, World!</h1>\n</body>\n</html>',
                 output="Renders a webpage with the title \"My Page\" and a heading \"Hello, World!\"",
                 notes="The <title> tag controls the text shown in the browser tab, not on the page itself.",
                 mistakes="Forgetting to close tags properly, which can cause the browser to render the page incorrectly.",
                 practice=["Create a basic HTML file with a title and one heading.", "Add a paragraph of text describing yourself below the heading."]),
            dict(title="Text Elements & Headings", explanation=
                 "HTML provides heading tags (h1 through h6) for titles of decreasing "
                 "importance, and the p tag for paragraphs of regular text.",
                 syntax="<h1>Main Heading</h1>\n<p>Paragraph text</p>",
                 code='<h1>Welcome to STUDY HUB</h1>\n<h2>Learn to Code</h2>\n<p>This is a paragraph of text.</p>',
                 output="Displays a large heading, a smaller subheading, and a paragraph below them.",
                 notes="Use only one <h1> per page for the main title, and use lower-level headings to structure sections.",
                 mistakes="Skipping heading levels (e.g. jumping from h1 straight to h4), which harms both readability and accessibility.",
                 practice=["Create a page with an h1, an h2, and two paragraphs.", "Add bold and italic text using <strong> and <em>."]),
            dict(title="Links & Images", explanation=
                 "The anchor tag <a> creates hyperlinks to other pages, and the <img> tag "
                 "embeds images, using the src attribute to point to the image file or URL.",
                 syntax='<a href="url">link text</a>\n<img src="image.jpg" alt="description">',
                 code='<a href="https://example.com">Visit Example</a>\n<img src="photo.jpg" alt="A profile photo">',
                 output="Displays a clickable link and an image on the page.",
                 notes="Always include a meaningful alt attribute on images — it's used by screen readers and shown if the image fails to load.",
                 mistakes="Leaving the alt attribute empty or missing, which hurts accessibility and SEO.",
                 practice=["Add a link to your favorite website on your page.", "Add an image with a descriptive alt attribute."]),
            dict(title="Lists & Tables", explanation=
                 "HTML offers ordered lists (<ol>), unordered lists (<ul>), and tables "
                 "(<table>) for organizing grouped or tabular data on a page.",
                 syntax="<ul><li>item</li></ul>\n<table><tr><td>cell</td></tr></table>",
                 code='<ul>\n    <li>Python</li>\n    <li>JavaScript</li>\n</ul>\n<table>\n    <tr><th>Language</th><th>Level</th></tr>\n    <tr><td>Python</td><td>Beginner</td></tr>\n</table>',
                 output="Displays a bulleted list and a simple table with headers and one data row.",
                 notes="Use <th> for header cells and <td> for regular data cells inside a table row (<tr>).",
                 mistakes="Using tables for page layout instead of actual tabular data — modern CSS layout tools are the correct choice for that.",
                 practice=["Create an unordered list of 3 of your favorite courses.", "Create a table with 2 columns and 3 rows of sample data."]),
            dict(title="Forms", explanation=
                 "Forms let users submit data, such as sign-up details or search queries, "
                 "using input fields, buttons, and the <form> element to group them together.",
                 syntax='<form>\n  <input type="text" name="fieldName">\n  <button type="submit">Submit</button>\n</form>',
                 code='<form>\n    <label for="email">Email:</label>\n    <input type="email" id="email" name="email">\n    <button type="submit">Sign Up</button>\n</form>',
                 output="Displays a labeled email input field and a submit button.",
                 notes="Always pair an <input> with a <label> using matching for/id attributes — it improves both usability and accessibility.",
                 mistakes="Forgetting the name attribute on inputs, which means the field's data won't be submitted with the form.",
                 practice=["Create a simple sign-up form with a name field and an email field.", "Add a password input field with type=\"password\"."]),
        ],
        quiz_questions=[
            ("Which tag defines the largest heading?", ["<h1>", "<h6>", "<head>", "<title>"], 0),
            ("Which attribute provides alternative text for an image?", ["alt", "src", "title", "text"], 0),
            ("Which tag creates a hyperlink?", ["<a>", "<link>", "<href>", "<url>"], 0),
            ("Which tag is used to create an unordered list?", ["<ul>", "<ol>", "<li>", "<list>"], 0),
        ])


def seed_css():
    seed_simple_course(
        "CSS", "css", "🎨",
        "Style and layout for the web — colors, spacing, and responsive design.",
        "CSS (Cascading Style Sheets) controls how HTML content looks — colors, fonts, "
        "spacing, and layout — and is essential for building visually appealing, "
        "responsive websites.",
        lessons=[
            dict(title="Introduction & Selectors", explanation=
                 "CSS rules select HTML elements and apply styles to them. Selectors can "
                 "target elements by tag name, class (.classname), or id (#idname).",
                 syntax="selector {\n    property: value;\n}",
                 code='h1 {\n    color: navy;\n}\n.highlight {\n    background-color: yellow;\n}\n#main-title {\n    font-size: 32px;\n}',
                 output="Styles all h1 elements navy, elements with class \"highlight\" get a yellow background, and the element with id \"main-title\" gets larger text.",
                 notes="IDs should be unique per page, while a class can be reused on many elements.",
                 mistakes="Using an ID selector when you actually need to style multiple elements — use a class instead.",
                 practice=["Style all paragraphs on a page to be a specific color.", "Create a class called .card and apply it to two different elements."]),
            dict(title="Box Model", explanation=
                 "Every HTML element is treated as a box made up of content, padding "
                 "(space inside the border), border, and margin (space outside the "
                 "border) — understanding this model is key to CSS layout.",
                 syntax="selector {\n    padding: value;\n    border: value;\n    margin: value;\n}",
                 code='.box {\n    padding: 16px;\n    border: 2px solid gray;\n    margin: 20px;\n    width: 200px;\n}',
                 output="Renders a 200px-wide box with 16px of inner spacing, a gray border, and 20px of outer spacing.",
                 notes="Use box-sizing: border-box to make padding and border included within the declared width, avoiding surprises.",
                 mistakes="Forgetting that padding and border add to an element's total rendered width by default, causing unexpected layout overflow.",
                 practice=["Create a box with padding, a border, and a margin, and view it in the browser.", "Add box-sizing: border-box and observe how the box's total size changes."]),
            dict(title="Colors, Fonts & Text", explanation=
                 "CSS controls typography with properties like color, font-family, "
                 "font-size, and font-weight, letting you fully customize how text appears.",
                 syntax="selector {\n    color: value;\n    font-family: value;\n    font-size: value;\n}",
                 code='body {\n    font-family: Arial, sans-serif;\n    color: #333333;\n}\nh1 {\n    font-size: 2rem;\n    font-weight: 700;\n}',
                 output="Sets a sans-serif font and dark gray color for all body text, with large, bold h1 headings.",
                 notes="Using rem units for font sizes keeps text scalable relative to the user's browser settings, improving accessibility.",
                 mistakes="Relying on a single font without a fallback — always list a generic fallback family (like sans-serif) after your preferred font.",
                 practice=["Change the font and color of all paragraph text on a page.", "Set your h1 to use rem units instead of pixels."]),
            dict(title="Flexbox Layout", explanation=
                 "Flexbox is a modern CSS layout system for arranging items in a row or "
                 "column, distributing space between them, and aligning them precisely — "
                 "ideal for navigation bars and card layouts.",
                 syntax="display: flex;\njustify-content: value;\nalign-items: value;",
                 code='.nav {\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n}',
                 output="Arranges the navigation's child elements in a row, spaced evenly apart and vertically centered.",
                 notes="justify-content controls spacing along the main axis, while align-items controls alignment along the cross axis.",
                 mistakes="Forgetting display: flex on the parent container — flex properties on children only work once the parent is a flex container.",
                 practice=["Create a row of 3 cards using flexbox that are evenly spaced.", "Center a single box both horizontally and vertically using flexbox."]),
            dict(title="Responsive Design with Media Queries", explanation=
                 "Media queries let you apply different CSS rules depending on the "
                 "screen size, which is essential for making a website look good on "
                 "phones, tablets, and desktops alike.",
                 syntax="@media (max-width: 768px) {\n    selector { property: value; }\n}",
                 code='.container {\n    display: flex;\n}\n\n@media (max-width: 768px) {\n    .container {\n        flex-direction: column;\n    }\n}',
                 output="Displays items in a row on larger screens, and stacks them vertically on screens narrower than 768px.",
                 notes="Design mobile-first when possible: write your base styles for small screens, then add media queries for larger ones.",
                 mistakes="Only testing a design on a desktop browser and never checking how it looks on a narrow, mobile-sized screen.",
                 practice=["Add a media query that changes the background color on small screens.", "Make a 3-column layout collapse to 1 column below 600px width."]),
        ],
        quiz_questions=[
            ("Which selector targets an element with a specific class?", [".classname", "#classname", "classname", "*classname"], 0),
            ("What does the box model NOT include?", ["Animation", "Padding", "Border", "Margin"], 0),
            ("Which property turns an element into a flex container?", ["display: flex;", "position: flex;", "flex: true;", "layout: flex;"], 0),
            ("What are media queries used for?", ["Applying styles based on screen size", "Loading external fonts", "Declaring variables", "Selecting HTML elements by tag"], 0),
        ])


def seed_sql():
    seed_simple_course(
        "SQL", "sql", "🗄️",
        "Query and manage relational databases with confidence.",
        "SQL (Structured Query Language) is used to create, read, update, and delete data "
        "in relational databases — an essential skill for nearly every backend and data role.",
        lessons=[
            dict(title="Introduction & SELECT", explanation=
                 "SQL organizes data into tables made of rows and columns. The SELECT "
                 "statement is the most common command, used to retrieve data from one or "
                 "more tables.",
                 syntax="SELECT column1, column2 FROM table_name;",
                 code="SELECT name, age FROM students;",
                 output="Returns a result set with the name and age columns for every row in the students table.",
                 notes="Use SELECT * to retrieve all columns, though it's best practice to select only the columns you actually need.",
                 mistakes="Forgetting the semicolon at the end of a SQL statement in tools that require it.",
                 practice=["Write a query that selects all columns from a table called courses.", "Write a query that selects only the name column from a students table."]),
            dict(title="Filtering with WHERE", explanation=
                 "The WHERE clause filters rows based on a condition, so you only get back "
                 "the data that matches what you're looking for.",
                 syntax="SELECT columns FROM table WHERE condition;",
                 code="SELECT name FROM students WHERE age > 18;",
                 output="Returns the names of every student whose age is greater than 18.",
                 notes="Combine multiple conditions with AND and OR, and use parentheses to control the order they're evaluated in.",
                 mistakes="Using = to compare against NULL, which never matches — use IS NULL instead.",
                 practice=["Write a query that finds all students older than 20.", "Write a query that finds students named 'Riya' using WHERE name = 'Riya'."]),
            dict(title="Sorting & Limiting Results", explanation=
                 "ORDER BY sorts your result set by one or more columns, and LIMIT "
                 "restricts how many rows are returned — useful for finding top results.",
                 syntax="SELECT columns FROM table ORDER BY column ASC|DESC LIMIT n;",
                 code="SELECT name, score FROM students ORDER BY score DESC LIMIT 3;",
                 output="Returns the names and scores of the top 3 students, sorted from highest to lowest score.",
                 notes="ASC (ascending) is the default sort order, so it can be left out if you want smallest-to-largest.",
                 mistakes="Forgetting DESC when you want the highest values first — by default ORDER BY sorts smallest to largest.",
                 practice=["Write a query that lists students sorted by age, youngest first.", "Write a query that returns only the top 5 highest-scoring students."]),
            dict(title="INSERT, UPDATE & DELETE", explanation=
                 "Besides reading data, SQL lets you modify it: INSERT adds new rows, "
                 "UPDATE changes existing rows, and DELETE removes rows — all central to "
                 "managing a database over time.",
                 syntax="INSERT INTO table (col1, col2) VALUES (val1, val2);\nUPDATE table SET col = value WHERE condition;\nDELETE FROM table WHERE condition;",
                 code="INSERT INTO students (name, age) VALUES ('Kabir', 19);\nUPDATE students SET age = 20 WHERE name = 'Kabir';\nDELETE FROM students WHERE name = 'Kabir';",
                 output="Adds a new student row, then updates their age, then removes that row from the table.",
                 notes="Always use a WHERE clause with UPDATE and DELETE — omitting it will affect every single row in the table.",
                 mistakes="Running an UPDATE or DELETE without a WHERE clause, accidentally modifying or deleting all the data in a table.",
                 practice=["Write an INSERT statement adding a new course to a courses table.", "Write an UPDATE statement that changes one student's age."]),
            dict(title="JOINs", explanation=
                 "A JOIN combines rows from two or more tables based on a related column, "
                 "which is essential since relational databases split data across "
                 "multiple, connected tables.",
                 syntax="SELECT columns FROM table1\nJOIN table2 ON table1.id = table2.table1_id;",
                 code="SELECT students.name, courses.title\nFROM students\nJOIN enrollments ON students.id = enrollments.student_id\nJOIN courses ON enrollments.course_id = courses.id;",
                 output="Returns each student's name alongside the title of every course they're enrolled in.",
                 notes="An INNER JOIN (the default) only returns rows that match in both tables; a LEFT JOIN also includes unmatched rows from the first table.",
                 mistakes="Joining tables on the wrong columns, which can produce duplicated or completely incorrect result rows.",
                 practice=["Write a JOIN query that lists each order alongside the customer's name.", "Explain in a comment the difference between an INNER JOIN and a LEFT JOIN."]),
        ],
        quiz_questions=[
            ("Which statement retrieves data from a table?", ["SELECT", "GET", "FETCH", "PULL"], 0),
            ("Which clause filters rows based on a condition?", ["WHERE", "FILTER", "IF", "HAVING"], 0),
            ("Which statement adds a new row to a table?", ["INSERT", "ADD", "CREATE", "NEW"], 0),
            ("What does a JOIN do?", ["Combines rows from two or more related tables", "Deletes a table", "Sorts a single table", "Creates a new database"], 0),
        ])


def seed_php():
    seed_simple_course(
        "PHP", "php", "🐘",
        "A widely-used server-side language that powers a huge share of the web.",
        "PHP is a server-side scripting language designed for web development. It powers "
        "a huge portion of the web, including large platforms built on PHP frameworks "
        "and content management systems.",
        lessons=[
            dict(title="Introduction & Setup", explanation=
                 "PHP code runs on the server and outputs HTML to the browser. A PHP file "
                 "mixes regular HTML with PHP code wrapped in <?php ?> tags, and files "
                 "typically end in .php.",
                 syntax="<?php\n    // your code here\n?>",
                 code='<?php\n    echo "Hello, World!";\n?>',
                 output="Hello, World!",
                 notes="To run PHP locally, you need a PHP-enabled server environment such as XAMPP or the built-in php -S command.",
                 mistakes="Forgetting the closing ?> tag isn't required at the end of a pure-PHP file, and adding it can sometimes cause unwanted output.",
                 practice=["Set up a local PHP environment and run a Hello World script.", "Print your name and today's date using two echo statements."]),
            dict(title="Variables & Data Types", explanation=
                 "PHP variables always start with a dollar sign ($) and don't require an "
                 "explicit type declaration — PHP determines the type automatically based "
                 "on the assigned value.",
                 syntax="$variableName = value;",
                 code='<?php\n    $name = "Sana";\n    $age = 21;\n    $isStudent = true;\n    echo "$name is $age years old.";\n?>',
                 output="Sana is 21 years old.",
                 notes="Double-quoted strings in PHP allow variable interpolation directly inside the string, while single-quoted strings do not.",
                 mistakes="Forgetting the $ sign before a variable name, which PHP will treat as an undefined constant.",
                 practice=["Declare variables for your name and age, and print a sentence using them.", "Try the same output using single quotes and observe the difference."]),
            dict(title="Conditions & Loops", explanation=
                 "PHP supports if/else statements and for, while, and foreach loops, with "
                 "syntax very close to C and JavaScript.",
                 syntax="if (condition) { }\nforeach ($array as $item) { }",
                 code='<?php\n    $fruits = ["apple", "banana", "mango"];\n    foreach ($fruits as $fruit) {\n        echo $fruit . "\\n";\n    }\n?>',
                 output="apple\nbanana\nmango",
                 notes="foreach is the most common way to loop through arrays in PHP, since you don't need to manage an index manually.",
                 mistakes="Forgetting the $ sign on the loop variable inside a foreach, which causes a parse error.",
                 practice=["Write a foreach loop that prints numbers 1 through 5 from an array.", "Write an if/else that checks whether a number is even or odd."]),
            dict(title="Functions", explanation=
                 "PHP functions are defined with the function keyword and can accept "
                 "parameters with optional default values, then return a value with return.",
                 syntax="function functionName($param1, $param2 = default) {\n    return value;\n}",
                 code='<?php\n    function greet($name, $greeting = "Hello") {\n        return "$greeting, $name!";\n    }\n    echo greet("Vikram");\n?>',
                 output="Hello, Vikram!",
                 notes="Default parameter values let you call a function with fewer arguments than it defines.",
                 mistakes="Placing a parameter with a default value before one without a default, which PHP does not allow.",
                 practice=["Write a function that adds two numbers with a default value of 0 for the second.", "Write a function that returns whether a number is positive, negative, or zero."]),
            dict(title="Arrays & Associative Arrays", explanation=
                 "PHP arrays can be indexed (like a list) or associative (like a "
                 "dictionary, using named keys), making them extremely flexible for "
                 "storing structured data.",
                 syntax='$arr = [value1, value2];\n$assoc = ["key" => value];',
                 code='<?php\n    $student = ["name" => "Neha", "age" => 22];\n    echo $student["name"];\n    $student["age"] = 23;\n?>',
                 output="Neha",
                 notes="Use the => operator to define key-value pairs in an associative array.",
                 mistakes="Mixing up indexed and associative array syntax, e.g. trying to access a keyed value using a numeric index.",
                 practice=["Create an associative array representing a course with name and duration keys.", "Loop through an associative array printing both keys and values."]),
        ],
        quiz_questions=[
            ("How do PHP variables start?", ["With a dollar sign ($)", "With an @ symbol", "With the keyword var", "With a hash (#)"], 0),
            ("Which tag wraps PHP code inside an HTML file?", ["<?php ?>", "<script php>", "<%php %>", "<php></php>"], 0),
            ("Which loop is most commonly used to iterate over an array?", ["foreach", "repeat", "loop", "each"], 0),
            ("What operator defines a key-value pair in an associative array?", ["=>", "->", ":", "="], 0),
        ])


def seed_data_structures():
    seed_simple_course(
        "Data Structures", "data-structures", "🧱",
        "Organize data efficiently — the foundation of every efficient program.",
        "Data structures are ways of organizing and storing data so it can be accessed and "
        "modified efficiently. Understanding them is essential for writing performant "
        "software and doing well in technical interviews.",
        lessons=[
            dict(title="Introduction to Data Structures", explanation=
                 "A data structure is a specific way of organizing data in memory. "
                 "Choosing the right one — like an array versus a linked list — can make "
                 "the difference between a fast program and a slow one.",
                 syntax="# conceptual — applies across languages",
                 code="# An array: fixed-size, indexed collection\nnumbers = [10, 20, 30, 40]\nprint(numbers[2])",
                 output="30",
                 notes="Arrays offer fast, constant-time access by index, but inserting in the middle can be slow because other elements must shift.",
                 mistakes="Assuming every data structure is equally fast for every operation — each one trades speed in one operation for speed in another.",
                 practice=["List three real-world examples where an array would be a natural fit.", "Explain why looking up an array element by index is fast."]),
            dict(title="Stacks", explanation=
                 "A stack follows Last-In, First-Out (LIFO) order — the last item added "
                 "is the first one removed, like a stack of plates. Stacks support push "
                 "(add) and pop (remove) operations.",
                 syntax="stack.push(item)\nstack.pop()",
                 code="stack = []\nstack.append('a')\nstack.append('b')\nstack.append('c')\nprint(stack.pop())\nprint(stack.pop())",
                 output="c\nb",
                 notes="Stacks are used for undo features, browser back buttons, and evaluating expressions.",
                 mistakes="Trying to pop from an empty stack without checking first, which causes an error.",
                 practice=["Use a stack to reverse the characters of a string.", "Write a function that checks if parentheses in an expression are balanced using a stack."]),
            dict(title="Queues", explanation=
                 "A queue follows First-In, First-Out (FIFO) order — the first item "
                 "added is the first one removed, like a line of people waiting. Queues "
                 "support enqueue (add) and dequeue (remove) operations.",
                 syntax="queue.enqueue(item)\nqueue.dequeue()",
                 code="from collections import deque\nqueue = deque()\nqueue.append('first')\nqueue.append('second')\nprint(queue.popleft())",
                 output="first",
                 notes="Queues are used for task scheduling, printer job management, and breadth-first search algorithms.",
                 mistakes="Using a plain list and removing from the front repeatedly, which is much slower than using a proper queue structure.",
                 practice=["Simulate a queue of customers being served one at a time.", "Explain the key difference between a stack and a queue."]),
            dict(title="Linked Lists", explanation=
                 "A linked list is a chain of nodes, where each node stores a value and a "
                 "reference (or 'link') to the next node. Unlike arrays, linked lists don't "
                 "require contiguous memory, making insertion and deletion very efficient.",
                 syntax="class Node:\n    def __init__(self, value):\n        self.value = value\n        self.next = None",
                 code="class Node:\n    def __init__(self, value):\n        self.value = value\n        self.next = None\n\nhead = Node(1)\nhead.next = Node(2)\nhead.next.next = Node(3)\n\ncurrent = head\nwhile current:\n    print(current.value)\n    current = current.next",
                 output="1\n2\n3",
                 notes="Unlike an array, a linked list has no fixed size and grows dynamically as you add nodes.",
                 mistakes="Losing the reference to the next node by overwriting it before saving it elsewhere, which breaks the chain.",
                 practice=["Build a linked list of 4 nodes and print all their values.", "Write a function that counts how many nodes are in a linked list."]),
            dict(title="Trees & Binary Search Trees", explanation=
                 "A tree is a hierarchical structure of nodes, where each node can have "
                 "child nodes. A binary search tree (BST) keeps smaller values to the left "
                 "and larger values to the right, enabling fast searching.",
                 syntax="class TreeNode:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None",
                 code="class TreeNode:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None\n\nroot = TreeNode(10)\nroot.left = TreeNode(5)\nroot.right = TreeNode(15)\nprint(root.left.value, root.value, root.right.value)",
                 output="5 10 15",
                 notes="A balanced binary search tree allows searching in O(log n) time, much faster than scanning a plain list.",
                 mistakes="Building an unbalanced tree (e.g. always inserting increasing values), which degrades performance to that of a linked list.",
                 practice=["Build a small binary search tree with 5 values.", "Write a function that searches for a value in a binary search tree."]),
        ],
        quiz_questions=[
            ("Which order does a stack follow?", ["Last-In, First-Out (LIFO)", "First-In, First-Out (FIFO)", "Random order", "Sorted order"], 0),
            ("Which order does a queue follow?", ["First-In, First-Out (FIFO)", "Last-In, First-Out (LIFO)", "Random order", "Reverse order"], 0),
            ("What does each node in a linked list store?", ["A value and a reference to the next node", "Only a value", "A key and an index", "A fixed memory address"], 0),
            ("In a binary search tree, where are smaller values placed relative to a node?", ["To the left", "To the right", "Above", "It doesn't matter"], 0),
        ])


def seed_algorithms():
    seed_simple_course(
        "Algorithms", "algorithms", "🧮",
        "Step-by-step problem solving — sorting, searching, and beyond.",
        "Algorithms are step-by-step procedures for solving problems efficiently. This "
        "course covers the classic sorting and searching algorithms every programmer "
        "should understand, along with how to reason about efficiency.",
        lessons=[
            dict(title="What Is an Algorithm?", explanation=
                 "An algorithm is a precise, step-by-step sequence of instructions for "
                 "solving a problem or completing a task. Good algorithms are correct, "
                 "efficient, and easy to understand.",
                 syntax="# Pseudocode: describe steps in plain language before coding them",
                 code="# Example: finding the largest number in a list\ndef find_max(numbers):\n    largest = numbers[0]\n    for n in numbers:\n        if n > largest:\n            largest = n\n    return largest\n\nprint(find_max([4, 9, 2, 7]))",
                 output="9",
                 notes="Writing pseudocode before real code helps you plan an algorithm's logic without worrying about syntax.",
                 mistakes="Jumping straight into code without planning the steps, which often leads to bugs and wasted time.",
                 practice=["Write pseudocode for finding the smallest number in a list.", "Implement your pseudocode as a real function."]),
            dict(title="Big O Notation", explanation=
                 "Big O notation describes how an algorithm's time or space requirements "
                 "grow as the input size increases, letting you compare algorithms "
                 "independent of hardware or programming language.",
                 syntax="O(1), O(log n), O(n), O(n log n), O(n^2)",
                 code="# O(n): time grows linearly with input size\ndef print_all(items):\n    for item in items:\n        print(item)\n\n# O(n^2): nested loop over the same list\ndef print_pairs(items):\n    for a in items:\n        for b in items:\n            print(a, b)",
                 output="print_all runs in O(n) time; print_pairs runs in O(n^2) time.",
                 notes="O(1) means constant time regardless of input size — like accessing an array by index.",
                 mistakes="Assuming an algorithm is 'fast enough' without considering how it performs as the input grows much larger.",
                 practice=["Identify the Big O of a function that loops through a list once.", "Identify the Big O of a function with two nested loops over the same list."]),
            dict(title="Bubble Sort & Selection Sort", explanation=
                 "Bubble sort repeatedly swaps adjacent out-of-order elements until the "
                 "list is sorted. Selection sort repeatedly finds the smallest remaining "
                 "element and moves it into place. Both run in O(n^2) time.",
                 syntax="# Repeated passes comparing and swapping/selecting elements",
                 code="def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr\n\nprint(bubble_sort([5, 2, 9, 1, 5]))",
                 output="[1, 2, 5, 5, 9]",
                 notes="Bubble sort is simple to understand but inefficient for large lists — it's mainly used for teaching sorting concepts.",
                 mistakes="Forgetting to reduce the inner loop's range on each pass, which does extra unnecessary comparisons.",
                 practice=["Trace bubble sort by hand on the list [4, 2, 7, 1].", "Implement selection sort and test it on a list of 6 numbers."]),
            dict(title="Merge Sort", explanation=
                 "Merge sort is a divide-and-conquer algorithm: it splits the list in "
                 "half recursively until each part has one element, then merges the "
                 "sorted halves back together. It runs in O(n log n) time, much faster "
                 "than bubble sort for large inputs.",
                 syntax="# Divide, recursively sort, then merge",
                 code="def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i]); i += 1\n        else:\n            result.append(right[j]); j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result\n\nprint(merge_sort([5, 2, 9, 1, 5]))",
                 output="[1, 2, 5, 5, 9]",
                 notes="Merge sort's O(n log n) performance makes it a good default choice for sorting large datasets.",
                 mistakes="Forgetting the base case (a list of length 0 or 1), which causes infinite recursion.",
                 practice=["Trace merge sort by hand on the list [8, 3, 5, 1].", "Explain why merge sort is faster than bubble sort on large lists."]),
            dict(title="Binary Search", explanation=
                 "Binary search finds a target value in a sorted list by repeatedly "
                 "halving the search range, comparing the target to the middle element "
                 "each time. It runs in O(log n) time — extremely fast even on huge lists.",
                 syntax="# Requires a sorted list",
                 code="def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n\nprint(binary_search([1, 3, 5, 7, 9, 11], 9))",
                 output="4",
                 notes="Binary search only works correctly on a sorted list — sort your data first if it isn't already sorted.",
                 mistakes="Forgetting to update low or high correctly, which can cause an infinite loop or an incorrect result.",
                 practice=["Trace binary search by hand searching for 7 in [1,3,5,7,9,11].", "Explain why binary search doesn't work on an unsorted list."]),
        ],
        quiz_questions=[
            ("What does Big O notation describe?", ["How an algorithm's performance scales with input size", "The exact runtime in seconds", "The programming language used", "The number of variables in a program"], 0),
            ("What sorting technique does merge sort use?", ["Divide and conquer", "Random shuffling", "Bubble swapping only", "Selection only"], 0),
            ("What is required for binary search to work correctly?", ["The list must be sorted", "The list must be an array, not a linked list", "The list must have an even number of items", "The list must contain only integers"], 0),
            ("What is the time complexity of bubble sort in the worst case?", ["O(n^2)", "O(n)", "O(log n)", "O(1)"], 0),
        ])


def run():
    with app.app_context():
        db.create_all()
        seed_accounts()
        seed_python()
        seed_c()
        seed_cpp()
        seed_java()
        seed_javascript()
        seed_html()
        seed_css()
        seed_sql()
        seed_php()
        seed_data_structures()
        seed_algorithms()
        db.session.commit()
        print("\nSTUDY HUB seed data loaded successfully.")
        print(f"Courses in database: {Course.query.count()}")
        print(f"Lessons in database: {Lesson.query.count()}")


if __name__ == "__main__":
    run()
