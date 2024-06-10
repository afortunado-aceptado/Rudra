import java.util.*;

public class REVERSE_LINKED_LIST {
    public static Node reverse_linked_list(Node node) {
        Node prevnode = null;
        Node nextnode;
        while (node != null) {
            nextnode = node.getSuccessor();
            node.setSuccessor(prevnode);
            prevnode = node;
            node = nextnode;
        }
        return prevnode;
    }
}
/* The original code had two critical issues. Firstly, it failed to update the \texttt{prevnode} within the loop, which is crucial for reversing the linked list. By adding \texttt{prevnode = node;} inside the loop, each node is correctly set to point to its predecessor. Secondly, returning \texttt{prevnode} instead of the original faulty return statement is correct because, after the loop completes, \texttt{prevnode} points to the new head of the reversed list (the original tail of the list), which aligns with the function's goal. Tracking these adjustments, particularly the update of \texttt{prevnode} within each iteration, ensures that the reversal logic is correctly implemented, leading to the successful reversal of the linked list.
 */