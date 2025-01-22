"""Script allowing CLI usage of the library."""

import rdflib
import pyshacl
from .read import read
from .rules import Rules
from .translate import shape_to_rules

def main(*args, **kwargs) -> None:
    """Read a given SHACL file from a given path or URl and output equivalent Datalog rules
    to a given filepath."""

    datalog: Rules = Rules()
    graph: pyshacl.ShapesGraph = read(args[0])

    for shape in graph.shapes():
        datalog += shape_to_rules(shape)

    datalog.write(args[1])
