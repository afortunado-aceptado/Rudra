import java.util.*;
public class KTH {
    public static Integer kth(ArrayList<Integer> arr, int k) {
        int pivot = arr.get(0);
        ArrayList<Integer> below = new ArrayList<Integer>();
        ArrayList<Integer> above = new ArrayList<Integer>();
        ArrayList<Integer> equal = new ArrayList<Integer>();
        for (Integer x : arr) {
            if (x < pivot) {
                below.add(x);
            } else if (x > pivot) {
                above.add(x);
            } else {
                equal.add(x);
            }
        }
        int num_less = below.size();
        int num_eq = equal.size();
        if (k < num_less) {
            return kth(below, k);
        } else if (k >= num_less && k < num_less + num_eq) {
            return pivot;
        } else {
            return kth(above, k - num_less - num_eq);
        }
    }
    public static void main(String[] args) {
        ArrayList<Integer> arr = new ArrayList<>(Arrays.asList(45, 2, 6, 8, 42, 90, 322));
        System.out.println(kth(arr, 6));
    }
}
/* The original code failed to handle two critical aspects: 
1. Elements equal to the pivot were not correctly managed. This omission could misplace the pivot in the final ordering, causing incorrect outputs. 
2. When recursively calling the function for the "above" list, the index \(k\) was not adjusted to account for the elements less than and equal to the pivot. 

To address these issues, an "equal" list was introduced to manage elements equal to the pivot. This adjustment allows the function to handle duplicates correctly and maintain the logic of the quickselect algorithm. Furthermore, when the recursive call is made for the "above" list, \(k\) is now properly adjusted by subtracting the sizes of the "below" and "equal" lists. This adjustment ensures that \(k\) references the correct position within the reduced list, aligning the algorithm with the quickselect's expected behavior.
 */