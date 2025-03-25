from typing import Iterable

import pyshacl

from .shape_to_datalog import shape_to_datalog
from .name import name


class DatalogShapesGraph:
    """ Wrapper around a pySHACL ShapeGraph. """

    def __init__(self, graph: pyshacl.ShapesGraph) -> None:
        self._shapes, self.namespace = name(graph)

    @property
    def shapes(self) -> Iterable[tuple[str, pyshacl.shape.Shape]]:
        return self._shapes

    def to_datalog(self) -> str:
        """ Return Datalog text expressing self._graph """

        # import library file (even though path will likely be edited by end user)
        datalog: str = ".include \"shacl.dl\""

        for shape in self.shapes:
            new_datalog, self.namespace = shape_to_datalog(*shape, namespace=self.namespace)
            datalog += new_datalog

        return datalog
