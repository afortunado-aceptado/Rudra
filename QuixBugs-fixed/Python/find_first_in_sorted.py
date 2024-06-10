def find_first_in_sorted(arr, x):
    lo = 0
    hi = len(arr) - 1  # Adjusted to point to the last index
    while lo < hi:  # Changed to loop until lo is not less than hi
        mid = (lo + hi) // 2
        if x > arr[mid]:
            lo = mid + 1
        else:
            hi = mid
    if arr[lo] == x:
        return lo
    return -1
'''
The original code had two primary issues. The first was in the condition of the while loop (while lo <= hi), which allowed it to enter an infinite loop in certain cases. Changing it to (while lo < hi) ensures the loop progresses towards convergence by narrowing the search space until the low and high pointers meet or cross. Secondly, the high pointer was initially set to len(arr), which is out of bounds for the array. Adjusting it to len(arr) - 1 ensures it points to the last valid index. The adjustment in the if-else logic inside the loop ensures that if x is greater than the value at mid, the search space is narrowed to the right half; otherwise, it narrows down to the left half including mid. This approach guarantees finding the lowest index of x by moving the high pointer to mid when x is less than or equal to arr[mid], thereby ensuring that if x exists in arr, lo will eventually point to its first occurrence.

'''