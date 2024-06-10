import java.util.*;
public
class KHEAPSORT {
public
  static ArrayList<Integer> kheapsort(ArrayList<Integer> arr, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<Integer>();
    // Fix to the loop - start adding to the heap not from the beginning but from k elements ahead if possible
    for (int i = 0; i < Math.min(k + 1, arr.size()); i++) {
      heap.add(arr.get(i));
    }
    ArrayList<Integer> output = new ArrayList<Integer>();
    // Start iterating from k+1 to include elements correctly and avoid re-adding the first k elements
    for (int i = k + 1; i < arr.size(); i++) {
      heap.add(arr.get(i));
      Integer popped = heap.poll();
      output.add(popped);
    }
    // Drain the rest of the heap after all elements have been added
    while (!heap.isEmpty()) {
      output.add(heap.poll());
    }
    return output;
  }
}
/* The faulty code did not correctly initialize the heap with the first \(k+1\) elements, leading to incorrect sorting as it started re-adding elements from the beginning of the array. By adjusting the loop to add the first \(k+1\) elements to the heap and then iterating from \(k+1\) onwards, the heap correctly represents a window of the \(k+1\) closest elements to their sorted positions at any time. This adjustment ensures that the minimum element within the acceptable displacement (k) is always at the top of the heap, ready to be polled and added to the sorted output. Tracking the heap's contents and the output list's growth throughout the iterations helped identify the misalignment in the initial code's logic.
 */