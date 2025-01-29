"""Script allowing CLI usage of the library."""

from .datalog_shape_graph import DatalogShapesGraph
from .read import read

def main(*args, **kwargs) -> None:
    """Read a given SHACL file from a given path or URl and output equivalent Datalog rules
    to a given filepath."""

    # hardcode a graph for testing until uv2nix behaves
    graph = read(r"https://raw.githubusercontent.com/w3c/data-shapes/refs/heads/gh-pages/data-shapes-test-suite/tests/core/complex/personexample.ttl")
    datalog = DatalogShapesGraph(graph).to_datalog()

    with open("out.dl", 'w') as file:
        file.write(datalog)
