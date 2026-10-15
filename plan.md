# Approved Plan: Health Correlation Explorer

Build one Streamlit app, `app.py`, that explores relationships between health measures in `nhanes_health.csv`.

## Data

- Read the CSV before building the app. It contains 4,433 adult participants, 11 columns, and no missing values in the supplied file.
- Use these 10 numeric variables: `age`, `bmi`, `waist_cm`, `systolic_bp`, `diastolic_bp`, `hba1c`, `total_chol`, `hdl_chol`, `sleep_hours`, and `sedentary_minutes`.
- Exclude `sex` from all correlations; use it only as a filter.
- Load the CSV from beside `app.py` so the app works regardless of the terminal's working directory.

## Build order

1. **Load the data and add filters.** Create sidebar controls for sex and an inclusive age range. Apply both controls to one filtered dataframe that feeds every view.
2. **Add the data preview.** Describe the NHANES dataset briefly and display the filtered participant rows in a table. Show the filtered participant count.
3. **Add the pairwise view.** Provide X and Y dropdowns containing every numeric variable. Display a scatter plot, a fitted trend line, the correlation coefficient, and the number of complete participant pairs. Allow optional coloring by a health threshold, such as systolic blood pressure at or above 130 mmHg.
4. **Add the correlation heatmap.** Let users select numeric variables. Label each cell with its coefficient and pairwise participant count. Keep the color scale fixed from -1 to 1, centered at zero.
5. **Add the correlation method control.** A sidebar choice between Pearson and Spearman applies to both the pairwise view and the heatmap.

## Rules for the numbers

- Calculate every correlation and participant count from the filtered data.
- For each X/Y pair, exclude only participants missing X or Y. Compute both the coefficient and `n` from those same complete pairs.
- Use the same pairwise handling of missing values for each heatmap cell; do not discard a participant merely because a different variable is missing.
- Show `n` beside the pairwise coefficient and within every heatmap cell.
- If fewer than two complete observations remain, or either variable has no variation, show that the correlation is undefined rather than reporting a misleading number.
- Allow a variable to be selected for both X and Y. Its correlation with itself is 1 when there are enough observations and the variable varies.
- Changing threshold colors does not change the pairwise correlation or participant count.

## Interpretation and presentation

- Explain that these correlations describe the sample rather than the U.S. population because NHANES oversamples some groups and this app does not apply survey weights.
- Remind users that a correlation near zero does not rule out a nonlinear relationship, such as a U-shaped pattern.
- Use readable labels, units, and sufficient text contrast.

## Implementation notes from debugging

The app uses Python, Streamlit, pandas, NumPy, and Matplotlib. Matplotlib draws the scatter plot and heatmap after the Seaborn dependency was removed during debugging. Spearman is calculated as Pearson correlation between average ranks of the complete pairs, avoiding an optional SciPy dependency.

## Run the app

From the `Module 9 Part 2` folder:

```bash
uv run --with streamlit,pandas,numpy,matplotlib streamlit run app.py
```

## Verification

Compare the app's values with independent pandas calculations using the checks in the exercise and record the results in `verification.md`. Confirm that sex and age filters update the table, scatter plot, coefficient, participant count, and heatmap, and that both methods work for all numeric selections.
