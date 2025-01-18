"""Simple wrapper around rdflib for reading in SHACL"""
from rdflib import Graph

def read(path: str) -> Graph:
    """
    Lightweight wrapper around rdflib.Graph.parse with some checks to make sure we're working with SHACL
    @param path: Path to RDF file
    @return: Graph object describing file at path
    """

    g = Graph()
    g.parse(path)

    # TODO: validate g

    return g