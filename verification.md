# Verification

Reference pandas calculations use **Pearson** and ages **20-80**. Rows 4-6 filter by sex only. Counts include participants with both selected measurements present. The exercise's ages 40-59 example uses a different filter.

Run the pandas calculations yourself as the exercise requires, then record the values you observe in the app and complete the Match column. The pairwise view rounds r to 3 decimal places; the heatmap rounds r to 2.



| # | Check | App shows | pandas gives | Match? |
|---|---|---|---|---|
| 1 | r for `age` vs `systolic_bp`, all participants |r = 0.463 | r = 0.462695061; n = 4,433 | yes |
| 2 | r for `bmi` vs `waist_cm`, all participants |0.903 | r = 0.902588776; n = 4,433 | yes |
| 3 | r for `waist_cm` vs `hdl_chol`, all participants |r = -0.335 | r = -0.334986876; n = 4,433 | yes |
| 4 | r and n for `age` vs `systolic_bp`, **Female only** |r = 0.555 n = 2,263 | r = 0.555342554; n = 2,263 | yes |
| 5 | r and n for `age` vs `systolic_bp`, **Male only** |r = 0.351 n = 2170 | r = 0.350697865; n = 2,170 | yes |
| 6 | With the filter set to Female, does the heatmap's `age`/`systolic_bp` square match row 4? |heat maps round r to 0.56 | r = 0.555342554; n = 2,263 (heatmap rounds r to 0.56) | yes  |
