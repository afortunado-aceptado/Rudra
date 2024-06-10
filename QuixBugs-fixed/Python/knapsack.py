def knapsack(capacity, items):
    from collections import defaultdict
    memo = defaultdict(int)
    for i in range(1, len(items) + 1):
        weight, value = items[i - 1]
        for j in range(capacity, 0, -1):
            if weight <= j:
                memo[j] = max(memo[j], value + memo[j - weight])
    return memo[capacity]
'''
The original code attempted to use a 2D memoization approach which was unnecessary and led to a misunderstanding of how to properly update the memoization table. Specifically, the buggy line "if weight < j" used a wrong condition and iterated in the wrong direction, not properly considering items that exactly fit the remaining capacity. By changing the iteration of "j" to go from "capacity" down to 1 (reversed), we ensure that each item is considered exactly once per capacity value, simulating the effect of adding each item to the knapsack. This prevents inadvertently considering an item more than once for a given subcapacity. The condition was changed to "if weight <= j" to include items that exactly fit the remaining capacity. Additionally, the memoization structure was simplified from a 2D to a 1D dictionary, which is sufficient for this problem. This corrected the logic flaw and ensured that all given test cases would pass, aligning with the problem's requirements.

'''