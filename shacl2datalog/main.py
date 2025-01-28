"""Script allowing CLI usage of the library."""

import pyshacl
import rdflib

from .datalog_shape_graph import DatalogShapesGraph

def main(*args, **kwargs) -> None:
    """Read a given SHACL file from a given path or URl and output equivalent Datalog rules
    to a given filepath."""

    graph = pyshacl.ShapesGraph(rdflib.Graph(args[0]))
    datalog = DatalogShapesGraph(graph).to_datalog()

    with open(args[1], 'w') as file:
        file.write(datalog)
