def find_in_sorted(arr, x):
    def binsearch(start, end):
        if start >= end:
            return -1
        mid = start + (end - start) // 2
        if x < arr[mid]:
            return binsearch(start, mid)
        elif x > arr[mid]:
            return binsearch(mid+1, end) # corrected line
        else:
            return mid
    return binsearch(0, len(arr))
'''
The issue with the original code was that it entered an infinite loop when the searched value \(x\) was greater than the middle element of the array but not present in the array. This happened because the binary search function \(binsearch\) was called with the same \(mid\) value as the starting point for the next search range, effectively not moving forward or discarding any part of the array. The solution was to call \(binsearch(mid+1, end)\) when \(x > arr[mid]\), ensuring that the search range is narrowed down correctly by moving past the current middle element. This change prevents the infinite loop by ensuring that each recursive call to \(binsearch\) either decreases the size of the search range or terminates the search.

'''