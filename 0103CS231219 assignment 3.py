"""
assignment 03

Name: Lakshya patel
Enrollment: 0103CS231219
Batch: 6
Batch Time: 12:10pm
"""

import json
import os
import random
from datetime import datetime

USERS_FILE = "students.json"
QUESTIONS_FILE = "questions.json"
SCORES_FILE = "scores.json"

def load(file):
    if not os.path.exists(file):
        return {}
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def ensure_defaults():
    users = load(USERS_FILE)
    if "admin" not in users:
        users["admin"] = {
            "password": "admin123",
            "name": "Administrator",
            "email": "admin@lnct.edu",
            "phone": "",
            "branch": "Admin",
            "year": "",
            "enrollment": "0000",
            "role": "admin"
        }
        save(USERS_FILE, users)
    questions = load(QUESTIONS_FILE)
    if not questions:
        questions = {
            "DSA": [
                {"q": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "ans": "O(log n)"},
                {"q": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Tree", "Graph"], "ans": "Stack"},
                {"q": "Which traversal uses queue?", "options": ["DFS", "BFS", "Inorder", "Postorder"], "ans": "BFS"},
                {"q": "Which data structure is used for recursion?", "options": ["Stack", "Queue", "Array", "Linked List"], "ans": "Stack"},
                {"q": "Which sorting algorithm is generally fastest on average?", "options": ["Bubble", "Insertion", "Quick", "Selection"], "ans": "Quick"},
                {"q": "What is the best case of quicksort on random pivot?", "options": ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"], "ans": "O(n log n)"},
                {"q": "Which is a self-balancing binary search tree?", "options": ["BST", "AVL", "LinkedList", "Heap"], "ans": "AVL"},
                {"q": "What does 'DFS' stand for?", "options": ["Depth First Search", "Data Flow System", "Distributed File System", "Direct File Search"], "ans": "Depth First Search"}
            ],
            "DBMS": [
                {"q": "Which key uniquely identifies a record?", "options": ["Primary Key", "Foreign Key", "Candidate Key", "Super Key"], "ans": "Primary Key"},
                {"q": "Which language is used to query database?", "options": ["HTML", "SQL", "C++", "Python"], "ans": "SQL"},
                {"q": "What is normalization?", "options": ["Data duplication", "Organizing data", "Deleting data", "Encrypting data"], "ans": "Organizing data"},
                {"q": "Which command is used to remove table?", "options": ["DELETE", "DROP", "TRUNCATE", "REMOVE"], "ans": "DROP"},
                {"q": "Which of these is a NoSQL DB?", "options": ["MySQL", "MongoDB", "Oracle", "PostgreSQL"], "ans": "MongoDB"},
                {"q": "What does ACID stand for in databases?", "options": ["Atomicity Consistency Isolation Durability", "Access Control Isolated Data", "Automatic Consistent Indexing Database", "None"], "ans": "Atomicity Consistency Isolation Durability"}
            ],
            "PYTHON": [
                {"q": "Which keyword defines a function?", "options": ["fun", "def", "function", "define"], "ans": "def"},
                {"q": "Which data type is immutable?", "options": ["List", "Set", "Dictionary", "Tuple"], "ans": "Tuple"},
                {"q": "Which operator is used for floor division?", "options": ["/", "//", "%", "**"], "ans": "//"},
                {"q": "Which function returns length of string?", "options": ["count()", "size()", "len()", "length()"], "ans": "len()"},
                {"q": "What is output of 2**3?", "options": ["5", "6", "8", "9"], "ans": "8"},
                {"q": "Which statement is used to handle exceptions?", "options": ["try/except", "if/else", "for/while", "switch/case"], "ans": "try/except"}
            ]
        }
        save(QUESTIONS_FILE, questions)
    scores = load(SCORES_FILE)
    if not isinstance(scores, dict):
        save(SCORES_FILE, {})

ensure_defaults()

logged_user = None
logged_role = None

def register():
    users = load(USERS_FILE)
    username = input("Choose username: ").strip()
    if not username:
        print("Username cannot be empty")
        return
    if username in users:
        print("Username already exists")
        return
    password = input("Choose password: ").strip()
    name = input("Full name: ").strip()
    email = input("Email: ").strip()
    phone = input("Contact number: ").strip()
    branch = input("Branch: ").strip()
    year = input("Year: ").strip()
    enrollment = input("Enrollment number: ").strip()
    users[username] = {
        "password": password,
        "name": name,
        "email": email,
        "phone": phone,
        "branch": branch,
        "year": year,
        "enrollment": enrollment,
        "role": "user"
    }
    save(USERS_FILE, users)
    print("Registration successful")

def login():
    global logged_user, logged_role
    users = load(USERS_FILE)
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username in users and users[username]["password"] == password:
        logged_user = username
        logged_role = users[username].get("role", "user")
        print(f"Logged in as {users[username].get('name','')}. Role: {logged_role}")
    else:
        print("Invalid credentials")

def show_profile():
    if not logged_user:
        print("Please login first")
        return
    users = load(USERS_FILE)
    p = users.get(logged_user)
    for k, v in p.items():
        if k != "password":
            print(f"{k.capitalize()}: {v}")

def update_profile():
    if not logged_user:
        print("Please login first")
        return
    users = load(USERS_FILE)
    p = users.get(logged_user)
    for field in ["name", "email", "phone", "branch", "year"]:
        current = p.get(field, "")
        new = input(f"{field.capitalize()} (current: {current}) new (leave blank to keep): ").strip()
        if new:
            p[field] = new
    users[logged_user] = p
    save(USERS_FILE, users)
    print("Profile updated")

def logout():
    global logged_user, logged_role
    if not logged_user:
        print("Not logged in")
        return
    print(f"{logged_user} logged out")
    logged_user = None
    logged_role = None

def attempt_quiz():
    if not logged_user:
        print("Please login to attempt quiz")
        return
    questions = load(QUESTIONS_FILE)
    cats = list(questions.keys())
    for i, c in enumerate(cats, start=1):
        print(f"{i}. {c}")
    choice = input("Choose category: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(cats):
        print("Invalid choice")
        return
    category = cats[int(choice)-1]
    qlist = questions.get(category, [])
    if not qlist:
        print("No questions in this category")
        return
    count = min(10, max(5, len(qlist)))
    if count > len(qlist):
        count = len(qlist)
    qsample = random.sample(qlist, count)
    score = 0
    total = len(qsample)
    for idx, q in enumerate(qsample, start=1):
        print(f"\nQ{idx}. {q['q']}")
        opts = q['options']
        random_opts = opts[:]
        random.shuffle(random_opts)
        for j, opt in enumerate(random_opts, start=1):
            print(f"  {j}. {opt}")
        ans = input("Enter option number: ").strip()
        if ans.isdigit() and 1 <= int(ans) <= len(random_opts):
            selected = random_opts[int(ans)-1]
            if selected == q['ans']:
                print("Correct")
                score += 1
            else:
                print(f"Wrong. Correct: {q['ans']}")
        else:
            print("Invalid input. Counted as wrong.")
    print(f"\nYour score: {score}/{total}")
    record = {
        "enrollment": load(USERS_FILE)[logged_user].get("enrollment", ""),
        "category": category,
        "score": f"{score}/{total}",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    scores = load(SCORES_FILE)
    if logged_user not in scores:
        scores[logged_user] = []
    scores[logged_user].append(record)
    save(SCORES_FILE, scores)

def show_my_scores():
    if not logged_user:
        print("Please login first")
        return
    scores = load(SCORES_FILE)
    user_scores = scores.get(logged_user, [])
    if not user_scores:
        print("No attempts yet")
        return
    for r in user_scores:
        print(f"{r['datetime']} | {r['category']} | {r['score']} | {r['enrollment']}")

def admin_view_all_scores():
    if logged_role != "admin":
        print("Admin access required")
        return
    scores = load(SCORES_FILE)
    for user, records in scores.items():
        print(f"\nUser: {user}")
        for r in records:
            print(f"  {r['datetime']} | {r['category']} | {r['score']} | {r['enrollment']}")

def admin_add_question():
    if logged_role != "admin":
        print("Admin access required")
        return
    questions = load(QUESTIONS_FILE)
    cats = list(questions.keys())
    for i, c in enumerate(cats, start=1):
        print(f"{i}. {c}")
    choice = input("Select category to add question or type new category name: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(cats):
        category = cats[int(choice)-1]
    else:
        category = choice
        if category not in questions:
            questions[category] = []
    qtext = input("Enter question text: ").strip()
    opts = []
    for i in range(1,5):
        o = input(f"Option {i}: ").strip()
        opts.append(o)
    ans = input("Enter the correct option text exactly as above: ").strip()
    questions[category].append({"q": qtext, "options": opts, "ans": ans})
    save(QUESTIONS_FILE, questions)
    print("Question added")

def menu():
    while True:
        print("\n1. Register\n2. Login\n3. Show Profile\n4. Update Profile\n5. Attempt Quiz\n6. Show My Scores\n7. Logout\n8. Exit")
        if logged_role == "admin":
            print("9. Admin: View All Scores\n10. Admin: Add Question")
        choice = input("Choose option: ").strip()
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            show_profile()
        elif choice == '4':
            update_profile()
        elif choice == '5':
            attempt_quiz()
        elif choice == '6':
            show_my_scores()
        elif choice == '7':
            logout()
        elif choice == '8':
            print("Goodbye")
            break
        elif choice == '9' and logged_role == "admin":
            admin_view_all_scores()
        elif choice == '10' and logged_role == "admin":
            admin_add_question()
        else:
            print("Invalid option")

if __name__ == "__main__":
    menu()import json
import os
import random
from datetime import datetime

USERS_FILE = "students.json"
QUESTIONS_FILE = "questions.json"
SCORES_FILE = "scores.json"

def load(file):
    if not os.path.exists(file):
        return {}
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def ensure_defaults():
    users = load(USERS_FILE)
    if "admin" not in users:
        users["admin"] = {
            "password": "admin123",
            "name": "Administrator",
            "email": "admin@lnct.edu",
            "phone": "",
            "branch": "Admin",
            "year": "",
            "enrollment": "0000",
            "role": "admin"
        }
        save(USERS_FILE, users)
    questions = load(QUESTIONS_FILE)
    if not questions:
        questions = {
            "DSA": [
                {"q": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "ans": "O(log n)"},
                {"q": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Tree", "Graph"], "ans": "Stack"},
                {"q": "Which traversal uses queue?", "options": ["DFS", "BFS", "Inorder", "Postorder"], "ans": "BFS"},
                {"q": "Which data structure is used for recursion?", "options": ["Stack", "Queue", "Array", "Linked List"], "ans": "Stack"},
                {"q": "Which sorting algorithm is generally fastest on average?", "options": ["Bubble", "Insertion", "Quick", "Selection"], "ans": "Quick"},
                {"q": "What is the best case of quicksort on random pivot?", "options": ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"], "ans": "O(n log n)"},
                {"q": "Which is a self-balancing binary search tree?", "options": ["BST", "AVL", "LinkedList", "Heap"], "ans": "AVL"},
                {"q": "What does 'DFS' stand for?", "options": ["Depth First Search", "Data Flow System", "Distributed File System", "Direct File Search"], "ans": "Depth First Search"}
            ],
            "DBMS": [
                {"q": "Which key uniquely identifies a record?", "options": ["Primary Key", "Foreign Key", "Candidate Key", "Super Key"], "ans": "Primary Key"},
                {"q": "Which language is used to query database?", "options": ["HTML", "SQL", "C++", "Python"], "ans": "SQL"},
                {"q": "What is normalization?", "options": ["Data duplication", "Organizing data", "Deleting data", "Encrypting data"], "ans": "Organizing data"},
                {"q": "Which command is used to remove table?", "options": ["DELETE", "DROP", "TRUNCATE", "REMOVE"], "ans": "DROP"},
                {"q": "Which of these is a NoSQL DB?", "options": ["MySQL", "MongoDB", "Oracle", "PostgreSQL"], "ans": "MongoDB"},
                {"q": "What does ACID stand for in databases?", "options": ["Atomicity Consistency Isolation Durability", "Access Control Isolated Data", "Automatic Consistent Indexing Database", "None"], "ans": "Atomicity Consistency Isolation Durability"}
            ],
            "PYTHON": [
                {"q": "Which keyword defines a function?", "options": ["fun", "def", "function", "define"], "ans": "def"},
                {"q": "Which data type is immutable?", "options": ["List", "Set", "Dictionary", "Tuple"], "ans": "Tuple"},
                {"q": "Which operator is used for floor division?", "options": ["/", "//", "%", "**"], "ans": "//"},
                {"q": "Which function returns length of string?", "options": ["count()", "size()", "len()", "length()"], "ans": "len()"},
                {"q": "What is output of 2**3?", "options": ["5", "6", "8", "9"], "ans": "8"},
                {"q": "Which statement is used to handle exceptions?", "options": ["try/except", "if/else", "for/while", "switch/case"], "ans": "try/except"}
            ]
        }
        save(QUESTIONS_FILE, questions)
    scores = load(SCORES_FILE)
    if not isinstance(scores, dict):
        save(SCORES_FILE, {})

ensure_defaults()

logged_user = None
logged_role = None

def register():
    users = load(USERS_FILE)
    username = input("Choose username: ").strip()
    if not username:
        print("Username cannot be empty")
        return
    if username in users:
        print("Username already exists")
        return
    password = input("Choose password: ").strip()
    name = input("Full name: ").strip()
    email = input("Email: ").strip()
    phone = input("Contact number: ").strip()
    branch = input("Branch: ").strip()
    year = input("Year: ").strip()
    enrollment = input("Enrollment number: ").strip()
    users[username] = {
        "password": password,
        "name": name,
        "email": email,
        "phone": phone,
        "branch": branch,
        "year": year,
        "enrollment": enrollment,
        "role": "user"
    }
    save(USERS_FILE, users)
    print("Registration successful")

def login():
    global logged_user, logged_role
    users = load(USERS_FILE)
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username in users and users[username]["password"] == password:
        logged_user = username
        logged_role = users[username].get("role", "user")
        print(f"Logged in as {users[username].get('name','')}. Role: {logged_role}")
    else:
        print("Invalid credentials")

def show_profile():
    if not logged_user:
        print("Please login first")
        return
    users = load(USERS_FILE)
    p = users.get(logged_user)
    for k, v in p.items():
        if k != "password":
            print(f"{k.capitalize()}: {v}")

def update_profile():
    if not logged_user:
        print("Please login first")
        return
    users = load(USERS_FILE)
    p = users.get(logged_user)
    for field in ["name", "email", "phone", "branch", "year"]:
        current = p.get(field, "")
        new = input(f"{field.capitalize()} (current: {current}) new (leave blank to keep): ").strip()
        if new:
            p[field] = new
    users[logged_user] = p
    save(USERS_FILE, users)
    print("Profile updated")

def logout():
    global logged_user, logged_role
    if not logged_user:
        print("Not logged in")
        return
    print(f"{logged_user} logged out")
    logged_user = None
    logged_role = None

def attempt_quiz():
    if not logged_user:
        print("Please login to attempt quiz")
        return
    questions = load(QUESTIONS_FILE)
    cats = list(questions.keys())
    for i, c in enumerate(cats, start=1):
        print(f"{i}. {c}")
    choice = input("Choose category: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(cats):
        print("Invalid choice")
        return
    category = cats[int(choice)-1]
    qlist = questions.get(category, [])
    if not qlist:
        print("No questions in this category")
        return
    count = min(10, max(5, len(qlist)))
    if count > len(qlist):
        count = len(qlist)
    qsample = random.sample(qlist, count)
    score = 0
    total = len(qsample)
    for idx, q in enumerate(qsample, start=1):
        print(f"\nQ{idx}. {q['q']}")
        opts = q['options']
        random_opts = opts[:]
        random.shuffle(random_opts)
        for j, opt in enumerate(random_opts, start=1):
            print(f"  {j}. {opt}")
        ans = input("Enter option number: ").strip()
        if ans.isdigit() and 1 <= int(ans) <= len(random_opts):
            selected = random_opts[int(ans)-1]
            if selected == q['ans']:
                print("Correct")
                score += 1
            else:
                print(f"Wrong. Correct: {q['ans']}")
        else:
            print("Invalid input. Counted as wrong.")
    print(f"\nYour score: {score}/{total}")
    record = {
        "enrollment": load(USERS_FILE)[logged_user].get("enrollment", ""),
        "category": category,
        "score": f"{score}/{total}",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    scores = load(SCORES_FILE)
    if logged_user not in scores:
        scores[logged_user] = []
    scores[logged_user].append(record)
    save(SCORES_FILE, scores)

def show_my_scores():
    if not logged_user:
        print("Please login first")
        return
    scores = load(SCORES_FILE)
    user_scores = scores.get(logged_user, [])
    if not user_scores:
        print("No attempts yet")
        return
    for r in user_scores:
        print(f"{r['datetime']} | {r['category']} | {r['score']} | {r['enrollment']}")

def admin_view_all_scores():
    if logged_role != "admin":
        print("Admin access required")
        return
    scores = load(SCORES_FILE)
    for user, records in scores.items():
        print(f"\nUser: {user}")
        for r in records:
            print(f"  {r['datetime']} | {r['category']} | {r['score']} | {r['enrollment']}")

def admin_add_question():
    if logged_role != "admin":
        print("Admin access required")
        return
    questions = load(QUESTIONS_FILE)
    cats = list(questions.keys())
    for i, c in enumerate(cats, start=1):
        print(f"{i}. {c}")
    choice = input("Select category to add question or type new category name: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(cats):
        category = cats[int(choice)-1]
    else:
        category = choice
        if category not in questions:
            questions[category] = []
    qtext = input("Enter question text: ").strip()
    opts = []
    for i in range(1,5):
        o = input(f"Option {i}: ").strip()
        opts.append(o)
    ans = input("Enter the correct option text exactly as above: ").strip()
    questions[category].append({"q": qtext, "options": opts, "ans": ans})
    save(QUESTIONS_FILE, questions)
    print("Question added")

def menu():
    while True:
        print("\n1. Register\n2. Login\n3. Show Profile\n4. Update Profile\n5. Attempt Quiz\n6. Show My Scores\n7. Logout\n8. Exit")
        if logged_role == "admin":
            print("9. Admin: View All Scores\n10. Admin: Add Question")
        choice = input("Choose option: ").strip()
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            show_profile()
        elif choice == '4':
            update_profile()
        elif choice == '5':
            attempt_quiz()
        elif choice == '6':
            show_my_scores()
        elif choice == '7':
            logout()
        elif choice == '8':
            print("Goodbye")
            break
        elif choice == '9' and logged_role == "admin":
            admin_view_all_scores()
        elif choice == '10' and logged_role == "admin":
            admin_add_question()
        else:
            print("Invalid option")

if __name__ == "__main__":
    menu()