from typing import Iterable

import pyshacl

FORBIDDEN_NAMES = {
    # validation rules
    "satisfied",
    "conforms",
    "target",
    "value_node",
    "path",

    # typing
    "instance_of",
    "subclass",
    "datatype",
    "node_kind",

    # properties of literals
    "value",
    "language",

    # properties of shapes
    "description",
    "severity",
    "message",
    "deactivated",
    "node_shape",
    "property_shape",
    "property_path",

    # constraints
    "min_count_constr",
    "max_count_constr",
    "not_constr",
    "and_constr",
    "and_shape",
    "or_constr",
    "or_shape",
    "xone_constr",
    "xone_shape",
    "equals_constr",
    "disjoint_constr",
    "less_than_constr",
    "less_than_or_eq_constr",
    "property_constr",
    "node_constr",
    "qualified_value_constr",
    "qualified_value_shape",
    "qualified_value_disjoint",
    "qualified_min_count",
    "qualified_max_count",
    "min_length_constr",
    "max_length_constr",
    "pattern_constr",
    "regex_match",
    "language_in_constr",
    "constr_language_tag",
    "unique_lang_constr",
    "class_constr",
    "datatype_constr",
    "node_kind_constr",
    "min_exclusive_constr",
    "min_inclusive_constr",
    "max_exclusive_constr",
    "max_inclusive_constr",
}

PERMITTED_INITIALS = ( "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     + "abcdefghijklmnopqrstuvwxyz"
                     + "_?" )

PERMITTED_CHARACTERS = ( "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                       + "abcdefghijklmnopqrstuvwxyz"
                       + "0123456789"
                       + "_?" )

def name(graph: pyshacl.ShapesGraph) -> tuple[list[tuple[str, pyshacl.shape.Shape]], set[str]]:
    """
    Associate each shape with a name so it can be referred to in Datalog.

    @param graph: Shape graph to be named
    @return: (name for shape, shape), namespace
    """

    namespace = FORBIDDEN_NAMES

    # can't use a generator; no point in returning a shape without a completed namespace
    named_shapes = []
    for shape in graph.shapes:
        named_shape, namespace = name_one_shape(shape, namespace)
        named_shapes.append(named_shape)
    return named_shapes, namespace


def name_one_shape(shape: pyshacl.ShapesGraph, namespace: set[str]) -> tuple[
    tuple[str, pyshacl.shape.Shape],
    set[str]
]:
    """
    Name a single shape, avoiding collisions in given namespace.

    Illegal characters in SHACL shape names will be replaced with a "?" character before collision
    checks.
    Split out into a separate function from name() above for use in some constraints.
    @param shape: Shape for naming.
    @param namespace: Set of names that can't be used.
    @return: (name for shape, shape), updated namespace
    """
    shape_name: str
    try:
        shape_name = next(shape.name)
    except StopIteration:
        shape_name = "shape"

    # handle illegal characters
    if shape_name[0] not in PERMITTED_INITIALS:
        shape_name = "?" + shape_name[1:]
    shape_name = "".join(c if c in PERMITTED_CHARACTERS else "?" for c in shape_name)

    # handle namespace collisions
    fixed_name = shape_name
    suffix: int = 0
    while fixed_name in namespace:
        fixed_name = shape_name + str(suffix)
        suffix += 1

    namespace.add(fixed_name)
    return (fixed_name, shape), namespace
