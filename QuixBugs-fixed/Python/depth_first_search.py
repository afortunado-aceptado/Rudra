class Node:
    def __init__(self, value, successors=None):
        self.value = value
        self.successors = successors if successors else []

def depth_first_search(startnode, goalnode):
    nodesvisited = set()
    def search_from(node):
        if node in nodesvisited:
            return False
        nodesvisited.add(node)
        if node == goalnode:
            return True
        else:
            return any(search_from(nextnode) for nextnode in node.successors)
    return search_from(startnode)
'''
The issue with the original code was the lack of adding the currently visited node to the nodesvisited set before proceeding with the recursive search on its successors. This omission could lead to an infinite loop in case of cyclic graphs or simply repetitive visits to the same node, which decreases efficiency. By tracking whether we correctly mark each visited node (by adding the currently visited node to nodesvisited right after checking if it has been visited), we ensure that each node is visited only once. This modification prevents infinite loops and unnecessary re-visits, making the code function correctly according to the problem description. The provided class Node definition is also necessary to create instances for testing the function as per the example given.

'''