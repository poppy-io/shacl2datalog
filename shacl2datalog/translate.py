"""Function to translate a SHACL triple to a Datalog rule."""

from .rules import Rule, Rules

from rdflib import Node, URIRef, BNode, Literal
from rdflib.namespace import XSD

from pyshacl.shape import Shape
from pyshacl.constraints import CONSTRAINT_PARAMETERS_MAP
from pyshacl.constraints.constraint_component import ConstraintComponent
from pyshacl.constraints.core.cardinality_constraints import MaxCountConstraintComponent, MinCountConstraintComponent
from pyshacl.constraints.core.logical_constraints import (
    AndConstraintComponent,
    NotConstraintComponent,
    OrConstraintComponent,
    XoneConstraintComponent,
)
from pyshacl.constraints.core.other_constraints import (
    ClosedConstraintComponent,
    HasValueConstraintComponent,
    InConstraintComponent,
)
from pyshacl.constraints.core.property_pair_constraints import (
    DisjointConstraintComponent,
    EqualsConstraintComponent,
    LessThanConstraintComponent,
    LessThanOrEqualsConstraintComponent,
)
from pyshacl.constraints.core.shape_based_constraints import (
    NodeConstraintComponent,
    PropertyConstraintComponent,
    QualifiedValueShapeConstraintComponent,
)
from pyshacl.constraints.core.string_based_constraints import (
    LanguageInConstraintComponent,
    MaxLengthConstraintComponent,
    MinLengthConstraintComponent,
    PatternConstraintComponent,
    UniqueLangConstraintComponent,
)
from pyshacl.constraints.core.value_constraints import (
    ClassConstraintComponent,
    DatatypeConstraintComponent,
    NodeKindConstraintComponent,
)
from pyshacl.constraints.core.value_range_constraints import (
    MaxExclusiveConstraintComponent,
    MaxInclusiveConstraintComponent,
    MinExclusiveConstraintComponent,
    MinInclusiveConstraintComponent,
)


def shape_to_rules(shape: Shape) -> Rules:
    """

    @param shape: Shape to be translated
    @return: Equivalent Rule object
    """

    # TODO: implement deactivated shape handling
    # TODO: implement shape severity
    # TODO: implement shape messages

    shape_comments = ["Name(s): " + ", ".join(list(shape.name())),
                      "Description(s):"] + list(shape.description())
    rules = Rules(shape_comments)

    if shape.is_property_shape():
        ...
    else:
        heads = targets_to_heads(*shape.target())
        constraints = [CONSTRAINT_PARAMETERS_MAP[p](shape) for p, _
                       in shape.sg.predicate_objects(shape.node)]
        bodies = set(constraint_to_body(constraints))
        for head in heads:
            rules += Rule(comments, head, bodies)

    return rules


def targets_to_heads(target_nodes, target_classes, implicit_targets, target_objects_of,
                     target_subjects_of) -> tuple[list[str], list[str]]:
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
            + [p[0].lower() + p[1:] + "(_, X)" for p in (str(t.toPython()) for t in
                                                         target_objects_of)]
            + [p[0].lower() + p[1:] + "(X, _)" for p in (str(t.toPython()) for t in
                                                         target_subjects_of)],

              [".decl X"])


def constraints_to_bodies(constraints: Iterable[ConstraintComponent]) -> Iterator[str]:
    """

    @param constraints:
    @return:
    """

    # appended to symbols for a constraint and then incremented to avoid namespace conflicts
    alpha: int = 0

    for c in constraints:
        match c:
            # Cardinal constraints
            case MinCountConstraintComponent():
                min_count = int(c.min_count.value)
                if min_count == 0:
                    continue
                ...
            case MaxCountConstraintComponent():
                max_count = int(c.max_count.value)
                ...

            # Logical constraints
            case NotConstraintComponent():
                for not_c in c.not_list:
                    yield ...
            case AndConstraintComponent():
                for and_c in c.and_list:
                    yield ...
            case OrConstraintComponent():
                for or_c in c.or_list:
                    yield ...
            case XoneConstraintComponent():
                for xone_c in c.xone_nodes:
                    yield ...

            # Property pair constraints
            case EqualsConstraintComponent():
                ...
            case DisjointConstraintComponent():
                ...
            case LessThanConstraintComponent():
                ...
            case LessThanOrEqualsConstraintComponent():
                ...

            # Shape-based constraints
            case PropertyConstraintComponent():
                ...
            case NodeConstraintComponent():
                ...
            case QualifiedValueShapeConstraintComponent():
                ...

            # String-based constraints
            case MinLengthConstraintComponent():
                ...
            case MaxLengthConstraintComponent():
                ...
            case PatternConstraintComponent():
                ...
            case LanguageInConstraintComponent():
                ...
            case UniqueLangConstraintComponent():
                ...

            # Value constraints
            case ClassConstraintComponent():
                ...
            case DatatypeConstraintComponent():
                ...
            case NodeKindConstraintComponent():
                ...

            # Value range constraints
            case MinExclusiveConstraintComponent():
                ...
            case MinInclusiveConstraintComponent():
                ...
            case MaxExclusiveConstraintComponent():
                ...
            case MaxInclusiveConstraintComponent():
                ...

            # Other constraints
            case InConstraintComponent():
                ...
            case ClosedConstraintComponent():
                ...
            case HasValueConstraintComponent():
                ...

            case _:
                raise NotImplementedError("Constraint not implemented: " + constr)


# WARNING: all functions from this point on likely to be removed with no warning in a future version
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
            raise ValueError("NOTATION literal passed to literal_to_datalog:", node)
        case _:
            raise ValueError("Literal datatype not handled: " + str(node.datatype))
