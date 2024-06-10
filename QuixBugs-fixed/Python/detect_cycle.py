class Node:
    def __init__(self, val=0, successor=None):
        self.val = val
        self.successor = successor

def detect_cycle(node):
    if not node or not node.successor:
        return False
    hare = tortoise = node
    while hare and hare.successor:
        tortoise = tortoise.successor
        hare = hare.successor.successor
        if hare == tortoise:
            return True
    return False
'''
The original code had issues with accessing the successor of a None type in the hare movement logic. By checking if the hare or the hare's successor is None before moving the hare two steps forward, we avoid these issues. This ensures that we do not try to access an attribute of a None type, which would raise an AttributeError. Additionally, we added a check at the beginning to immediately return False if the input node is None or its successor is None, which handles empty or single-node linked lists. Tracking the hare and tortoise positions through each iteration, if they ever meet, it confirms a cycle exists; otherwise, if the hare reaches the end of the list (None), the list is acyclic.

'''