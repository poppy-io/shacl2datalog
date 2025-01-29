"""Script allowing CLI usage of the library."""

from .datalog_shape_graph import DatalogShapesGraph
from .read import read

def main(*args, **kwargs) -> None:
    """Read a given SHACL file from a given path or URl and output equivalent Datalog rules
    to a given filepath."""

    graph = read(args[0])
    datalog = DatalogShapesGraph(graph).to_datalog()

    with open(args[1], 'w') as file:
        file.write(datalog)
