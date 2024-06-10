import java.util.*;
public class FIND_FIRST_IN_SORTED {
  public static int find_first_in_sorted(int[] arr, int x) {
    int lo = 0;
    int hi = arr.length - 1; // corrected to ensure hi is within bounds
    while (lo < hi) { // changed from <= to < to prevent infinite loop
      int mid = lo + (hi - lo) / 2; // changed to prevent potential overflow
      if (x == arr[mid] && (mid == 0 || x > arr[mid - 1])) {
        return mid;
      } else if (x <= arr[mid]) {
        hi = mid; // corrected to ensure narrowing of search range
      } else {
        lo = mid + 1;
      }
    }
    // Additional check to handle the case where lo equals hi
    return arr[lo] == x ? lo : -1;
  }
}
/* The original code had two primary issues leading to incorrect functionality and infinite loops. First, the initialization of \texttt{hi} as \texttt{arr.length} instead of \texttt{arr.length - 1} was incorrect because array indices in Java are zero-based. This mistake could lead to \texttt{ArrayIndexOutOfBoundsException}. Second, the condition in the \texttt{while} loop was adjusted from \texttt{lo <= hi} to \texttt{lo < hi}, preventing an infinite loop when \texttt{lo} and \texttt{hi} converge but are not yet equal. Additionally, to address potential integer overflow, the calculation of \texttt{mid} was modified to use \texttt{lo + (hi - lo) / 2} instead of directly averaging \texttt{lo} and \texttt{hi}. Lastly, a final check was added after the loop to determine if the element at \texttt{arr[lo]} is equal to \texttt{x}, returning \texttt{lo} if true, and \texttt{-1} otherwise. This ensures that the method correctly identifies when \texttt{x} is not present in the array, addressing the failed test cases.
 */