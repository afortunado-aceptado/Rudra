import java.util.*;
public class QUICKSORT {
  public static ArrayList<Integer> quicksort(ArrayList<Integer> arr) {
    if (arr.isEmpty()) {
      return new ArrayList<Integer>();
    }
    Integer pivot = arr.get(0);
    ArrayList<Integer> lesser = new ArrayList<Integer>();
    ArrayList<Integer> greater = new ArrayList<Integer>();
    for (Integer x : arr.subList(1, arr.size())) {
      if (x < pivot) {
        lesser.add(x);
      } else { // Removed condition to include pivot duplicates in the greater list
        greater.add(x);
      }
    }
    ArrayList<Integer> sortedList = new ArrayList<Integer>();
    lesser = quicksort(lesser);
    greater = quicksort(greater);
    sortedList.addAll(lesser); // Added directly to sortedList
    sortedList.add(pivot);
    sortedList.addAll(greater);
    return sortedList;
  }
}
/* Tracking the values of parameters through the failed case revealed that the original code did not handle duplicates of the pivot correctly, leading to an unsorted array. By removing the condition that explicitly checked if \(x > pivot\) for adding to the greater list, duplicates of the pivot are now correctly handled. Additionally, the original code incorrectly merged the lists, which was fixed by creating a new sortedList and correctly merging lesser, pivot, and greater. This approach ensures that all elements, including duplicates of the pivot, are accounted for and properly sorted.
 */