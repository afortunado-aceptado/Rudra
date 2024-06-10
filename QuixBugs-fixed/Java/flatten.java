import java.util.*;

public class FLATTEN {
    public static ArrayList<Object> flatten(Object arr) {
        // Check if the input is an instance of ArrayList
        if (arr instanceof ArrayList) {
            ArrayList<Object> narr = (ArrayList<Object>)arr;
            ArrayList<Object> result = new ArrayList<>(50);
            for (Object x : narr) {
                if (x instanceof ArrayList) {
                    // Recursively flatten the ArrayList and add all its elements to the result list
                    result.addAll(flatten(x));
                } else {
                    // Add non-ArrayList elements directly to the result list
                    result.add(x);
                }
            }
            return result;
        } else {
            // Create a new ArrayList to hold the non-ArrayList element
            ArrayList<Object> singleItemList = new ArrayList<>();
            singleItemList.add(arr);
            return singleItemList;
        }
    }
}
/* The original code had two main issues. Firstly, it incorrectly attempted to recursively flatten any object, even non-ArrayLists, which led to infinite recursion for non-ArrayList objects. This was evident in the second buggy line where `flatten(arr)` was called without a base case for non-ArrayList objects. The solution was to remove the recursive call for non-ArrayList objects and instead return a new ArrayList containing the non-ArrayList object itself. Secondly, the original code added the result of `flatten(x)` directly to the result list without checking if `x` was an ArrayList or not. This was fixed by properly adding all elements from the recursively flattened ArrayList to the result list using `addAll()`. Tracking these critical parameter values, such as recognizing when `arr` is not an ArrayList and hence should not be treated with recursive flattening, guided the revisions. Additionally, ensuring that the result list correctly accumulates all elements, including nested lists, by using `addAll()` for ArrayList objects, was essential for the repair. These corrections ensure that the code now correctly flattens a nested list structure into a single list, as required.
 */