I want you to build  a Streamlit app, app.py, that explores the correlations in real health data in nhanes_health.csv and make sure to the read the CSV first. The app must include a data preview: a short description of the dataset and a table of rows, Pairwise view: two dropdowns pick X and Y. The app shows a scatter plot, the correlation r, and the number of participants n. The scatter plot has a trend line or binned means, and an option to color points by a health threshold such as SBP ≥ 130.  Correlation heatmap. The user picks which numeric variables to include. Every square shows its coefficient, and the color scale is fixed from −1 to 1. Filters. Sidebar controls for sex and an age range that update every view: the table, scatter plot, r, n and heatmap. Correlation method. A toggle between Pearson and Spearman that applies to both the pairwise view and the heatmap.

Time to debug. This is how it looks and the text needs to be a different color


There is little text at the top that is being covered by a black bar. Do you know what this is?

what about choosing the correlation methods. Sometime either picking Pearson or Spearman it doesn't show amnything in the pairwise relationships

![alt text](image.png) I keep getting the same result for each combination with using Spearman. Please help fix this to display the plots