"""Script allowing CLI usage of the library."""

from rdflib import Graph
from .read import read
from .rules import Rules
from .translate import triple_to_rule

def main(*args, **kwargs) -> None:
    """Read a given SHACL file from a given path or URl and output equivalent Datalog rules
    to a given filepath."""

    datalog: Rules = Rules()
    shacl: Graph = read(args[0])
    for triple in shacl:
        datalog += triple_to_rule(triple)

    datalog.write(args[1])
