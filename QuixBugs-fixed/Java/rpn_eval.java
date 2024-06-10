import java.util.*;
import java.util.function.BinaryOperator;

public class RPN_EVAL {
    public static Double rpn_eval(ArrayList<Object> tokens) { // Corrected generic type
        Map<String, BinaryOperator<Double>> op = new HashMap<>();
        op.put("+", (a, b) -> a + b);
        op.put("-", (a, b) -> a - b);
        op.put("*", (a, b) -> a * b);
        op.put("/", (a, b) -> a / b);
        Stack<Double> stack = new Stack<>(); // Corrected generic type
        for (Object token : tokens) {
            if (token instanceof Double) {
                stack.push((Double) token);
            } else {
                token = (String) token;
                Double b = stack.pop(); // Corrected order of operands
                Double a = stack.pop();
                Double c;
                BinaryOperator<Double> bin_op = op.get(token);
                c = bin_op.apply(a, b);
                stack.push(c);
            }
        }
        return stack.pop();
    }
}
/* The main issue with the original code was related to generic types and operand order. First, the \texttt{ArrayList} parameter lacked a generic type, leading to potential type safety issues. I corrected this by specifying \texttt{ArrayList<Object>} to accommodate both \texttt{Double} and \texttt{String} types. Second, the \texttt{Stack} instantiation did not specify a generic type, which I fixed by declaring it as \texttt{Stack<Double>} to ensure it only contains \texttt{Double} values. The most critical logical error was the order of operands popped from the stack for binary operations. In Reverse Polish Notation, the second operand popped is actually the first operand for the operation (\texttt{a}), and the first operand popped is the second operand for the operation (\texttt{b}). This mistake altered the intended mathematical operations, leading to incorrect calculations. Correcting the order in which operands are popped from the stack and applied to the operations fixed the incorrect output. Tracking the flow of operands and ensuring they're used in the correct order was key to resolving the issue.
 */