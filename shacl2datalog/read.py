"""Simple wrapper around rdflib for reading in SHACL"""

import rdflib
import pyshacl

def read(path: str) -> rdflib.Graph:
    """
    Lightweight wrapper around rdflib.Graph.parse with some checks to make sure we're working
    with SHACL.
    @param path: Path to RDF file
    @return: Graph object describing file at path
    """

    g = rdflib.Graph()

    try:
        g.parse(location=path, format="application/rdf+xml")
    except SyntaxError as se:
        print("Graph is not valid RDF. Please check the provided path and file.")
        raise se

    try:
        sg = pyshacl.ShapesGraph(g)
    except pyshacl.ShapeLoadError as sle:
        print("Graph is not valid SHACL.")
        raise sle

    return sg
