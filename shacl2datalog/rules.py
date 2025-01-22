"""Classes for representing Datalog rules."""

from typing import Self

class Rule:
    """Representation of a Datalog rule."""

    def __init__(self, head: str, body: set[str]):
        self._head = head
        self._body = body

    @property
    def head(self):
        return self._head

    @property
    def body(self):
        return self._body

    def __str__(self) -> str:
        return self.__head + " :- " + ", ".join(self._body) + "."

    def __repr__(self) -> str:
        return "Rule(" + self._head + ", " + str(self._body) + ")"

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other: Rule) -> bool:
        return self.__repr__() == other.__repr__()


class Rules:
    """Container to hold a series of Rules with some convenience methods"""

    def __init__(self, rules: set[Rule] = None) -> None:
        self._rules: set[Rule] = rules

    @property
    def rules(self) -> set[Rule]:
        return self.rules

    def __iadd__(self, other: Rule | Rules) -> Self:
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
