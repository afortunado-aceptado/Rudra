import java.util.*;
public class LIS {
    public static int lis(int[] arr) {
        Map<Integer, Integer> ends = new HashMap<Integer, Integer>(100);
        int longest = 0;
        int i = 0;
        for (int val : arr) {
            ArrayList<Integer> prefix_lengths = new ArrayList<Integer>(100);
            for (int j = 1; j < longest + 1; j++) {
                if (arr[ends.get(j)] < val) {
                    prefix_lengths.add(j);
                }
            }
            int length =
                    !prefix_lengths.isEmpty() ? Collections.max(prefix_lengths) : 0;
            // Fixed condition to correctly update the ends map only when necessary
            // Removed the second part of the buggy condition as it was unnecessary and incorrect
            ends.put(length + 1, i);
            if (length + 1 > longest) { // Correctly update the longest variable
                longest = length + 1;
            }
            i++;
        }
        return longest;
    }
}
/* The original code had a buggy condition that incorrectly determined when to update the "ends" map and the "longest" variable. The condition was supposed to ensure that we only update the ends map if we found a longer subsequence or if the current value was smaller than the last value of the current longest subsequence. However, the second part of this condition was not only unnecessary (since the ints in arr are unique and the logic for choosing the longest subsequence was already correctly handled) but also incorrectly implemented, leading to faulty behavior. By removing the second part of the condition and always updating the "ends" map, but only updating the "longest" variable when we actually find a longer subsequence, the code now correctly calculates the length of the longest increasing subsequence. Tracking the "length" variable and understanding its role in determining the "longest" subsequence was key to identifying and fixing the faulty logic.
 */