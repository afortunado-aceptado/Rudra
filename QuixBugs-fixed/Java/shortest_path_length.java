import java.util.*;

public class SHORTEST_PATH_LENGTH {

    public static int shortest_path_length(Map<List<Node>, Integer> length_by_edge,
                                           Node startnode, Node goalnode) {
        // Initialize all nodes distance to infinity except start node
        Map<Node, Integer> distances = new HashMap<>();
        Set<Node> visitedNodes = new HashSet<>();
        PriorityQueue<NodeDistancePair> priorityQueue = new PriorityQueue<>(Comparator.comparingInt(NodeDistancePair::getDistance));

        distances.put(startnode, 0);
        priorityQueue.add(new NodeDistancePair(startnode, 0));

        while (!priorityQueue.isEmpty()) {
            NodeDistancePair currentPair = priorityQueue.poll();
            Node currentNode = currentPair.getNode();
            
            if (visitedNodes.contains(currentNode)) continue;
            visitedNodes.add(currentNode);

            if (currentNode.equals(goalnode)) {
                return distances.get(currentNode);
            }

            for (Node neighbor : currentNode.getSuccessors()) {
                if (visitedNodes.contains(neighbor)) continue;
                List<Node> edge = Arrays.asList(currentNode, neighbor);
                
                if (!length_by_edge.containsKey(edge)) continue; // Ensure the edge exists

                int newDist = distances.get(currentNode) + length_by_edge.get(edge);
                if (newDist < distances.getOrDefault(neighbor, Integer.MAX_VALUE)) {
                    distances.put(neighbor, newDist);
                    priorityQueue.add(new NodeDistancePair(neighbor, newDist));
                }
            }
        }
        return Integer.MAX_VALUE;
    }

    static class NodeDistancePair {
        private Node node;
        private int distance;

        public NodeDistancePair(Node node, int distance) {
            this.node = node;
            this.distance = distance;
        }

        public Node getNode() {
            return node;
        }

        public int getDistance() {
            return distance;
        }
    }
}
/* The critical issue in the original code was the handling of distances and the way edges were looked up in the map. The original implementation did not correctly update the distances based on the lengths of the edges, leading to incorrect shortest path calculations. Furthermore, comparing nodes directly using \texttt{getValue()} might not always work if \texttt{Node} overrides \texttt{equals()} and \texttt{hashCode()}. The corrected version uses a \texttt{PriorityQueue} to efficiently select the next node to visit based on the shortest distance discovered so far, ensuring that the algorithm follows Dijkstra's approach more closely. By mapping each node to its current shortest distance and updating these distances based on the edges' lengths, the algorithm correctly finds the shortest path. The addition of a \texttt{NodeDistancePair} class helps in managing the priority queue's entries. This approach more accurately reflects the priority of nodes based on their current shortest distances, which is crucial for Dijkstra's algorithm to function properly.
 */