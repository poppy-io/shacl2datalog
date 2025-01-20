""""""

from read import read
from rdflib import Graph
from rules import Rules

def main(*args, **kwargs) -> None:
    """Read a given SHACL file from a given path or URl and output equivalent Datalog rules
    to a given filepath."""
    shacl: Graph = read(args[0])
    datalog: Rules = ...
    datalog.write(args[1])
