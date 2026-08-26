LESSON_CONTENT = {

    # =========================================================
    # PYTHON
    # =========================================================
    "python": {

        "Introduction": {
            "title": "Python Introduction",
            "intro": "Python is a high-level, beginner-friendly programming language known for its simple and readable syntax.",
            "sections": [
                {
                    "title": "What is Python?",
                    "text": "Python is a general-purpose programming language created by Guido van Rossum. It was first released in 1991 and is widely used in web development, automation, data science, artificial intelligence, and software development."
                },
                {
                    "title": "Why Learn Python?",
                    "points": [
                        "Python has simple and readable syntax.",
                        "It is beginner-friendly.",
                        "It is widely used in Artificial Intelligence and Machine Learning.",
                        "It is useful for automation and scripting.",
                        "Python has many powerful libraries and frameworks."
                    ]
                },
                {
                    "title": "Your First Python Program",
                    "text": "The print() function displays information on the screen.",
                    "code": "print(\"Hello, World!\")"
                },
                {
                    "title": "Important Points",
                    "points": [
                        "Python files use the .py extension.",
                        "Python is case-sensitive.",
                        "Indentation is important.",
                        "Python uses indentation instead of curly braces."
                    ]
                }
            ]
        },

        "Variables & Data Types": {
            "title": "Python Variables & Data Types",
            "intro": "Variables are used to store values in a Python program.",
            "sections": [
                {
                    "title": "What is a Variable?",
                    "text": "A variable is a name that refers to a value stored in memory.",
                    "code": "name = \"Sohel\"\nage = 17\nmarks = 85.5"
                },
                {
                    "title": "Common Data Types",
                    "points": [
                        "int - whole numbers",
                        "float - decimal numbers",
                        "str - text",
                        "bool - True or False",
                        "list - collection of values",
                        "tuple - ordered immutable collection",
                        "dict - key-value pairs"
                    ]
                },
                {
                    "title": "Example",
                    "code": "name = \"Rahul\"\nage = 20\nheight = 5.8\nstudent = True\n\nprint(name)\nprint(age)\nprint(height)\nprint(student)"
                }
            ]
        },

        "Operators": {
            "title": "Python Operators",
            "intro": "Operators are symbols used to perform operations on values and variables.",
            "sections": [
                {
                    "title": "Arithmetic Operators",
                    "points": [
                        "+ Addition",
                        "- Subtraction",
                        "* Multiplication",
                        "/ Division",
                        "% Modulus",
                        "** Exponentiation",
                        "// Floor Division"
                    ],
                    "code": "a = 10\nb = 3\n\nprint(a + b)\nprint(a - b)\nprint(a * b)\nprint(a / b)\nprint(a % b)"
                },
                {
                    "title": "Comparison Operators",
                    "points": [
                        "== Equal to",
                        "!= Not equal to",
                        "> Greater than",
                        "< Less than",
                        ">= Greater than or equal to",
                        "<= Less than or equal to"
                    ]
                },
                {
                    "title": "Logical Operators",
                    "points": [
                        "and - both conditions must be true",
                        "or - at least one condition must be true",
                        "not - reverses a condition"
                    ]
                }
            ]
        },

        "Conditions": {
            "title": "Python Conditions",
            "intro": "Conditional statements allow programs to make decisions.",
            "sections": [
                {
                    "title": "The if Statement",
                    "text": "The if statement executes code when a condition is true.",
                    "code": "age = 18\n\nif age >= 18:\n    print(\"You are an adult.\")"
                },
                {
                    "title": "if-else",
                    "code": "age = 16\n\nif age >= 18:\n    print(\"Adult\")\nelse:\n    print(\"Minor\")"
                },
                {
                    "title": "if-elif-else",
                    "code": "marks = 75\n\nif marks >= 90:\n    print(\"A+\")\nelif marks >= 60:\n    print(\"A\")\nelse:\n    print(\"Needs improvement\")"
                }
            ]
        },

        "Loops": {
            "title": "Python Loops",
            "intro": "Loops are used to execute a block of code repeatedly.",
            "sections": [
                {
                    "title": "for Loop",
                    "text": "A for loop is commonly used to iterate over a sequence.",
                    "code": "for i in range(5):\n    print(i)"
                },
                {
                    "title": "while Loop",
                    "text": "A while loop continues while its condition is true.",
                    "code": "count = 1\n\nwhile count <= 5:\n    print(count)\n    count += 1"
                },
                {
                    "title": "break",
                    "text": "The break statement stops a loop immediately.",
                    "code": "for i in range(10):\n    if i == 5:\n        break\n    print(i)"
                },
                {
                    "title": "continue",
                    "text": "The continue statement skips the current iteration.",
                    "code": "for i in range(5):\n    if i == 2:\n        continue\n    print(i)"
                }
            ]
        },

        "Functions": {
            "title": "Python Functions",
            "intro": "A function is a reusable block of code designed to perform a specific task.",
            "sections": [
                {
                    "title": "Creating a Function",
                    "text": "The def keyword is used to define a function.",
                    "code": "def greet():\n    print(\"Hello!\")\n\ngreet()"
                },
                {
                    "title": "Function Parameters",
                    "code": "def greet(name):\n    print(\"Hello\", name)\n\ngreet(\"Sohel\")"
                },
                {
                    "title": "Return Statement",
                    "text": "The return statement sends a value back from a function.",
                    "code": "def add(a, b):\n    return a + b\n\nresult = add(10, 20)\nprint(result)"
                }
            ]
        },

        "OOP": {
            "title": "Python Object-Oriented Programming",
            "intro": "Object-Oriented Programming is a programming approach based on classes and objects.",
            "sections": [
                {
                    "title": "Class",
                    "text": "A class is a blueprint for creating objects.",
                    "code": "class Student:\n    name = \"Sohel\""
                },
                {
                    "title": "Object",
                    "text": "An object is an instance of a class.",
                    "code": "class Student:\n    def greet(self):\n        print(\"Hello\")\n\nstudent = Student()\nstudent.greet()"
                },
                {
                    "title": "OOP Concepts",
                    "points": [
                        "Class",
                        "Object",
                        "Inheritance",
                        "Encapsulation",
                        "Polymorphism",
                        "Abstraction"
                    ]
                }
            ]
        },

        "File Handling": {
            "title": "Python File Handling",
            "intro": "File handling allows programs to create, read, write, and modify files.",
            "sections": [
                {
                    "title": "Opening a File",
                    "text": "The open() function is used to open a file.",
                    "code": "file = open(\"data.txt\", \"r\")"
                },
                {
                    "title": "Reading a File",
                    "code": "with open(\"data.txt\", \"r\") as file:\n    content = file.read()\n    print(content)"
                },
                {
                    "title": "Writing to a File",
                    "code": "with open(\"data.txt\", \"w\") as file:\n    file.write(\"Hello Python\")"
                }
            ]
        }
    },


    # =========================================================
    # C
    # =========================================================
    "c": {

        "Introduction": {
            "title": "C Programming Introduction",
            "intro": "C is a powerful general-purpose programming language widely used for system programming and software development.",
            "sections": [
                {
                    "title": "What is C?",
                    "text": "C was developed by Dennis Ritchie at Bell Labs. It is known for speed, efficiency, and low-level memory access."
                },
                {
                    "title": "First C Program",
                    "code": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\");\n    return 0;\n}"
                },
                {
                    "title": "Important Features",
                    "points": [
                        "Fast and efficient",
                        "Portable",
                        "Structured programming language",
                        "Supports pointers",
                        "Used for operating systems and embedded systems"
                    ]
                }
            ]
        },

        "Variables & Data Types": {
            "title": "C Variables & Data Types",
            "intro": "Variables store data in memory and every variable in C has a specific data type.",
            "sections": [
                {
                    "title": "Common Data Types",
                    "points": [
                        "int - integer values",
                        "float - decimal values",
                        "double - high precision decimal values",
                        "char - single character"
                    ]
                },
                {
                    "title": "Example",
                    "code": "#include <stdio.h>\n\nint main() {\n    int age = 20;\n    float marks = 85.5;\n    char grade = 'A';\n\n    printf(\"%d\\n\", age);\n    printf(\"%.1f\\n\", marks);\n    printf(\"%c\\n\", grade);\n\n    return 0;\n}"
                }
            ]
        },

        "Operators": {
            "title": "C Operators",
            "intro": "Operators are symbols used to perform calculations and comparisons.",
            "sections": [
                {
                    "title": "Arithmetic Operators",
                    "points": [
                        "+ Addition",
                        "- Subtraction",
                        "* Multiplication",
                        "/ Division",
                        "% Modulus"
                    ],
                    "code": "int a = 10;\nint b = 3;\n\nprintf(\"%d\", a + b);"
                },
                {
                    "title": "Comparison Operators",
                    "points": [
                        "== Equal",
                        "!= Not equal",
                        "> Greater than",
                        "< Less than",
                        ">= Greater than or equal",
                        "<= Less than or equal"
                    ]
                },
                {
                    "title": "Logical Operators",
                    "points": [
                        "&& Logical AND",
                        "|| Logical OR",
                        "! Logical NOT"
                    ]
                }
            ]
        },

        "Conditions": {
            "title": "C Conditional Statements",
            "intro": "Conditional statements allow a C program to make decisions.",
            "sections": [
                {
                    "title": "if Statement",
                    "code": "int age = 20;\n\nif (age >= 18) {\n    printf(\"Adult\");\n}"
                },
                {
                    "title": "if-else",
                    "code": "int age = 16;\n\nif (age >= 18) {\n    printf(\"Adult\");\n} else {\n    printf(\"Minor\");\n}"
                },
                {
                    "title": "switch Statement",
                    "code": "int day = 1;\n\nswitch(day) {\n    case 1:\n        printf(\"Monday\");\n        break;\n    default:\n        printf(\"Invalid day\");\n}"
                }
            ]
        },

        "Loops": {
            "title": "C Loops",
            "intro": "Loops execute a block of code repeatedly.",
            "sections": [
                {
                    "title": "for Loop",
                    "code": "for (int i = 1; i <= 5; i++) {\n    printf(\"%d\\n\", i);\n}"
                },
                {
                    "title": "while Loop",
                    "code": "int i = 1;\n\nwhile (i <= 5) {\n    printf(\"%d\\n\", i);\n    i++;\n}"
                },
                {
                    "title": "do-while Loop",
                    "code": "int i = 1;\n\ndo {\n    printf(\"%d\\n\", i);\n    i++;\n} while (i <= 5);"
                }
            ]
        },

        "Functions": {
            "title": "C Functions",
            "intro": "Functions are reusable blocks of code that perform specific tasks.",
            "sections": [
                {
                    "title": "Creating a Function",
                    "code": "void greet() {\n    printf(\"Hello\");\n}"
                },
                {
                    "title": "Function with Parameters",
                    "code": "int add(int a, int b) {\n    return a + b;\n}"
                },
                {
                    "title": "Calling a Function",
                    "code": "int result = add(10, 20);\nprintf(\"%d\", result);"
                }
            ]
        },

        "Arrays": {
            "title": "C Arrays",
            "intro": "An array stores multiple values of the same data type.",
            "sections": [
                {
                    "title": "Creating an Array",
                    "code": "int numbers[5] = {10, 20, 30, 40, 50};"
                },
                {
                    "title": "Accessing Elements",
                    "text": "Array indexing starts from zero.",
                    "code": "printf(\"%d\", numbers[0]);"
                },
                {
                    "title": "Loop Through an Array",
                    "code": "for (int i = 0; i < 5; i++) {\n    printf(\"%d\\n\", numbers[i]);\n}"
                }
            ]
        },

        "Pointers": {
            "title": "C Pointers",
            "intro": "A pointer is a variable that stores the memory address of another variable.",
            "sections": [
                {
                    "title": "Pointer Example",
                    "code": "int age = 20;\nint *ptr = &age;\n\nprintf(\"%d\", *ptr);"
                },
                {
                    "title": "Address Operator",
                    "text": "The & operator returns the memory address of a variable."
                },
                {
                    "title": "Dereference Operator",
                    "text": "The * operator is used to access the value stored at an address."
                }
            ]
        }
    },


    # =========================================================
    # C++
    # =========================================================
    "cpp": {

        "Introduction": {
            "title": "C++ Introduction",
            "intro": "C++ is a powerful programming language that supports both procedural and object-oriented programming.",
            "sections": [
                {
                    "title": "What is C++?",
                    "text": "C++ was developed by Bjarne Stroustrup. It is widely used for games, system software, applications, and competitive programming."
                },
                {
                    "title": "First C++ Program",
                    "code": "#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"Hello, World!\";\n    return 0;\n}"
                },
                {
                    "title": "Features",
                    "points": [
                        "Object-oriented programming",
                        "Fast execution",
                        "Classes and objects",
                        "Templates",
                        "STL library"
                    ]
                }
            ]
        },

        "Variables & Data Types": {
            "title": "C++ Variables & Data Types",
            "intro": "Variables are named memory locations used to store values.",
            "sections": [
                {
                    "title": "Common Data Types",
                    "points": [
                        "int",
                        "float",
                        "double",
                        "char",
                        "bool",
                        "string"
                    ]
                },
                {
                    "title": "Example",
                    "code": "int age = 20;\ndouble marks = 85.5;\nchar grade = 'A';\nbool passed = true;\nstring name = \"Sohel\";"
                }
            ]
        },

        "Operators": {
            "title": "C++ Operators",
            "intro": "C++ provides operators for arithmetic, comparison, assignment, and logical operations.",
            "sections": [
                {
                    "title": "Arithmetic",
                    "code": "int a = 10;\nint b = 3;\n\ncout << a + b << endl;\ncout << a - b << endl;\ncout << a * b << endl;"
                },
                {
                    "title": "Comparison",
                    "points": [
                        "==",
                        "!=",
                        ">",
                        "<",
                        ">=",
                        "<="
                    ]
                }
            ]
        },

        "Conditions": {
            "title": "C++ Conditions",
            "intro": "Conditional statements control which part of a program is executed.",
            "sections": [
                {
                    "title": "if-else",
                    "code": "int age = 20;\n\nif (age >= 18) {\n    cout << \"Adult\";\n} else {\n    cout << \"Minor\";\n}"
                },
                {
                    "title": "switch",
                    "code": "int choice = 1;\n\nswitch(choice) {\n    case 1:\n        cout << \"Start\";\n        break;\n    default:\n        cout << \"Invalid\";\n}"
                }
            ]
        },

        "Loops": {
            "title": "C++ Loops",
            "intro": "Loops repeat a block of code.",
            "sections": [
                {
                    "title": "for Loop",
                    "code": "for (int i = 1; i <= 5; i++) {\n    cout << i << endl;\n}"
                },
                {
                    "title": "while Loop",
                    "code": "int i = 1;\n\nwhile (i <= 5) {\n    cout << i << endl;\n    i++;\n}"
                },
                {
                    "title": "range-based for",
                    "code": "int numbers[] = {10, 20, 30};\n\nfor (int n : numbers) {\n    cout << n << endl;\n}"
                }
            ]
        },

        "Functions": {
            "title": "C++ Functions",
            "intro": "Functions allow programmers to divide programs into reusable blocks.",
            "sections": [
                {
                    "title": "Function",
                    "code": "int add(int a, int b) {\n    return a + b;\n}"
                },
                {
                    "title": "Calling a Function",
                    "code": "cout << add(10, 20);"
                },
                {
                    "title": "Default Parameters",
                    "code": "void greet(string name = \"Student\") {\n    cout << \"Hello \" << name;\n}"
                }
            ]
        },

        "Classes & Objects": {
            "title": "C++ Classes & Objects",
            "intro": "Classes and objects are fundamental concepts of object-oriented programming.",
            "sections": [
                {
                    "title": "Creating a Class",
                    "code": "class Student {\npublic:\n    string name;\n\n    void greet() {\n        cout << \"Hello\";\n    }\n};"
                },
                {
                    "title": "Creating an Object",
                    "code": "Student s;\ns.name = \"Sohel\";\ns.greet();"
                }
            ]
        },

        "Inheritance": {
            "title": "C++ Inheritance",
            "intro": "Inheritance allows one class to acquire properties and methods of another class.",
            "sections": [
                {
                    "title": "Basic Inheritance",
                    "code": "class Animal {\npublic:\n    void eat() {\n        cout << \"Eating\";\n    }\n};\n\nclass Dog : public Animal {\n};"
                },
                {
                    "title": "Why Use Inheritance?",
                    "points": [
                        "Code reuse",
                        "Better organization",
                        "Supports hierarchical relationships",
                        "Reduces duplicate code"
                    ]
                }
            ]
        }
    },


    # =========================================================
    # JAVA
    # =========================================================
    "java": {

        "Introduction": {
            "title": "Java Introduction",
            "intro": "Java is a popular object-oriented programming language designed to be portable and reliable.",
            "sections": [
                {
                    "title": "What is Java?",
                    "text": "Java was developed by James Gosling at Sun Microsystems. Java programs run on the Java Virtual Machine."
                },
                {
                    "title": "First Java Program",
                    "code": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}"
                },
                {
                    "title": "Features",
                    "points": [
                        "Object-oriented",
                        "Platform independent",
                        "Secure",
                        "Robust",
                        "Multithreaded"
                    ]
                }
            ]
        },

        "Variables & Data Types": {
            "title": "Java Variables & Data Types",
            "intro": "Java requires variables to have a declared data type.",
            "sections": [
                {
                    "title": "Primitive Types",
                    "points": [
                        "int",
                        "float",
                        "double",
                        "char",
                        "boolean",
                        "long",
                        "short",
                        "byte"
                    ]
                },
                {
                    "title": "Example",
                    "code": "int age = 20;\ndouble marks = 85.5;\nchar grade = 'A';\nboolean passed = true;\nString name = \"Sohel\";"
                }
            ]
        },

        "Operators": {
            "title": "Java Operators",
            "intro": "Operators are used to perform calculations and comparisons.",
            "sections": [
                {
                    "title": "Arithmetic Operators",
                    "code": "int a = 10;\nint b = 3;\n\nSystem.out.println(a + b);\nSystem.out.println(a - b);\nSystem.out.println(a * b);"
                },
                {
                    "title": "Logical Operators",
                    "points": [
                        "&& AND",
                        "|| OR",
                        "! NOT"
                    ]
                }
            ]
        },

        "Conditions": {
            "title": "Java Conditions",
            "intro": "Conditional statements allow Java programs to make decisions.",
            "sections": [
                {
                    "title": "if-else",
                    "code": "int age = 20;\n\nif (age >= 18) {\n    System.out.println(\"Adult\");\n} else {\n    System.out.println(\"Minor\");\n}"
                },
                {
                    "title": "switch",
                    "code": "int day = 1;\n\nswitch(day) {\n    case 1:\n        System.out.println(\"Monday\");\n        break;\n    default:\n        System.out.println(\"Unknown\");\n}"
                }
            ]
        },

        "Loops": {
            "title": "Java Loops",
            "intro": "Loops execute a block of code repeatedly.",
            "sections": [
                {
                    "title": "for Loop",
                    "code": "for (int i = 1; i <= 5; i++) {\n    System.out.println(i);\n}"
                },
                {
                    "title": "while Loop",
                    "code": "int i = 1;\n\nwhile (i <= 5) {\n    System.out.println(i);\n    i++;\n}"
                },
                {
                    "title": "for-each Loop",
                    "code": "int[] numbers = {10, 20, 30};\n\nfor (int n : numbers) {\n    System.out.println(n);\n}"
                }
            ]
        },

        "Methods": {
            "title": "Java Methods",
            "intro": "Methods are reusable blocks of code inside a class.",
            "sections": [
                {
                    "title": "Creating a Method",
                    "code": "static void greet() {\n    System.out.println(\"Hello\");\n}"
                },
                {
                    "title": "Method Parameters",
                    "code": "static void greet(String name) {\n    System.out.println(\"Hello \" + name);\n}"
                },
                {
                    "title": "Return Value",
                    "code": "static int add(int a, int b) {\n    return a + b;\n}"
                }
            ]
        },

        "Classes & Objects": {
            "title": "Java Classes & Objects",
            "intro": "A class is a blueprint and an object is an instance of that class.",
            "sections": [
                {
                    "title": "Creating a Class",
                    "code": "class Student {\n    String name;\n\n    void greet() {\n        System.out.println(\"Hello\");\n    }\n}"
                },
                {
                    "title": "Creating an Object",
                    "code": "Student student = new Student();\nstudent.name = \"Sohel\";\nstudent.greet();"
                }
            ]
        },

        "Inheritance": {
            "title": "Java Inheritance",
            "intro": "Inheritance allows a class to inherit properties and methods from another class.",
            "sections": [
                {
                    "title": "Example",
                    "code": "class Animal {\n    void eat() {\n        System.out.println(\"Eating\");\n    }\n}\n\nclass Dog extends Animal {\n}"
                },
                {
                    "title": "Benefits",
                    "points": [
                        "Code reuse",
                        "Less duplicate code",
                        "Better program structure",
                        "Supports polymorphism"
                    ]
                }
            ]
        }
    },


    # =========================================================
    # JAVASCRIPT
    # =========================================================
    "javascript": {

        "Introduction": {
            "title": "JavaScript Introduction",
            "intro": "JavaScript is a programming language used to make websites interactive and dynamic.",
            "sections": [
                {
                    "title": "What is JavaScript?",
                    "text": "JavaScript runs mainly inside web browsers and can interact with HTML and CSS."
                },
                {
                    "title": "First Program",
                    "code": "console.log(\"Hello, World!\");"
                },
                {
                    "title": "Uses of JavaScript",
                    "points": [
                        "Interactive websites",
                        "Web applications",
                        "Server-side development",
                        "Mobile applications",
                        "Browser-based games"
                    ]
                }
            ]
        },

        "Variables": {
            "title": "JavaScript Variables",
            "intro": "Variables are used to store values.",
            "sections": [
                {
                    "title": "let",
                    "code": "let name = \"Sohel\";"
                },
                {
                    "title": "const",
                    "code": "const pi = 3.14159;"
                },
                {
                    "title": "var",
                    "code": "var age = 20;"
                }
            ]
        },

        "Data Types": {
            "title": "JavaScript Data Types",
            "intro": "JavaScript supports several primitive and non-primitive data types.",
            "sections": [
                {
                    "title": "Common Types",
                    "points": [
                        "String",
                        "Number",
                        "Boolean",
                        "Undefined",
                        "Null",
                        "Object",
                        "Array"
                    ]
                },
                {
                    "title": "Example",
                    "code": "let name = \"Sohel\";\nlet age = 20;\nlet passed = true;\nlet value = null;"
                }
            ]
        },

        "Operators": {
            "title": "JavaScript Operators",
            "intro": "Operators are used to perform calculations and comparisons.",
            "sections": [
                {
                    "title": "Arithmetic",
                    "code": "let a = 10;\nlet b = 3;\n\nconsole.log(a + b);\nconsole.log(a - b);\nconsole.log(a * b);\nconsole.log(a / b);"
                },
                {
                    "title": "Comparison",
                    "points": [
                        "==",
                        "===",
                        "!=",
                        "!==",
                        ">",
                        "<",
                        ">=",
                        "<="
                    ]
                }
            ]
        },

        "Conditions": {
            "title": "JavaScript Conditions",
            "intro": "Conditional statements allow JavaScript to make decisions.",
            "sections": [
                {
                    "title": "if-else",
                    "code": "let age = 20;\n\nif (age >= 18) {\n    console.log(\"Adult\");\n} else {\n    console.log(\"Minor\");\n}"
                },
                {
                    "title": "else-if",
                    "code": "let marks = 80;\n\nif (marks >= 90) {\n    console.log(\"A+\");\n} else if (marks >= 60) {\n    console.log(\"A\");\n} else {\n    console.log(\"Needs improvement\");\n}"
                }
            ]
        },

        "Loops": {
            "title": "JavaScript Loops",
            "intro": "Loops repeat code while a condition is satisfied.",
            "sections": [
                {
                    "title": "for Loop",
                    "code": "for (let i = 1; i <= 5; i++) {\n    console.log(i);\n}"
                },
                {
                    "title": "while Loop",
                    "code": "let i = 1;\n\nwhile (i <= 5) {\n    console.log(i);\n    i++;\n}"
                },
                {
                    "title": "for-of",
                    "code": "let numbers = [10, 20, 30];\n\nfor (let n of numbers) {\n    console.log(n);\n}"
                }
            ]
        },

        "Functions": {
            "title": "JavaScript Functions",
            "intro": "Functions are reusable blocks of JavaScript code.",
            "sections": [
                {
                    "title": "Normal Function",
                    "code": "function greet() {\n    console.log(\"Hello\");\n}\n\ngreet();"
                },
                {
                    "title": "Parameters",
                    "code": "function greet(name) {\n    console.log(\"Hello \" + name);\n}\n\ngreet(\"Sohel\");"
                },
                {
                    "title": "Arrow Function",
                    "code": "const add = (a, b) => a + b;\n\nconsole.log(add(10, 20));"
                }
            ]
        },

        "DOM": {
            "title": "JavaScript DOM",
            "intro": "The Document Object Model allows JavaScript to access and modify HTML elements.",
            "sections": [
                {
                    "title": "Selecting an Element",
                    "code": "const heading = document.getElementById(\"title\");"
                },
                {
                    "title": "Changing Text",
                    "code": "document.getElementById(\"title\").textContent = \"Hello JavaScript\";"
                },
                {
                    "title": "Changing Style",
                    "code": "document.getElementById(\"title\").style.color = \"blue\";"
                }
            ]
        }
    },


    # =========================================================
    # SQL
    # =========================================================
    "sql": {

        "Introduction": {
            "title": "SQL Introduction",
            "intro": "SQL stands for Structured Query Language and is used to communicate with relational databases.",
            "sections": [
                {
                    "title": "What is SQL?",
                    "text": "SQL allows developers to create, read, update, and delete data in databases."
                },
                {
                    "title": "Common SQL Databases",
                    "points": [
                        "MySQL",
                        "PostgreSQL",
                        "SQLite",
                        "Microsoft SQL Server",
                        "Oracle Database"
                    ]
                },
                {
                    "title": "Basic Query",
                    "code": "SELECT * FROM students;"
                }
            ]
        },

        "SELECT": {
            "title": "SQL SELECT",
            "intro": "The SELECT statement is used to retrieve data from a database table.",
            "sections": [
                {
                    "title": "Select All Columns",
                    "code": "SELECT * FROM students;"
                },
                {
                    "title": "Select Specific Columns",
                    "code": "SELECT name, age FROM students;"
                },
                {
                    "title": "Column Alias",
                    "code": "SELECT name AS student_name FROM students;"
                }
            ]
        },

        "WHERE": {
            "title": "SQL WHERE",
            "intro": "The WHERE clause filters records based on a condition.",
            "sections": [
                {
                    "title": "Basic WHERE",
                    "code": "SELECT * FROM students\nWHERE age >= 18;"
                },
                {
                    "title": "Multiple Conditions",
                    "code": "SELECT * FROM students\nWHERE age >= 18 AND marks >= 60;"
                }
            ]
        },

        "INSERT": {
            "title": "SQL INSERT",
            "intro": "The INSERT statement adds new records to a table.",
            "sections": [
                {
                    "title": "Insert a Record",
                    "code": "INSERT INTO students (name, age)\nVALUES ('Sohel', 20);"
                },
                {
                    "title": "Insert Multiple Records",
                    "code": "INSERT INTO students (name, age)\nVALUES\n('Sohel', 20),\n('Rahul', 21);"
                }
            ]
        },

        "UPDATE": {
            "title": "SQL UPDATE",
            "intro": "The UPDATE statement modifies existing records.",
            "sections": [
                {
                    "title": "Update a Record",
                    "code": "UPDATE students\nSET age = 21\nWHERE name = 'Sohel';"
                },
                {
                    "title": "Important Warning",
                    "text": "Always use a WHERE clause when appropriate. Without it, all rows may be updated."
                }
            ]
        },

        "DELETE": {
            "title": "SQL DELETE",
            "intro": "The DELETE statement removes records from a database table.",
            "sections": [
                {
                    "title": "Delete a Record",
                    "code": "DELETE FROM students\nWHERE name = 'Sohel';"
                },
                {
                    "title": "Important Warning",
                    "text": "Using DELETE without a WHERE clause can remove every record from the table."
                }
            ]
        },

        "JOIN": {
            "title": "SQL JOIN",
            "intro": "JOIN operations combine data from multiple related tables.",
            "sections": [
                {
                    "title": "INNER JOIN",
                    "code": "SELECT students.name, courses.title\nFROM students\nINNER JOIN courses\nON students.course_id = courses.id;"
                },
                {
                    "title": "Common JOIN Types",
                    "points": [
                        "INNER JOIN",
                        "LEFT JOIN",
                        "RIGHT JOIN",
                        "FULL OUTER JOIN"
                    ]
                }
            ]
        },

        "GROUP BY": {
            "title": "SQL GROUP BY",
            "intro": "GROUP BY groups rows that have the same values and is commonly used with aggregate functions.",
            "sections": [
                {
                    "title": "Example",
                    "code": "SELECT course, COUNT(*)\nFROM students\nGROUP BY course;"
                },
                {
                    "title": "Aggregate Functions",
                    "points": [
                        "COUNT()",
                        "SUM()",
                        "AVG()",
                        "MIN()",
                        "MAX()"
                    ]
                }
            ]
        }
    },


    # =========================================================
    # HTML & CSS
    # =========================================================
    "html-css": {

        "HTML Introduction": {
            "title": "HTML Introduction",
            "intro": "HTML stands for HyperText Markup Language and is used to create the structure of web pages.",
            "sections": [
                {
                    "title": "Basic HTML Document",
                    "code": "<!DOCTYPE html>\n<html>\n<head>\n    <title>My Website</title>\n</head>\n<body>\n    <h1>Hello World</h1>\n</body>\n</html>"
                },
                {
                    "title": "Common HTML Elements",
                    "points": [
                        "h1 to h6 - headings",
                        "p - paragraph",
                        "a - link",
                        "img - image",
                        "button - button",
                        "div - container"
                    ]
                }
            ]
        },

        "HTML Text & Links": {
            "title": "HTML Text & Links",
            "intro": "HTML provides elements for displaying text and creating hyperlinks.",
            "sections": [
                {
                    "title": "Headings and Paragraphs",
                    "code": "<h1>Main Heading</h1>\n<h2>Sub Heading</h2>\n<p>This is a paragraph.</p>"
                },
                {
                    "title": "Links",
                    "code": "<a href=\"https://example.com\">Visit Website</a>"
                }
            ]
        },

        "HTML Lists": {
            "title": "HTML Lists",
            "intro": "Lists are used to display related items.",
            "sections": [
                {
                    "title": "Unordered List",
                    "code": "<ul>\n    <li>Python</li>\n    <li>C++</li>\n    <li>Java</li>\n</ul>"
                },
                {
                    "title": "Ordered List",
                    "code": "<ol>\n    <li>Login</li>\n    <li>Learn</li>\n    <li>Practice</li>\n</ol>"
                }
            ]
        },

        "HTML Forms": {
            "title": "HTML Forms",
            "intro": "HTML forms collect information from users.",
            "sections": [
                {
                    "title": "Basic Form",
                    "code": "<form>\n    <label>Name:</label>\n    <input type=\"text\">\n    <button type=\"submit\">Submit</button>\n</form>"
                },
                {
                    "title": "Common Input Types",
                    "points": [
                        "text",
                        "email",
                        "password",
                        "number",
                        "date",
                        "checkbox",
                        "radio"
                    ]
                }
            ]
        },

        "CSS Introduction": {
            "title": "CSS Introduction",
            "intro": "CSS stands for Cascading Style Sheets and is used to style HTML pages.",
            "sections": [
                {
                    "title": "Basic CSS",
                    "code": "body {\n    background: #08111f;\n    color: white;\n}\n\nh1 {\n    color: cyan;\n}"
                },
                {
                    "title": "Why CSS?",
                    "points": [
                        "Colors",
                        "Spacing",
                        "Fonts",
                        "Layouts",
                        "Animations",
                        "Responsive design"
                    ]
                }
            ]
        },

        "CSS Selectors": {
            "title": "CSS Selectors",
            "intro": "CSS selectors identify the HTML elements that should be styled.",
            "sections": [
                {
                    "title": "Element Selector",
                    "code": "p {\n    color: blue;\n}"
                },
                {
                    "title": "Class Selector",
                    "code": ".card {\n    padding: 20px;\n}"
                },
                {
                    "title": "ID Selector",
                    "code": "#title {\n    color: red;\n}"
                }
            ]
        },

        "CSS Box Model": {
            "title": "CSS Box Model",
            "intro": "The CSS box model describes how every HTML element is represented as a rectangular box.",
            "sections": [
                {
                    "title": "Box Model Parts",
                    "points": [
                        "Content",
                        "Padding",
                        "Border",
                        "Margin"
                    ]
                },
                {
                    "title": "Example",
                    "code": ".card {\n    width: 300px;\n    padding: 20px;\n    border: 1px solid white;\n    margin: 20px;\n}"
                }
            ]
        },

        "Responsive Design": {
            "title": "CSS Responsive Design",
            "intro": "Responsive design allows websites to look good on desktops, tablets, and mobile devices.",
            "sections": [
                {
                    "title": "Media Query",
                    "code": "@media (max-width: 600px) {\n    .card {\n        width: 100%;\n    }\n}"
                },
                {
                    "title": "Important Techniques",
                    "points": [
                        "Flexible layouts",
                        "CSS Grid",
                        "Flexbox",
                        "Media queries",
                        "Responsive images"
                    ]
                }
            ]
        }
    }
}