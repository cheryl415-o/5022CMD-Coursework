"""Entity class for a university course."""


class Course:
    CORE = "core"
    ELECTIVE = "elective"

    def __init__(self, code: str, name: str, credit_hours: int,
                 level: str, description: str = "") -> None:
        self.code = code.upper()
        self.name = name
        self.credit_hours = credit_hours
        self.level = level.lower()        # "core" or "elective"
        self.description = description

    def is_core(self) -> bool:
        return self.level == Course.CORE

    def full_details(self) -> str:
        return (f"Course Code  : {self.code}\n"
                f"Course Name  : {self.name}\n"
                f"Credit Hours : {self.credit_hours}\n"
                f"Level        : {self.level.capitalize()}\n"
                f"Description  : {self.description}")

    def visible_details(self) -> str:
        """Electives only reveal their name; core courses show everything."""
        if self.is_core():
            return self.full_details()
        return f"Course Name  : {self.name}\n(Details hidden for elective courses)"

    # Course objects are used as graph vertices, so make them hashable by code.
    def __hash__(self) -> int:
        return hash(self.code)

    def __eq__(self, other) -> bool:
        return isinstance(other, Course) and self.code == other.code

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
