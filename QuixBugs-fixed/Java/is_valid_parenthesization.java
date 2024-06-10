import java.util.*;
public class IS_VALID_PARENTHESIZATION {
  public static Boolean is_valid_parenthesization(String parens) {
    int depth = 0;
    for (int i = 0; i < parens.length(); i++) {
      Character paren = parens.charAt(i);
      if (paren.equals('(')) {
        depth++;
      } else {
        depth--;
        if (depth < 0) {
          return false;
        }
      }
    }
    // Fixed by checking if depth is not zero after the loop
    return depth == 0;
  }
}
/* The issue with the original code was that it only checked for cases where there were too many closing parentheses but did not verify if there were unmatched opening parentheses left at the end of the input string. By tracking the \textit{depth} variable, it was observed that if there are unmatched opening parentheses, the depth will not return to 0 by the end of the iteration. Thus, by adding a final check to ensure \textit{depth} equals 0 after processing all characters in the input, it guarantees that all parentheses are properly nested and matched. This resolves the failure in cases where the input had unmatched opening parentheses.
 */