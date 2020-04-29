import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from networkx.algorithms import approximation
from networkx.algorithms import shortest_paths
import sys


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    # we follow the original idea, creating a dominating set and building a tree from that
    min_dom_set = nx.algorithms.approximation.min_weighted_dominating_set(G)
    return_set = set([]) # we create a set of nodes that we want to be in the final tree
    source = min_dom_set.pop()
    # we connect all the nodes in the dominating set by finding all the nodes in the shortest paths
    for node in min_dom_set:
        # use dijkstra shortest paths to create the new tree
        curr_path = nx.algorithms.shortest_paths.dijkstra_path(G, source, node)
        for node1 in curr_path:
            return_set.add(node1)
    # we recreate the subgraph with the necessary nodes to keep it connected
    min_dom_subgraph = G.subgraph(list(return_set))
    # resulting graph will have extra unnecessary edges, use MST to prune
    min_dom_tree = nx.minimum_spanning_tree(min_dom_subgraph)
    return min_dom_tree

    """
    #MST baseline
    min_tree = nx.minimum_spanning_tree(G)
    return min_tree
    """

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    # graph_name = path.split(".")[0] --> doesn't work
    G = read_input_file(path)
    T = solve(G)
    assert is_valid_network(G, T)
    print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
    # need to change to be dynamic for file name
    write_output_file(T, f"outputs/test.out")




# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')
