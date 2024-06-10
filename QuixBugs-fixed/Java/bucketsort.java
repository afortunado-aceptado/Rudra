import java.util.*;
public class BUCKETSORT {
  public static ArrayList<Integer> bucketsort(ArrayList<Integer> arr, int k) {
    ArrayList<Integer> counts = new ArrayList<Integer>(Collections.nCopies(k, 0));
    for (Integer x : arr) {
      counts.set(x, counts.get(x) + 1);
    }
    ArrayList<Integer> sorted_arr = new ArrayList<Integer>(); // Fixed
    for (int i = 0; i < counts.size(); i++) { // Fixed
      sorted_arr.addAll(Collections.nCopies(counts.get(i), i)); // Fixed
    }
    return sorted_arr;
  }
}
/* The original code had several issues:
1. The initial capacity of the sorted\_arr ArrayList was arbitrarily set to 100, which is unnecessary and could lead to incorrect results if the actual sorted array size is different. This was fixed by removing the initial capacity, allowing the ArrayList to dynamically adjust its size.
2. The loop that is supposed to add the elements to the sorted\_arr was iterating over the original array (arr) instead of the counts array, which stores the frequency of each element. This was fixed by iterating over the counts array to correctly populate the sorted array based on the frequencies.
3. The parameters in the addAll method call inside the loop were incorrect. It was adding elements based on the original element values (count) rather than their frequencies (counts.get(i)) and the corresponding index i, which represents the actual value to be added. This was fixed by correctly using counts.get(i) for the number of copies and i as the element to add.

By tracking the values in the counts array and ensuring that we iterate over it to construct the sorted\_arr, we ensure that each element is added to the sorted array the correct number of times based on its frequency, thus producing a correctly sorted array.
 */