
"""
Test suite for DynamicSSSP algorithms goes here.
We will add a variety of comprehensive test cases 
for edge weight incrementation and decrementation algorithms
"""

from Algorithms.DynamicSSSP import DynamicSSSP
from logger_config import end_logging, setup_logging
import logging

setup_logging(logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Starting tests for DynamicSSSP")

def print_test_results_incrementation(graph, src, dst, new_weight, sink='T'):

    sssp = DynamicSSSP(graph, sink)

    print("\n-----BEFORE INCREMENT------")
    sssp.print_graph()
    sssp.print_state()

    old_weight = graph[src][dst]
    
    print(f"\n*** Incrementing edge {src} -> {dst} from {old_weight} to {new_weight}***\n")

    affected = sssp.increment_edge(src, dst, new_weight)

    print("\nAffected vertices:", sorted(affected))

    print("\nAFTER INCREMENT")
    sssp.print_state()
    sssp.print_graph()
    print("------------------------------------------------\n")

def print_test_results_decrementation(graph, src, dst, new_weight, sink='T'):

    sssp = DynamicSSSP(graph, sink)

    print("\n-----BEFORE DECREMENT------")
    sssp.print_graph()
    sssp.print_state()

    old_weight = graph[src][dst]
    print(f"\n*** Decrementing edge {src} -> {dst} from {old_weight} to {new_weight}***\n")


    affected = sssp.decrement_edge(src, dst, new_weight)

    print("\nAffected vertices:", sorted(affected))

    print("\nAFTER DECREMENT")
    sssp.print_state()
    sssp.print_graph()
    print("------------------------------------------------\n")


print("Dynamic SSSP Edge weight increment tests")
print("----------------------------------------------------\n")

graph1 = {
    "A": {"B": 2, "C": 5, "T": 10},
    "B": {"T": 3},
    "C": {"T": 2},
    "T": {},
}

graph2 = {
    "A" :{"C":1},
    "B" : {"D":2},
    "C" : {"E":3},
    "D" : {"C":2, "F":2},
    "E" : {"T":2},
    "F" : {"T":4}
}

graph3 = {
    "A" :{"B":4, "D":1},
    "B" : {"C":1},
    "C" : {"T":1},
    "D" : {"T":4},
    "E" : {"D":6, "A":2}
}


logger.info(f"\ntest 1 : Incrementing an edge that will remain as a part of a shortest path")
print_test_results_incrementation(graph1, "A", "B", 4, sink='T')

logger.info("test 2: Incrementing an edge that will no longer be a part of a shortest path")
print_test_results_incrementation(graph1, "A", "B", 10, sink='T')

logger.info("test 3: Incrementing an edge that leaves all shortest paths unaffected")
print_test_results_incrementation(graph1, "A", "B", 12, sink='T')

logger.info("test 4: Incrementing an edge that changes shortest distances but SP(G) structure unaffected")
print_test_results_incrementation(graph2, "C", "E", 5, sink='T')

logger.info("test 5: Decrementing an edge that alters the shortest path of ancestors of source")
print_test_results_decrementation(graph2, "C", "E", 1, sink='T')

logger.info("test 6: Decrementing an edge so that it becomes a shortest path edge")
print_test_results_decrementation(graph3, "A", "B", 2, sink='T')

logger.info("test 7: Decrementing an edge so that it changes the shortest path of other branch")
print_test_results_decrementation(graph2, "C", "E", 1, sink='T')

logger.info("test 8: decrementing an edge")
print_test_results_decrementation(graph2, "C", "E", 1, sink='T')


logger.info("Tests for DynamicSSSP ended")
end_logging()




