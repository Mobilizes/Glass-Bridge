import pandas as pd
import random

df = pd.DataFrame({"id": [], "ac": []})

for i in range(100):
    r = random.uniform(0, 1)
    ans = "l" if r < 0.5 else "r"

    df.loc[len(df)] = [i, ans]
    with open(f"data/secret/{i+1}.in", "w") as f:
        f.write(f"{i}")
    with open(f"data/secret/{i+1}.ans", "w") as f:
        f.write(f"{ans}")

df.to_csv("steps.csv", index=False)
