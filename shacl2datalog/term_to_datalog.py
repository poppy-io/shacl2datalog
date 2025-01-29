import rdflib

from decimal import Decimal
from datetime import date, datetime, time, timedelta


def term_to_datalog(term: rdflib.Node) -> str:
    """

    @param term:
    @return:
    """
    match term:
        case rdflib.Literal():
            match term.value:
                # booleans
                case bool():
                    return str(term.value).lower()

                # numeric types
                case float() | int() | rdflib.compat.long_type() | Decimal():
                    return str(term.value)

                # timey types
                case datetime() | date() | time():
                    # FIXME(?) production of decidedly evil underscore iso format
                    return term.value.isoformat().replace("-", "_")
                # FIXME: date duration to iso function access? github:rdflib/rdflib/xsd_datetime.py
                # case rdflib.xsd_dateDuration() | timedelta():

                # everything else is considered stringy
                case _:
                    return f"\"{term.value}\""

        case rdflib.BNode():
            return f"blank_node{term}"
        case rdflib.URIRef():
            return f"\"{term}\""

        case _:
            raise TypeError("term passed to term_to_datalog is not a Literal, BNode, or URIRef!"
                            + str(term))
