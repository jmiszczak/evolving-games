import random as rnd

import networkx as nx

#rnd.seed(19680801)

# uniform choice of a node from the graph
def get_rand_node(g: nx.Graph) -> object:
    return rnd.choice(list(g.nodes))


# uniform selection of a node excluding give list
def get_rand_node_excluding(g: nx.Graph, l: [object]) -> object:
    choice_nodes = list(g.nodes)
    [choice_nodes.remove(x) for x in l]
    return rnd.choice(choice_nodes)


# append random edge
def append_rand_edge(g: nx.Graph, depth: int = 0) -> object:
    rn1 = get_rand_node(g)
    exclude_nodes = [rn1]
    exclude_nodes.extend(g.neighbors(rn1))
    rn2: object = get_rand_node_excluding(g, exclude_nodes)
    g.add_edge(rn1, rn2)
    if depth == 0:
        return g
    else:
        return append_rand_edge(g, depth - 1)


def main():
    dim1, dim2 = 10, 10
    add_edges = 200
    print("Running with", dim1, "x", dim2, "grid.")
    init_graph = nx.grid_2d_graph(dim1, dim2)
    print("Average shortest path length at begining:", nx.average_shortest_path_length(init_graph))
    out_graph = append_rand_edge(init_graph, add_edges)
    print("Average shortest path length after adding",
          add_edges, "edges:", nx.average_shortest_path_length(out_graph))


if __name__ == "__main__":
    main()
