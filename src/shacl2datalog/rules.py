"""Classes for representing Datalog rules."""

from typing import Self

class Rule:
    """Representation of a Datalog rule."""

    def __init__(self, head: str, body: Set[str]):
        self.head = head
        self.body = body

    def __str__(self) -> str:
        return "(<- " + self.head + "\n".join(self.body) + ")"

    def __repr__(self) -> str:
        return "Rule(" + self.head + str(self.body) + ")"


class Rules:
    """Container to hold a series of Rules with some convenience methods"""

    def __init__(self, rules: set[Rule] = None) -> None:
        self._rules: set[Rule] = rules

    def __iadd__(self, other: Rule) -> Self:
        """
        Augmented assignment to append a rule to the object
        @param other: Rule to be appended
        @return: self with other added
        """
        if self._rules:
            self._rules += other
        else:  # handle self._rules == None
            self._rules = {other}

        return self

    def write(self, path: str) -> None:
        """
        Writes rules to a given file.

        If the file does not exist, it will be created. If it does, it will be overwritten.
        @param path: Path to file to be written to.
        """
        with open(path, "w", encoding="utf_8") as file:
            # necessary for all time-related type handling, but may not be needed for all graphs
            file.write("(require '[java-time.api :as jt])")
            for rule in self._rules:
                file.write(str(rule))

        # TODO: handling of malformed path either here or in main
