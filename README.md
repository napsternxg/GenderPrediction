# GenderPrediction
Experiments with predicting gender using US SSN data

## Get most confident names
```
import pandas as pd
df = pd.read_csv("ALL_STATENAMES.txt", header=None)
df.columns = ["State", "Gender", "Year", "Name", "Count"]
df_genders = df.pivot_table(values="Count", index="Name", columns="Gender", aggfunc=sum)
df_genders = df_genders.fillna(0)
df_genders["total"] = (df_genders["F"] + df_genders["M"]).astype("float")
df_genders["prop_M"] = df_genders["M"] / df_genders["total"]
df_genders[(df_genders.prop_M > 0.95) | (df_genders.prop_M < 0.05)].to_csv("confident_names.txt", sep="\t",index=False)
```
