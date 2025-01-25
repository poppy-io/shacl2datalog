"""Classes for representing Datalog rules."""

from typing import Self

class Rule:
    """Representation of a Datalog rule."""

    def __init__(self, comments: list[str] = None, head: str = None, body: set[str] = None):
        self._comments = comments
        self._head = head
        self._body = body

    @property
    def comments(self):
        return self._comments

    @property
    def head(self):
        return self._head

    @property
    def body(self):
        return self._body

    def __str__(self) -> str:
        return (("//" + "\n//".join(self._comments) + "\n") if self._comments else ""
                + self._head + " :- "
                + (",\n" + " " * (len(self._head) + len(" :- "))).join(self._body) # align body terms
                + ".")

    def __repr__(self) -> str:
        return "Rule(" + str(self._comments) + ", " + self._head + ", " + str(self._body) + ")"

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other: Self) -> bool:
        return self.__repr__() == other.__repr__()


class Rules:
    """Container to hold a series of Rules with some convenience methods"""

    def __init__(self, comments: list[str] = None, declarations: list[str] = None, rules: set[Rule] = None) -> None:
        self._comments: list[str] = comments
        self._declarations: list[str] = declarations
        self._rules: set[Rule] = rules

    @property
    def comments(self) -> list[str]:
        return self._comments

    @property
    def declarations(self) -> list[str]:
        return self._declarations

    @property
    def rules(self) -> set[Rule]:
        return self._rules

    def __iadd__(self, other: Rule | Self) -> Self:
        """
        Augmented assignment to append a rule to the object
        @param other: Rule to be appended
        @return: self with other added
        """
        match other:
            case Rule():
                if self._rules:
                    self._rules.add(other)
                else:  # handle self._rules == None
                    self._rules = {other}
            case Rules():
                if self._rules:
                    self._rules |= other
                else:
                    self._rules = other
        return self

    def write(self, path: str) -> None:
        """
        Writes rules to a given file.

        If the file does not exist, it will be created. If it does, it will be overwritten.
        @param path: Path to file to be written to.
        """
        with open(path, "w", encoding="utf_8") as file:
            for rule in self._rules:
                file.write(str(rule) + "\n")

        # TODO: handling of malformed path either here or in main
