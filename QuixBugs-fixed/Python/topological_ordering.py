def topological_ordering(nodes):
    ordered_nodes = [node for node in nodes if not node.incoming_nodes]
    for node in ordered_nodes:
        for nextnode in node.outgoing_nodes:
            if (
                all(x in ordered_nodes for x in nextnode.incoming_nodes)
                and nextnode not in ordered_nodes
            ):
                ordered_nodes.append(nextnode)
    return ordered_nodes
'''
\text{In the original code, the condition }\texttt{set(ordered_nodes).issuperset(nextnode.outgoing_nodes)}\text{ was incorrect. This condition was checking if all outgoing nodes of the nextnode were in the ordered_nodes list, but we need to check if all incoming nodes of the nextnode are in the ordered_nodes list. Therefore, we changed the condition to }\texttt{all(x in ordered_nodes for x in nextnode.incoming_nodes)}\text{. This way, we make sure that all nodes that current node points to are already in the ordered_nodes list before adding the nextnode to it.}

'''