"""Script allowing CLI usage of the library."""

from .read import read
from rdflib import Graph
from .rules import Rules, Rule

def main(*args, **kwargs) -> None:
    """Read a given SHACL file from a given path or URl and output equivalent Datalog rules
    to a given filepath."""

    datalog: Rules = Rules()
    shacl: Graph = read(args[0])
    for triple in shacl:
        datalog += triple_to_rule(triple)

    datalog.write(args[1])
