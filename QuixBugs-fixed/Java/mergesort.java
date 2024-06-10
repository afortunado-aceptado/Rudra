import java.util.*;
public class MERGESORT {
    public static ArrayList<Integer> merge(ArrayList<Integer> left, ArrayList<Integer> right) {
        ArrayList<Integer> result = new ArrayList<Integer>(); // Corrected initialization
        int i = 0;
        int j = 0;
        while (i < left.size() && j < right.size()) {
            if (left.get(i) <= right.get(j)) {
                result.add(left.get(i++));
            } else {
                result.add(right.get(j++));
            }
        }
        while (i < left.size()) {
            result.add(left.get(i++));
        }
        while (j < right.size()) {
            result.add(right.get(j++));
        }
        return result;
    }

    public static ArrayList<Integer> mergesort(ArrayList<Integer> arr) {
        if (arr.size() < 2) { // Corrected condition to trigger recursion properly
            return arr;
        } else {
            int middle = arr.size() / 2;
            ArrayList<Integer> left = new ArrayList<Integer>(arr.subList(0, middle));
            ArrayList<Integer> right = new ArrayList<Integer>(arr.subList(middle, arr.size()));
            left = mergesort(left);
            right = mergesort(right);
            return merge(left, right);
        }
    }
}
/* The initial code had several issues, including improper base case handling in the mergesort function and inefficiency in the merge function due to the unnecessary initial capacity setting and missing logic to append remaining elements from both left and right sublists. By correcting the base case to return the array when its size is less than 2, we ensure that the recursion properly divides the array until it cannot be divided further. Additionally, fixing the merge function to dynamically grow the result list and adding loops to append remaining elements from both sublists after the main merging loop ensure that all elements are included in the final sorted list. Tracking the size of sublists and ensuring that elements from both are completely merged was key to resolving the issues.
 */