def possible_change(coins, total, index=0, memo=None):
    if total == 0:
        return 1
    if total < 0 or index == len(coins):
        return 0
    if memo is None:
        memo = {}
    key = (total, index)
    if key in memo:
        return memo[key]
    # Include the coin
    include = possible_change(coins, total - coins[index], index, memo)
    # Exclude the coin
    exclude = possible_change(coins, total, index + 1, memo)
    memo[key] = include + exclude
    return memo[key]
'''
The original code failed because it didn't correctly handle the case when we should not include the current coin in the sum, and also it lacked memoization which is crucial for reducing the computational complexity for larger inputs. By introducing an "index" parameter, we can recursively check both including and excluding the current coin without altering the original list of coins. This approach also allows us to add memoization to the function, which significantly improves performance by caching results of sub-problems (identified uniquely by the current "total" and the "index" of the coin being considered) and avoiding redundant calculations. This fixes the code and ensures it passes all the given test cases.

'''