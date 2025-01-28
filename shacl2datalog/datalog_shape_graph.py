import pyshacl
import rdflib


class DatalogShapesGraph:
    """ Wrapper around a pySHACL ShapeGraph. """

    def __init__(self, graph: pyshacl.ShapesGraph) -> None:
        self._shapes = self.name(graph)

    @property
    def shapes(self) -> list[tuple[str, pyshacl.shape.Shape]]:
        return self._shapes

    def to_datalog(self) -> str:
        """ Return Datalog text expressing self._graph """

        # import library file (even though path will likely be edited by end user)
        datalog: str = ".include shacl.dl\n\n"

        for shape in self.shapes:
            datalog += shape_to_datalog(*shape)

        return datalog


def name(graph: pyshacl.ShapesGraph) -> list[tuple[str, pyshacl.shape.Shape]]:
    # TODO: add reserved symbols to namespace
    namespace = set()
    named = []

    for shape in graph.shapes:
        named_shape, namespace = name_one_shape(shape, namespace)
        named.append(named_shape)

    return named


def name_one_shape(shape: pyshacl.ShapesGraph, namespace: set[str]) -> tuple[
    tuple[str, pyshacl.shape.Shape],
    set[str]
]:
    """
    Name a single shape, avoiding collisions in given namespace.

    Split out into a separate function from name() above for use in some constraints.
    @param shape: Shape for naming.
    @param namespace: Set of names that can't be used.
    @return: (name for shape, shape), updated namespace
    """
    # TODO: strip illegal characters
    shape_name: str = next(shape.name)
    shape_name = shape_name if shape_name else "shape"

    # handle namespace collisions
    fixed_name = shape_name
    suffix: int = 0
    while fixed_name in namespace:
        fixed_name = shape_name + str(suffix)
        suffix += 1

    namespace.add(fixed_name)
    # TODO: consider if shape would ever actually need to be passed back out here?
    return (fixed_name, shape), namespace


def node_to_str(node: rdflib.term.Node) -> str:
    """
    Convenience method to get a sanitised string value from an RDF node.
    @param node: the node to extract the value from
    """
    # TODO: sanitise the value literally even slightly
    return str(node.toPython())


