def shortest_paths(source, weight_by_edge):
    # Initialize all nodes with infinity and set distance for source to 0
    nodes = set([u for u, v in weight_by_edge.keys()] + [v for u, v in weight_by_edge.keys()])
    weight_by_node = {node: float('inf') for node in nodes}
    weight_by_node[source] = 0

    # Relax edges repeatedly
    for i in range(len(nodes) - 1):
        for (u, v), weight in weight_by_edge.items():
            if weight_by_node[u] + weight < weight_by_node[v]:
                weight_by_node[v] = weight_by_node[u] + weight

    return weight_by_node
'''
The original code had a significant issue in the initialization of \texttt{weight\_by\_node} which only considered destination nodes, potentially omitting the source and other nodes not appearing as a destination in any edge. To fix this, all unique nodes are identified by combining sources and destinations from the \texttt{weight\_by\_edge} keys, ensuring all nodes are included. Additionally, the faulty line attempting to update \texttt{weight\_by\_edge} inside the loop was corrected to update \texttt{weight\_by\_node} based on the Bellman-Ford algorithm's core logic, which relaxes edges by updating the stored weights if a shorter path is found. This corrected approach ensures that the function correctly computes the minimum path weights from the source to all nodes in the graph.

'''