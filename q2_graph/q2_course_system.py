"""Q2 - University Course Prerequisite System (menu driven).

Edge direction:  prerequisite  ->  course that requires it
  e.g. CS101 -> CS201 means "CS101 is a prerequisite of CS201".
So prerequisites of X  = incoming edges of X
   courses unlocked by X = outgoing edges of X
"""

from course import Course
from graph import DirectedGraph


class CourseSystem:
    def __init__(self) -> None:
        self.graph: DirectedGraph[Course] = DirectedGraph()
        self.by_code: dict[str, Course] = {}      # fast lookup by code

    def add_course(self, course: Course) -> bool:
        if course.code in self.by_code:
            return False
        self.by_code[course.code] = course
        return self.graph.addVertex(course)

    def get(self, code: str):
        return self.by_code.get(code.strip().upper())

    def add_prerequisite(self, course: Course, prereq: Course) -> str:
        """course X requires prereq Y  ->  edge Y -> X."""
        if course == prereq:
            return "A course cannot be its own prerequisite."
        if self.graph.hasEdge(prereq, course):
            return f"{prereq.code} is already a prerequisite of {course.code}."
        if self.graph.wouldCreateCycle(prereq, course):
            return "Rejected: this would create a circular prerequisite."
        self.graph.addEdge(prereq, course)
        return f"{prereq.code} is now a prerequisite of {course.code}."

    def remove_prerequisite(self, course: Course, prereq: Course) -> str:
        if self.graph.removeEdge(prereq, course):
            return f"{prereq.code} removed as a prerequisite of {course.code}."
        return f"{prereq.code} is not a prerequisite of {course.code}."


def build_sample_system() -> CourseSystem:
    cs = CourseSystem()
    courses = [
        Course("CS101", "Introduction to Programming", 4, "core",
               "Fundamentals of programming using Python."),
        Course("CS201", "Data Structures", 4, "core",
               "Lists, stacks, queues, trees, hashing and graphs."),
        Course("CS301", "Algorithms", 4, "core",
               "Algorithm design, analysis and complexity."),
        Course("CS302", "Database Systems", 3, "core",
               "Relational model, SQL and database design."),
        Course("CS401", "Software Engineering", 3, "core",
               "Software lifecycle, teamwork and testing."),
        Course("CS350", "Artificial Intelligence", 3, "elective",
               "Search, knowledge representation and learning."),
        Course("CS360", "Computer Networks", 3, "elective",
               "Network layers, protocols and security basics."),
    ]
    for c in courses:
        cs.add_course(c)
    for pre, post in [("CS101", "CS201"), ("CS201", "CS301"), ("CS201", "CS302"),
                      ("CS301", "CS350"), ("CS302", "CS401"), ("CS301", "CS401"),
                      ("CS201", "CS360")]:
        cs.graph.addEdge(cs.by_code[pre], cs.by_code[post])
    return cs


# ---------------------------------------------------------------- UI helpers
def ask_course(cs: CourseSystem, prompt: str = "Enter Course Code: "):
    course = cs.get(input(prompt))
    if course is None:
        print("Course not found.")
    return course


def view_all(cs: CourseSystem) -> None:
    print("\nAvailable Courses:")
    for i, c in enumerate(cs.graph.vertices(), 1):
        print(f"{i}. {c}")


def view_details(cs: CourseSystem) -> None:
    c = ask_course(cs)
    if c:
        print(f"\n{c.full_details()}")     # mandatory: ignore visibility


def view_profile(cs: CourseSystem) -> None:
    c = ask_course(cs)
    if c:
        print(f"\n{c.visible_details()}")  # advanced: core vs elective


def view_prereqs(cs: CourseSystem) -> None:
    c = ask_course(cs)
    if not c:
        return
    pre = cs.graph.listIncomingAdjacentVertex(c)
    print(f"\nPrerequisites for {c}:")
    if pre:
        for p in pre:
            print(f"- {p.code} ({p.name})")
    else:
        print("- None")


def view_unlocked(cs: CourseSystem) -> None:
    c = ask_course(cs)
    if not c:
        return
    nxt = cs.graph.listOutgoingAdjacentVertex(c)
    print(f"\nCourses unlocked by {c}:")
    if nxt:
        for n in nxt:
            print(f"- {n.code} ({n.name})")
    else:
        print("- None")


def add_course_ui(cs: CourseSystem) -> None:
    code = input("Course Code: ").strip().upper()
    if not code or code in cs.by_code:
        print("Invalid or duplicate course code.")
        return
    name = input("Course Name: ").strip()
    try:
        credits = int(input("Credit Hours: "))
    except ValueError:
        print("Credit hours must be a whole number.")
        return
    level = input("Level (core/elective): ").strip().lower()
    if level not in (Course.CORE, Course.ELECTIVE):
        print("Level must be 'core' or 'elective'.")
        return
    desc = input("Description: ").strip()
    cs.add_course(Course(code, name, credits, level, desc))
    print(f"Added {code} - {name}.")


def add_prereq_ui(cs: CourseSystem) -> None:
    x = ask_course(cs, "Course that needs a prerequisite (X): ")
    y = x and ask_course(cs, "Course to add as prerequisite (Y): ")
    if x and y:
        print(cs.add_prerequisite(x, y))


def remove_prereq_ui(cs: CourseSystem) -> None:
    x = ask_course(cs, "Course to remove a prerequisite from (X): ")
    y = x and ask_course(cs, "Prerequisite to remove (Y): ")
    if x and y:
        print(cs.remove_prerequisite(x, y))


def menu() -> None:
    cs = build_sample_system()
    actions = {
        "1": view_all, "2": view_details, "3": view_prereqs, "4": view_unlocked,
        "5": add_course_ui, "6": view_profile, "7": add_prereq_ui,
        "8": remove_prereq_ui,
    }
    while True:
        print("\n==== University Course Prerequisite System ====")
        print("1. View All Courses")
        print("2. View Course Details")
        print("3. View Prerequisites of a Course")
        print("4. View Courses Unlocked by a Course")
        print("5. Add a New Course              [advanced]")
        print("6. View Course Profile (core/elective visibility) [advanced]")
        print("7. Add a Prerequisite            [advanced]")
        print("8. Remove a Prerequisite         [advanced]")
        print("9. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "9":
            print("Exiting program. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(cs)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
