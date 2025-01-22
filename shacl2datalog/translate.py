"""Function to translate a SHACL triple to a Datalog rule."""

from .rules import Rule
from rdflib import Node, URIRef, BNode, Literal
from rdflib.namespace import XSD
from decimal import Decimal
from pyshacl import Shape


def shape_to_rules(shape: Shape) -> Rules:
    """

    @param triple: Triple to be translated
    @return: Equivalent Rule object
    """
    #TODO: implement deactivated shape handling
    #TODO: implement shape severity
    #TODO: implement shape messages

    rules = Rules()
    if shape.is_property_shape():
        ...
    else:
        comments = ["Name(s): " + ", ".join(list(shape.name())),
                    "Description(s): " + "; ".join(list(shape.description()))]
        heads = targets_to_heads(*shape.target())
        bodies = ...
        for head in heads:
            rules += Rule(comments, head, bodies)


def targets_to_heads(target_nodes, target_classes, implicit_targets, target_objects_of,
                     target_subjects_of) -> list[str]:
    """

    @param target_nodes:
    @param target_classes:
    @param implicit_targets:
    @param target_objects_of:
    @param target_subjects_of:
    @return:
    """
    return (  [p[0].lower() + p[1:] for p in (str(t.toPython()) for t in target_nodes)]
            + [p[0].lower() + p[1:] + "(X)" for p in (str(t.toPython()) for t in target_classes)]
            + [p[0].lower() + p[1:] + "(X)" for p in (str(t.toPython()) for t in implicit_targets)]
            + [p[0].lower() + p[1:] + "(_, X)" for p in (str(t.toPython()) for t in target_objects_of)]
            + [p[0].lower() + p[1:] + "(X, _)" for p in (str(t.toPython()) for t in target_subjects_of)])


def node_to_datalog(node: Node) -> str:
    """
    Translates a Node object to an equivalent Datalog representation.

    @param node: Node object to be translated
    @return: Datalog string representing the node
    """
    match node:
        case URIRef():
            return uriref_to_datalog(node)
        case BNode():
            return bnode_to_datalog(node)
        case Literal():
            return literal_to_datalog(node)
        case _:
            raise ValueError("Node type not handled: " + str(Node))


def uriref_to_datalog(node: URIRef) -> str:
    """

    @param node:
    @return:
    """
    ...


def bnode_to_datalog(node: BNode) -> str:
    """

    @param node:
    @return:
    """
    ...


def literal_to_datalog(node: Literal) -> str:
    """
    Translate a literal into an equivalent string representation in Datalog
    @param node: The Literal node to be translated
    @return: The Datalog translation of the literal
    """
    match node.datatype():
        case XSD.boolean:
            ...
        case XSD.str | XSD.base64Binary | XSD.hexBinary | XSD.anyURI:
            ...
        case XSD.integer:
            ...
        case XSD.float | XSD.double:
            ...
        case XSD.decimal:
            ...

        # Time related types
        case XSD.duration:
            ...
        case XSD.gYear:
            ...
        case XSD.gYearMonth:
            ...
        case XSD.gMonthDay:
            ...
        case XSD.gDay:
            ...
        case XSD.gMonth:
            ...
        case XSD.time | XSD.date | XSD.dateTime:
            ...

        case XSD.QName:
            ...
        case XSD.NOTATION:
            raise ValueError("NOTATION node passed to literal_to_datalog:", node)
        case _:
            raise ValueError("Literal datatype not handled: " + str(node.datatype))
