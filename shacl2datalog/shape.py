"""Classes to provide wrappers around pySHACL shapes."""

from .rules import Rule

from typing import Iterator, Iterable

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


# Used in order to prevent namespace clashes.
# TODO: handle declarations for "builtins"
# TODO: consider adding sh:order, sh:group, sh:defaultValue,
namespace = {"description", "severity", "message", "deactivated", "conforms"}


class DatalogShape:
    """ """

    def __init__(self, shape: Shape) -> None:
        """

        @param shape: pySHACL shape object to wrap
        """
        global namespace

        self._shape = shape
        # FIXME: handle multiple names more gracefully
        name: str = next(shape.name) if shape.name else "shape"
        suffix: int = 0
        while name in namespace:
            name = shape.name + str(suffix)
            suffix += 1

        self._name = name
        namespace.add(name)

        self._declarations = set()
        self._rules = {}

        self._rules |= set(Rule(head=f"description({name}, {desc})") for desc in shape.description)
        self._rules.add(Rule(head=f"severity({name}, {shape.severity})"))
        self._rules |= set(Rule(head=f"message({name}, {msg})") for msg in shape.message)
        if shape.deactivated:
            self._rules.add(Rule(head=f"deactivated({name})"))
        self._rules.add(Rule(head=f"satisfied({name})", body={f"deactivated({name})"}))

        self._constraints = [CONSTRAINT_PARAMETERS_MAP[p](shape) for p, _
                       in shape.sg.predicate_objects(shape.node)]
        self.propagate_constraints()

    @property
    def shape(self) -> Shape:
        return self._shape

    @property
    def name(self) -> str:
        return self._name

    def head(self) -> str:
        """Convenience method to generate a head for this shape."""
        return f"satisfied({self.name})"

    def propagate_constraints(self) -> None:
        """Process self._constraints in order to populate comments, declarations, and rules."""

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
                    f"instance-of({...}, {...})"
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
