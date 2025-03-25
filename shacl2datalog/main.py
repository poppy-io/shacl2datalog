"""Script allowing CLI usage of the library."""

import sys
import cProfile
import pstats
import glob, os

from .datalog_shape_graph import DatalogShapesGraph
from .read import read

def main(*args, **kwargs) -> int:
    """Read a given SHACL file from a given path or URl and output equivalent Datalog rules
    to a given filepath."""

    # hardcode a graph for testing until uv2nix behaves
    # graph = read(args[0])
    
    #graph = read("datalog_library/personexample.ttl")
    #datalog = DatalogShapesGraph(graph).to_datalog()

    # with open(args[1], 'w') as file:
    #with open("datalog_library/out.dl", 'w') as file:
    #    file.write(datalog)

    folder_path = "./shacl_tests"
    for test in glob.glob(os.path.join(folder_path, "**/*.ttl"), recursive=True):
        print(f"Transpiling file: {test}")
        graph = read(test)
        datalog = DatalogShapesGraph(graph).to_datalog()
        with open(os.path.join("./out", os.path.relpath(test, start=folder_path)), 'w') as out:
            out.write(datalog)

def profile() :
    with cProfile.Profile() as pr:
        main()
        st = pstats.Stats(pr)
        st.strip_dirs()
        st.sort_stats(pstats.SortKey.CUMULATIVE)
        st.print_stats(10)

