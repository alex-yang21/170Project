import networkx as nx
from parse import *
from utils import is_valid_network, average_pairwise_distance, deg_heuristic
from networkx.algorithms import approximation
from networkx.algorithms import shortest_paths
import sys
import os


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # central = get_central(G)
    # if len(central) > 0:
    #     return central


    n = G.number_of_nodes()
    for j in range(0, n):
        f1 = deg_heuristic(G, j)
        G.add_node(j, weight=f1)

    # print(G[0][1]['weight'])

    # we follow the original idea, creating a dominating set and building a tree from that
    min_dom_set = nx.algorithms.approximation.min_weighted_dominating_set(G, "weight")
    # print(min_dom_set)
    # print(min_dom_set)
    lists = []
    # return_set = set([]) # we create a set of nodes that we want to be in the final tree
    leest = list(min_dom_set)
    source = min_dom_set.pop()


    # we connect all the nodes in the dominating set by finding all the nodes in the shortest paths
    # for node in min_dom_set:
    #     # use dijkstra shortest paths to create the new tree
    #     curr_path = nx.algorithms.shortest_paths.dijkstra_path(G, source, node)
    #     for node1 in curr_path:
    #         return_set.add(node1)
    for a in leest:
        return_set = set([])
        for b in leest:

        # use dijkstra shortest paths to create the new tree
            curr_path = nx.algorithms.shortest_paths.dijkstra_path(G, a, b)
            for node1 in curr_path:
                return_set.add(node1)
        lists.append(return_set)

    # checks if nodes were added to return set, if none there is a central node and return single node
    # print(len(return_set))
    if not lists:
        r = nx.Graph()
        r.add_node(source)
        return r


    min_tree = source
    min = 10000000
    for c in lists:
        min_dom_subgraph = G.subgraph(list(c))
        min_dom_tree = nx.minimum_spanning_tree(min_dom_subgraph)
        pair = average_pairwise_distance(min_dom_tree)
        if pair < min:
            min = pair
            min_tree = min_dom_tree


    # we recreate the subgraph with the necessary nodes to keep it connected
    # min_dom_subgraph = G.subgraph(list(return_set))
    # resulting graph will have extra unnecessary edges, use MST to prune
    # min_dom_tree = nx.minimum_spanning_tree(min_dom_subgraph)

    return min_tree

    """
    #MST baseline
    min_tree = nx.minimum_spanning_tree(G)
    return min_tree
    """

#
if __name__ == "__main__":
    output_dir = "outputs"
    input_dir = "inputs"
    for input_path in os.listdir(input_dir):
        graph_name = input_path.split(".")[0]
        G = read_input_file(f"{input_dir}/{input_path}")
        T = solve(G)
        print(graph_name)
        write_output_file(T, f"{output_dir}/{graph_name}.out")


# """
# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     # graph_name = path.split(".")[0] --> doesn't work
#     G = read_input_file("inputs/" +path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     # need to change to be dynamic for file name
#     write_output_file(T, f"myoutputs/test.out")
# """




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
