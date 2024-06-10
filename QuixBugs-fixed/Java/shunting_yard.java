import java.util.*;
public class SHUNTING_YARD {
    public static List<Object> shunting_yard(ArrayList<Object> tokens) {
        Map<String, Integer> precedence = new HashMap<>();
        precedence.put("+", 1);
        precedence.put("-", 1);
        precedence.put("*", 2);
        precedence.put("/", 2);
        ArrayList<Object> rpntokens = new ArrayList<>();
        ArrayDeque<String> opstack = new ArrayDeque<>();
        for (Object token : tokens) {
            if (token instanceof Integer) {
                rpntokens.add(token);
            } else {
                String operator = (String) token;
                while (!opstack.isEmpty() &&
                       precedence.get(operator) <= precedence.get(opstack.peek())) {
                    rpntokens.add(opstack.pop());
                }
                opstack.push(operator);
            }
        }
        while (!opstack.isEmpty()) {
            rpntokens.add(opstack.pop());
        }
        return rpntokens;
    }
}
/* The main issue with the original code was that it failed to push operators onto the operator stack (\textit{opstack}) after comparing their precedence. This omission led to operators not being included in the Reverse Polish Notation (RPN) output. To fix this, after the precedence comparison and popping of higher or equal precedence operators, the current operator is now pushed onto the stack (\texttt{opstack.push(operator);}). This ensures that all operators are correctly considered and placed in the output list (\textit{rpntokens}) according to the rules of RPN. Furthermore, I modified the method and list declarations to use \texttt{List<Object>} and \texttt{ArrayList<Object>} to avoid raw type warnings and ensure type safety. Additionally, \texttt{getLast()} method was changed to \texttt{peek()} to correctly peek at the top of the stack without removing the item, which is the intended operation for checking the last operator's precedence.
 */