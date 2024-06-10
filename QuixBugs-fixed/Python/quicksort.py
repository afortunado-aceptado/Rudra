def quicksort(arr):
    if not arr:
        return []
    pivot = arr[0]
    lesser = quicksort([x for x in arr[1:] if x <= pivot]) # corrected line
    greater = quicksort([x for x in arr[1:] if x > pivot])
    return lesser + [pivot] + greater
'''
The original code failed to sort arrays correctly when they included duplicate elements. By tracking the pivot's behavior, it became evident that elements equal to the pivot were not being handled properly—they were being discarded instead of being placed alongside the pivot. Thus, the change was to include elements equal to the pivot (\texttt{x <= pivot}) in the \texttt{lesser} list. This minor adjustment ensures that the algorithm can handle duplicates correctly, leading to the expected sorted output. The rest of the algorithm remains unchanged, as it follows the QuickSort principle of dividing the array into lesser, equal, and greater elements relative to a chosen pivot.

'''