import java.util.*;
public class DETECT_CYCLE {
    public static boolean detect_cycle(Node node) {
        if (node == null) return false;
        
        Node hare = node;
        Node tortoise = node;
        
        while (hare != null && hare.getSuccessor() != null) {
            tortoise = tortoise.getSuccessor();
            hare = hare.getSuccessor().getSuccessor();
            if (hare == tortoise)
                return true;
        }
        return false;
    }
}
/* The original code had several issues. First, the import statement for Node was incorrect because Node is not a library class but rather a user-defined class, so we need to define the Node class within the same code or in another file correctly within the project. Secondly, the check "if (hare.getSuccessor() == null)" was insufficient because it should also consider the case when "hare" itself is null. To address this, I modified the while condition to "while (hare != null && hare.getSuccessor() != null)" to ensure we don't encounter a NullPointerException by trying to access the successor of a null object. This approach ensures that the code checks for both the existence of the "hare" node and its successor before proceeding to move the "hare" two steps ahead. The rest of the code was logically sound for detecting a cycle based on the tortoise and hare algorithm, where the hare (fast pointer) moves two steps at a time and the tortoise (slow pointer) moves one step. If there is a cycle, they are guaranteed to meet. Tracking the hare and tortoise's positions is crucial for detecting a cycle, and correcting the loop's conditions ensures the code functions as expected without throwing exceptions.*/