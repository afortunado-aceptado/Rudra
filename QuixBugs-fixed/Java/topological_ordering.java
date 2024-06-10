import java.util.*;

public class TOPOLOGICAL_ORDERING {
    public static ArrayList<Node> topological_ordering(List<Node> directedGraph) {
        ArrayList<Node> orderedNodes = new ArrayList<Node>();
        for (Node node : directedGraph) {
            if (node.getPredecessors().isEmpty()) {
                orderedNodes.add(node);
            }
        }

        int index = 0;
        while (index < orderedNodes.size()) {
            Node node = orderedNodes.get(index);
            for (Node nextNode : node.getSuccessors()) {
                if (orderedNodes.containsAll(nextNode.getPredecessors()) &&
                        !orderedNodes.contains(nextNode)) {
                    orderedNodes.add(nextNode);
                }
            }
            index++;
        }

        return orderedNodes;
    }
}
/* Tracking the key parameter values such as predecessors and successors of nodes helped in identifying the issue in the original code. By checking if all predecessors of the next node are in the ordered list before adding the next node, we ensure that the topological ordering is correct.
``` */