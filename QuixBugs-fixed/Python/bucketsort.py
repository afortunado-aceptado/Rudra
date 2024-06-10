def bucketsort(arr, k):
    counts = [0] * k
    for x in arr:
        counts[x] += 1
    sorted_arr = []
    for i, count in enumerate(counts):  # Corrected line
        sorted_arr.extend([i] * count)
    return sorted_arr
'''
The issue in the original code was with the enumeration in the loop used to recreate the sorted array. Originally, it incorrectly enumerated over \texttt{arr} instead of \texttt{counts}, which led to the program simply repeating the input array instead of constructing the sorted array. By tracking the \texttt{counts} list—which properly tallies the occurrences of each integer—during debugging, it became clear that this list should be the one enumerated over to correctly build the sorted array. Each index \texttt{i} in \texttt{counts} represents a value from the original array, and the value at that index represents how many times \texttt{i} appears, allowing the corrected loop to extend the \texttt{sorted\_arr} list with \texttt{i} repeated \texttt{count} times, thus repairing the code.

'''