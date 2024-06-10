import java.util.*;
public class GCD {
  public static int gcd(int a, int b) {
    if (b == 0) {
      return a;
    } else {
      return gcd(b, a % b); // corrected line
    }
  }
}
/* The given faulty code had the recursive call to the gcd function with incorrect parameters. In the original code, the parameters were \texttt{gcd(a \% b, b)}, which does not correctly follow the Euclidean algorithm for finding the greatest common divisor (GCD). The Euclidean algorithm states that the GCD of two numbers also divides their difference. Therefore, to correctly implement this, when \texttt{b} is not zero, we should recursively call \texttt{gcd} with \texttt{b} and \texttt{a \% b} as its parameters, effectively reducing the problem size in each step until \texttt{b} becomes zero, at which point \texttt{a} is the GCD. The corrected line is \texttt{return gcd(b, a \% b);}, which ensures the function correctly follows the Euclidean algorithm by swapping the roles of \texttt{a} and \texttt{b} in each recursive call, and making the second parameter the remainder of \texttt{a} divided by \texttt{b}, as required. This change addresses the issue and ensures the function works as intended for all test cases.
 */