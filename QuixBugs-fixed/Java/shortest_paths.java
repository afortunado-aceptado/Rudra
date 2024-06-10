import java.util.*;

public class SHORTEST_PATHS {
  final static int INF = 99999;
  public static Map<String, Integer> shortest_paths(String source, Map<List<String>, Integer> weight_by_edge) {
    Map<String, Integer> weight_by_node = new HashMap<String, Integer>();
    for (List<String> edge : weight_by_edge.keySet()) {
      weight_by_node.put(edge.get(1), INF);
      weight_by_node.put(edge.get(0), INF);
    }
    weight_by_node.put(source, 0);
    for (int i = 0; i < weight_by_node.size(); i++) {
      for (List<String> edge : weight_by_edge.keySet()) {
        int newWeight = weight_by_node.get(edge.get(0)) + weight_by_edge.get(edge);
        if (weight_by_node.get(edge.get(1)) < newWeight) {
          newWeight = weight_by_node.get(edge.get(1));
        }
        weight_by_node.put(edge.get(1), newWeight);
      }
    }
    return weight_by_node;
  }
}
/* The original code contained several fundamental issues which needed addressing to correctly implement the Bellman-Ford algorithm. 
Firstly, the algorithm was incorrectly updating the weights of edges instead of the weights of the nodes. This mistake was corrected by directly updating the minimum distances in the \texttt{weight\_by\_node} map, rather than attempting to update the \texttt{weight\_by\_edge} map, which should remain constant. 
Secondly, the original code attempted to modify and use a \texttt{Map<List<String>, Integer>} directly for edge processing, which is cumbersome and error-prone due to the complexity of using list structures as keys in a map. Instead, the repaired code maintains the input structure but simplifies the processing logic by focusing on node updates. By tracking these critical values – specifically, the minimum path weights from the source node – and ensuring the algorithm correctly updates these weights over each iteration, the repaired code now functions according to the problem description and passes all test cases.
 */