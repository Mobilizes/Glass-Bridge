import pandas as pd
import random

random.seed()

df = pd.DataFrame({"id": [], "ac": []})

print("{", end='')
for i in range(150):
    r = random.uniform(0, 1)
    ans = "l" if r < 0.5 else "r"
    print(ans, end=", " if i < 149 else "")

    df.loc[len(df)] = [i, ans]
    with open(f"problem/data/secret/{i+1}.in", "w") as f:
        f.write(f"{i}")
    with open(f"problem/data/secret/{i+1}.ans", "w") as f:
        f.write(f"{ans}")
print("}")

df.to_csv("steps.csv", index=False)

df = pd.read_csv("steps.csv")
print("{", end='')
for i, row in df.iterrows():
    print(f"'{row["ac"]}'", end=", " if i < 149 else "")
print("}")
