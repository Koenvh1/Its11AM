start_hours = 490_885 # 1 January 2026


tzs = {}

for line in open("expression.csv").read().split("\n"):
    if not line:
        continue
    t, tz = line.split("\t", 1)
    tz = tz.replace("_", " ")
    tzs[int(t)] = tz

def do(lo, hi):
    """Build a binary search expression tree covering [lo, hi] inclusive."""
    if lo == hi:
        return f"&quot;{tzs[lo]}&quot;"
    
    mid = (lo + hi) // 2
    left  = do(lo, mid)
    right = do(mid + 1, hi)
    return f"([HOURS_SINCE_EPOCH] &lt;= {mid} ? {left} : {right})"

expression = do(490885, 621956)
expression = f"<Parameter expression=\"{expression}\" />"
open("expression_tree.txt", "w").write(expression)