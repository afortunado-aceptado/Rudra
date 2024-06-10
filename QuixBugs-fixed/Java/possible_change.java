import java.util.*;
public class POSSIBLE_CHANGE {
    public static int possible_change(int[] coins, int total) {
        int[] dp = new int[total + 1];
        dp[0] = 1;
        for (int coin : coins) {
            for (int i = coin; i <= total; i++) {
                dp[i] += dp[i - coin];
            }
        }
        return dp[total];
    }
}
/* The original code attempted to solve the problem recursively without memoization, leading to incorrect recursion logic and excessive computations for larger inputs. By introducing dynamic programming (DP), we can efficiently calculate the number of ways to make change for any given total. The DP array dp[] is initialized with dp[0]=1 since there is only one way to make a sum of 0 (by choosing no coins). For each coin, we iterate through the array and update dp[i] by adding the value of dp[i-coin]. This represents the number of ways to make change for the amount i using the current coin. This solution efficiently computes the correct number of combinations by building up from smaller to larger amounts, ensuring all test cases pass with minimal computational overhead.
 */