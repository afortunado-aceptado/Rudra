def minDistance(a, b):
    if abs(len(a) - len(b)) >= 1: return 100
    dp = [[0 for _ in range(len(b) + 1)] for j in range(len(a) + 1)]
    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + 1)
    return dp[-1][-1]

def gauge_localizer(ans, res) -> tuple: #TP, FP, FN, Jaccard coefficient, Hit@5
    if len(ans) == 0:
        return 1, 0, 0
    label = [False] * len(ans)
    
    tp, fp = 0, 0
    for l in res:
        flag = 0
        for i, gt in enumerate(ans):
            if label[i]: continue
            l, gt = l.replace(" ", "").strip(), gt.replace(" ", "").strip()
            if l == gt or (minDistance(l, gt) <= 1):
                tp += 1; flag = 1; 
                label[i] = True
                break
        fp += (flag == 0)
    
    fn = max(0, min(5, sum([len(gt) > 3 for gt in ans])) - sum(label))
    #Jc = sum(label) / (fn + len(res)) # (A*B) / (A|B)
    return tp, fp, fn