import pandas as pd
df = pd.read_csv("nhanes_health.csv")
f = df[(df["sex"] == "Female") & df["age"].between(40, 59)]
f["age"].corr(f["systolic_bp"]), len(f)