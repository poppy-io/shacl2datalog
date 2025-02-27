import pyshacl

from .name import name_one_shape
from .term_to_datalog import term_to_datalog


def shape_to_datalog(name: str, shape: pyshacl.shape.Shape, namespace: set[str] | None = None) -> tuple[
                                                                                           str,
                                                                                           set[str] | None]:
    """
    Translates a Shape object into an equivalent datalog string.

    @param name: the name of the shape
    @param shape: the shape to be translated
    @param namespace: set of names to avoid collision with
    @return: the translated datalog string, updated namespace
    """

    datalog: str = ""

    # many attributes of Shapes are given as iterables
    # (presumably due to multiple language translations)
    datalog += "\n".join(f"description({name}, {desc})." for desc in shape.description) + "\n"
    datalog += "\n".join(f"message({name}, {msg})." for msg in shape.message) + "\n"

    if shape.deactivated:
        datalog += f"deactivated({name}).\n"

    datalog += f"severity({name}, \"{shape.severity}\").\n"

    datalog += f"property_shape({name}).\n" \
                if shape.is_property_shape \
                else f"node_shape({name}).\n"

    # translate targets of shape
    datalog += "\n".join(f"target({name}, {n})." for n in
                         map(term_to_datalog, shape.target_nodes())) + "\n"
    datalog += "\n".join(f"target({name}, node) :- instance_of({c}, node)." for c in
                         map(term_to_datalog, shape.target_classes())) + "\n"
    datalog += "\n".join(f"target({name}, node) :- instance_of({c}, node)." for c in
                         map(term_to_datalog, shape.implicit_class_targets())) + "\n"
    datalog += "\n".join(f"target({name}, node) :- path(_, {p}, node)." for p in
                         map(term_to_datalog, shape.target_objects_of())) + "\n"
    datalog += "\n".join(f"target({name}, node) :- path(node, {p}, _)." for p in
                         map(term_to_datalog, shape.target_subjects_of())) + "\n"

    # construct iterable of constraint objects from shape
    for c in (pyshacl.constraints.CONSTRAINT_PARAMETERS_MAP[p](shape)
              for p, _
              in shape.sg.predicate_objects(shape.node)
              if p in pyshacl.constraints.ALL_CONSTRAINT_PARAMETERS):
        match c:
            # Cardinal constraints
            case pyshacl.constraints.MinCountConstraintComponent():
                min_count = int(term_to_datalog(c.min_count))
                if min_count == 0:
                    continue
                datalog += f"min_count_constr({name}, {min_count}).\n"
            case pyshacl.constraints.MaxCountConstraintComponent():
                max_count = int(term_to_datalog(c.max_count))
                datalog += f"max_count_constr({name}, {max_count}).\n"

            # Logical constraints
            case pyshacl.constraints.NotConstraintComponent():
                for not_c in c.not_list:
                    datalog += f"not_constr({name}, {term_to_datalog(not_c)}).\n"
            case pyshacl.constraints.AndConstraintComponent():
                datalog += f"and_constr({name}).\n"
                for and_c in c.and_list:
                    datalog += f"and_shape({name}, {term_to_datalog(and_c)}).\n"
            case pyshacl.constraints.OrConstraintComponent():
                datalog += f"or_constr({name}).\n"
                for or_c in c.or_list:
                    datalog += f"or_shape({name}, {term_to_datalog(or_c)}.\n"
            case pyshacl.constraints.XoneConstraintComponent():
                datalog += f"xone_constr({name}).\n"
                for xone_c in c.xone_nodes:
                    datalog += f"xone_shape({name}, {term_to_datalog(xone_c)}).\n"

            # Property pair constraints
            case pyshacl.constraints.EqualsConstraintComponent():
                for pred in c.property_compare_set:
                    datalog += f"equals_constr({name}, {term_to_datalog(pred)}).\n"
            case pyshacl.constraints.DisjointConstraintComponent():
                for pred in c.property_compare_set:
                    datalog += f"disjoint_constr({name}, {term_to_datalog(pred)}).\n"
            case pyshacl.constraints.LessThanConstraintComponent():
                for pred in c.property_compare_set:
                    datalog += f"less_than_constr({name}, {term_to_datalog(pred)}.\n"
            case pyshacl.constraints.LessThanOrEqualsConstraintComponent():
                for pred in c.property_compare_set:
                    datalog += f"less_than_or_eq_constr({name}, {term_to_datalog(pred)}.\n"

            # Shape-based constraints
            case pyshacl.constraints.PropertyConstraintComponent():
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
                    datalog += "{" + shape_datalog + "}"
                    datalog += "property_constr(name, other_name).\n"
            case pyshacl.constraints.NodeConstraintComponent():
                for shape_node in c.node_shapes:
                    other_shape = shape.get_other_shape(shape_node)
                    if namespace:
                        (other_name, _), namespace = name_one_shape(other_shape, namespace)
                    else:
                        other_name = "shape"
                    shape_datalog, namespace = shape_to_datalog(other_name, other_shape, namespace)
                    datalog += shape_datalog
                    datalog += f"node_constr({name}, {other_name}).\n"
            case pyshacl.constraints.QualifiedValueShapeConstraintComponent():
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
            case pyshacl.constraints.MinLengthConstraintComponent():
                # yes, this is the best way to access the length constraints for these
                datalog += f"min_length_constr({name}, {term_to_datalog(c.string_rules[0])}).\n"
            case pyshacl.constraints.MaxLengthConstraintComponent():
                datalog += f"max_length_constr({name}, {term_to_datalog(c.string_rules[0])}).\n"
            case pyshacl.constraints.PatternConstraintComponent():
                datalog += f"pattern_constr({name}, {term_to_datalog(c.string_rules[0])}).\n"
            case pyshacl.constraints.LanguageInConstraintComponent():
                for language in c.string_rules:
                    datalog += f"constr_language_tag({name}, {term_to_datalog(language)}).\n"
                datalog += f"language_in_constr({name}).\n"
            case pyshacl.constraints.UniqueLangConstraintComponent():
                datalog += f"unique_lang_constr({name}).\n"

            # Value constraints
            case pyshacl.constraints.ClassConstraintComponent():
                for class_rule in c.class_rules:
                    datalog += f"class_constr({name}, {term_to_datalog(class_rule)}).\n"
            case pyshacl.constraints.DatatypeConstraintComponent():
                datalog += f"datatype_constr({name}, {term_to_datalog(c.datatype_rule)}).\n"
            case pyshacl.constraints.NodeKindConstraintComponent():
                datalog += f"node_kind_constr({name}, {term_to_datalog(c.nodekind_rule)}).\n"

            # Value range constraints
            case pyshacl.constraints.MinExclusiveConstraintComponent():
                for min_val in c.min_vals:
                    # TODO: might need to handle types more explicitly here; LOTS are accepted
                    datalog += f"min_exclusive_constr({name}, {term_to_datalog(min_val)}).\n"
            case pyshacl.constraints.MinInclusiveConstraintComponent():
                for min_val in c.min_vals:
                    datalog += f"min_inclusive_constr({name}, {term_to_datalog(min_val)}).\n"
            case pyshacl.constraints.MaxExclusiveConstraintComponent():
                for max_val in c.max_vals:
                    datalog += f"max_exclusive_constr({name}, {term_to_datalog(max_val)}).\n"
            case pyshacl.constraints.MaxInclusiveConstraintComponent():
                for max_val in c.max_vals:
                    datalog += f"max_inclusive_constr({name}, {term_to_datalog(max_val)}).\n"

            # Other constraints

            case _:
                pass # for testing
                # raise NotImplementedError("Constraint not implemented:", c)

    return datalog, namespace
