import java.util.*;
public class MINIMUM_SPANNING_TREE {
    public static Set<WeightedEdge> minimum_spanning_tree(List<WeightedEdge> weightedEdges) {
        Map<Node, Set<Node>> groupByNode = new HashMap<>();
        Set<WeightedEdge> minSpanningTree = new HashSet<>();
        Collections.sort(weightedEdges);
        for (WeightedEdge edge : weightedEdges) {
            Node vertex_u = edge.node1;
            Node vertex_v = edge.node2;
            if (!groupByNode.containsKey(vertex_u)) {
                groupByNode.put(vertex_u, new HashSet<>(Arrays.asList(vertex_u)));
            }
            if (!groupByNode.containsKey(vertex_v)) {
                groupByNode.put(vertex_v, new HashSet<>(Arrays.asList(vertex_v)));
            }
            if (!isSameGroup(groupByNode, vertex_u, vertex_v)) {
                minSpanningTree.add(edge);
                union(groupByNode, vertex_u, vertex_v);
            }
        }
        return minSpanningTree;
    }

    private static boolean isSameGroup(Map<Node, Set<Node>> groupByNode, Node vertex_u, Node vertex_v) {
        return groupByNode.get(vertex_u).equals(groupByNode.get(vertex_v));
    }

    private static void union(Map<Node, Set<Node>> groupByNode, Node vertex_u, Node vertex_v) {
        Set<Node> vertex_u_group = new HashSet<>(groupByNode.get(vertex_u));
        Set<Node> vertex_v_group = new HashSet<>(groupByNode.get(vertex_v));
        vertex_u_group.addAll(vertex_v_group);
        for (Node node : vertex_u_group) {
            groupByNode.put(node, vertex_u_group);
        }
    }
}
/* The primary issue was with the update method, which failed to correctly merge groups of nodes (or sets) and update all relevant entries in the groupByNode map. The original code attempted to update groups but did not properly merge the sets or update all affected nodes' group mappings, leading to incorrect behavior when checking if two nodes are in the same group. By introducing the union method, which correctly merges the sets of nodes and updates the map for all nodes in the merged set, this issue is resolved. Furthermore, the isSameGroup method was introduced to cleanly check if two nodes belong to the same group, improving readability and correctness. This approach ensures that whenever an edge is added to the minimum spanning tree, all nodes in the connected components of the two vertices of the edge are correctly identified as being in the same group, thereby preventing cycles and ensuring the algorithm correctly implements Kruskal's algorithm.
 */