def shape_to_datalog(name: str, shape: pyshacl.shape.Shape, namespace: set[str] = None) -> tuple[
                                                                                           str,
                                                                                           set[str]]:
    """
    Translates a Shape object into an equivalent datalog string.
    @param name: the name of the shape
    @param shape: the shape to be translated
    @return: the translated datalog string
    """

    datalog: str = ""

    # many attributes of Shapes are given as iterables
    # (presumably due to multiple language translations)
    datalog += "\n".join(f"description({name}, {desc})." for desc in shape.description) + "\n"
    datalog += "\n".join(f"message({name}, {msg})." for msg in shape.message) + "\n"

    if shape.deactivated:
        datalog += f"deactivated({name}).\n"

    datalog += f"severity({name}, {shape.severity}).\n"

    datalog += f"property_shape({name}).\n" \
                if shape.is_property_shape \
                else f"node_shape({name}).\n"

    # translate targets of shape
    datalog += "\n".join(f"target({name}, {n})." for n in
                         map(node_to_str, shape.target_nodes())) + "\n"
    datalog += "\n".join(f"target({name}, node) :- instance_of({c}, node)." for c in
                         map(node_to_str, shape.target_classes())) + "\n"
    datalog += "\n".join(f"target({name}, node) :- instance_of({c}, node)." for c in
                         map(node_to_str, shape.implicit_class_targets())) + "\n"
    datalog += "\n".join(f"target({name}, node) :- path(_, {p}, node)." for p in
                         map(node_to_str, shape.target_objects_of())) + "\n"
    datalog += "\n".join(f"target({name}, node) :- path(node, {p}, _)." for p in
                         map(node_to_str, shape.target_subjects_of())) + "\n"

    # construct iterable of constraint objects from shape
    for c in (pyshacl.constraints.CONSTRAINT_PARAMETERS_MAP[p](shape)
              for p, _
              in shape.sg.predicate_objects(shape.node)
              if p in pyshacl.constraints.ALL_CONSTRAINT_PARAMETERS):
        match c:
            # Cardinal constraints
            case MinCountConstraintComponent():
                min_count = int(c.min_count.value)
                if min_count == 0:
                    continue
                datalog += f"min_count_constr({name}, {min_count}).\n"
            case MaxCountConstraintComponent():
                max_count = int(c.max_count.value)
                datalog += f"max_count_constr({name}, {max_count}).\n"

            # Logical constraints
            case NotConstraintComponent():
                for not_c in c.not_list:
                    datalog += f"not_constr({name}, {node_to_str(not_c)}).\n"
            case AndConstraintComponent():
                datalog += f"and_constr({name}).\n"
                for and_c in c.and_list:
                    datalog += f"and_shape({name}, {node_to_str(and_c)}).\n"
            case OrConstraintComponent():
                datalog += f"or_constr({name}).\n"
                for or_c in c.or_list:
                    datalog += f"or_shape({name}, {node_to_str(or_c)}.\n"
            case XoneConstraintComponent():
                datalog += f"xone_constr({name}).\n"
                for xone_c in c.xone_nodes:
                    datalog += f"xone_shape({name}, {node_to_str(xone_c)}).\n"

            # Property pair constraints
            case EqualsConstraintComponent():
                for pred in c.property_compare_set:
                    datalog += f"equals_constr({name}, {node_to_str(pred)}).\n"
            case DisjointConstraintComponent():
                for pred in c.property_compare_set:
                    datalog += f"disjoint_constr({name}, {node_to_str(pred)}).\n"
            case LessThanConstraintComponent():
                for pred in c.property_compare_set:
                    datalog += f"less_than_constr({name}, {node_to_str(pred)}.\n"
            case LessThanOrEqualsConstraintComponent():
                for pred in c.property_compare_set:
                    datalog += f"less_than_or_eq_constr({name}, {node_to_str(pred)}.\n"

            # Shape-based constraints
            case PropertyConstraintComponent():
                for shape_node in c.property_shapes:
                    other_shape = shape.get_other_shape(shape_node)
                    # there's no need to worry about tail recursion etc. here; depth will never be
                    # any higher than one or possibly two in some niche cases
                    if namespace:
                        (other_name, _), namespace = name_one_shape(other_shape, namespace)
                    else:
                        # shortcut to output of name_one_shape on an empty set
                        other_name = "shape"
                    shape_datalog, namespace = shape_to_datalog(other_name, other_shape, namespace)
                    datalog += shape_datalog
                    datalog += "property_constr(name, other_name).\n"
            case NodeConstraintComponent():
                for shape_node in c.node_shapes:
                    other_shape = shape.get_other_shape(shape_node)
                    if namespace:
                        (other_name, _), namespace = name_one_shape(other_shape, namespace)
                    else:
                        other_name = "shape"
                    shape_datalog, namespace = shape_to_datalog(other_name, other_shape, namespace)
                    datalog += shape_datalog
                    datalog += f"node_constr({name}, {other_name}).\n"
            case QualifiedValueShapeConstraintComponent():
                for shape_node in c.value_shapes:
                    other_shape = shape.get_other_shape(shape_node)
                    if namespace:
                        (other_name, _), namespace = name_one_shape(other_shape, namespace)
                    else:
                        other_name = "shape"
                    shape_datalog, namespace = shape_to_datalog(other_name, other_shape, namespace)
                    datalog += shape_datalog
                    datalog += f"qualified_value_shape({name}, {other_name}).\n"
                if c.min_count:
                    datalog += f"qualified_min_count({name}, {c.min_count}).\n"
                if c.max_count:
                    datalog += f"qualified_max_count({name}, {c.max_count}).\n"
                if c.is_disjoint:
                    datalog += f"qualified_value_disjoint({name}).\n"
                datalog += f"qualified_value_constr({name}).\n"

            # String-based constraints
            case MinLengthConstraintComponent():
                # yes, this is the best way to access the length constraints for these
                datalog += f"min_length_constr({name}, {c.string_rules[0].value}).\n"
            case MaxLengthConstraintComponent():
                datalog += f"max_length_constr({name}, {c.string_rules[0].value}).\n"
            case PatternConstraintComponent():
                datalog += f"pattern_constr({name}, {c.string_rules[0].value}).\n"
            case LanguageInConstraintComponent():
                for language in c.string_rules:
                    datalog += f"constr_language_tag({name}, {language.value}).\n"
                datalog += f"language_in_constr({name}).\n"
            case UniqueLangConstraintComponent():
                datalog += f"unique_lang_constr({name}).\n"

            # Value constraints
            case ClassConstraintComponent():
                for class_rule in c.class_rules:
                    datalog += f"class_constr({name}, {class_rule.value}).\n"
            case DatatypeConstraintComponent():
                datalog += f"datatype_constr({name}, {c.datatype_rule.value}).\n"
            case NodeKindConstraintComponent():
                datalog += f"node_kind_constr({name}, {c.nodekind_rule.value}).\n"

            # Value range constraints
            case MinExclusiveConstraintComponent():
                for min_val in c.min_vals:
                    # TODO: might need to handle types more explicitly here; LOTS are accepted
                    datalog += f"min_exclusive_constr({name}, {min_val.value}).\n"
            case MinInclusiveConstraintComponent():
                for min_val in c.min_vals:
                    datalog += f"min_inclusive_constr({name}, {min_val.value}).\n"
            case MaxExclusiveConstraintComponent():
                for max_val in c.max_vals:
                    datalog += f"max_exclusive_constr({name}, {max_val.value}).\n"
            case MaxInclusiveConstraintComponent():
                for max_val in c.max_vals:
                    datalog += f"max_inclusive_constr({name}, {max_val.value}).\n"

            # Other constraints

            case _:
                raise NotImplementedError("Constraint not implemented: " + constr)

    return datalog, namespace
