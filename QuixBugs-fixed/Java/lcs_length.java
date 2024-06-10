import java.util.*;
public class LCS_LENGTH {
    public static Integer lcs_length(String s, String t) {
        int[][] dp = new int[s.length()+1][t.length()+1];
        int max = 0;
        for (int i = 1; i <= s.length(); i++) {
            for (int j = 1; j <= t.length(); j++) {
                if (s.charAt(i-1) == t.charAt(j-1)) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                    max = Math.max(max, dp[i][j]);
                }
            }
        }
        return max;
    }
}
/* The original code attempted to use a complex structure with nested Maps, which made it difficult to track and update the lengths of common substrings correctly. By changing the data structure to a 2D array, the code becomes much simpler and more efficient. The 2D array \(dp\) now directly stores the length of the longest common substring ending at \(s[i-1]\) and \(t[j-1]\). The condition checks if the current characters of \(s\) and \(t\) match, and if so, it updates \(dp[i][j]\) based on the value of \(dp[i-1][j-1]\) plus one, indicating an extension of a common substring. The \(max\) variable keeps track of the maximum length encountered so far, which is then returned as the result. This approach addresses the deficiencies of the original code by ensuring accurate and efficient computation of the longest common substring length.
 */