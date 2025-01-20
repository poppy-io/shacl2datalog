"""Function to translate a SHACL triple to a Datalog rule."""

from .rules import Rule
from rdflib import Node, URIRef, BNode, Literal
from rdflib.namespace import XSD
from decimal import Decimal


def triple_to_rule(triple: Tuple[Node, Node, Node]) -> Rule:
    """

    @param triple: Triple to be translated
    @return: Equivalent Rule object
    """
    subj, pred, obj = triple
    ...


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
    Translate a literal into an equivalent string representation in Clojure Datalog
    @param node: The Literal node to be translated
    @return: The Datalog translation of the literal
    """
    match node.datatype():
        case XSD.boolean:
            return "true" if node.toPython() else "false"
        case XSD.str | XSD.base64Binary | XSD.hexBinary | XSD.anyURI:
            return '"' + str(node.toPython()) + '"'
        case XSD.integer:
            return str(int(node.toPython()))
        case XSD.float | XSD.double:
            return str(float(node.toPython()))
        case XSD.decimal:
            return str(Decimal(node.toPython()))

        # Time related types
        case XSD.duration:
            return "(jt/duration " + str(node.toPython) + ")"
        case XSD.gYear:
            return "(jt/year " + str(node.toPython) + ")"
        case XSD.gYearMonth:
            return "(jt/year-month " + str(node.toPython()) + ")"
        case XSD.gMonthDay:
            return "(jt/month-day " + str(node.toPython()) + ")"
        case XSD.gDay:
            return "(jt/day-of-month " + str(node.toPython()) + ")"
        case XSD.gMonth:
            return "(jt/month " + str(node.toPython()) + ")"
        case XSD.time | XSD.date | XSD.dateTime:
            return "(jt/instant " + str(node.toPython()) + ")"

        case XSD.QName:
            return str(node.toPython())
        case XSD.NOTATION:
            raise ValueError("NOTATION node passed to literal_to_datalog:", node)
        case _:
            raise ValueError("Literal datatype not handled: " + str(node.datatype))
