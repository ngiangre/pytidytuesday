from plotnine import *
import functions as f

repo = "rfordatascience/tidytuesday/contents/data/2025/2025-04-22/"
files = f.list_github_repo_files(repo)

file_urls = ['https://raw.githubusercontent.com/' + repo.replace('contents/', 'main/') + f for f in files if f.endswith('.csv')]

conn = f.inject_files_into_duckdb(file_urls)  

# Execute query to get fatalities data by quarter AND year with statistics for confidence intervals
query = """
    SELECT
        SUBSTR(CAST(date AS STRING), 1, 4) AS year,
        AVG(fatalities_count) AS avg_fatalities,
        AVG(fatalities_count) - 1.96 * STDDEV(fatalities_count) / SQRT(COUNT(*)) AS ci_lower,
        AVG(fatalities_count) + 1.96 * STDDEV(fatalities_count) / SQRT(COUNT(*)) AS ci_upper,
        COUNT(*) as count,
        STDDEV(fatalities_count) as stddev
    FROM daily_accidents
    GROUP BY year
    ORDER BY year
"""

quarterly_df = conn.execute(query).fetchdf()

plot = (
    ggplot(quarterly_df, aes(x='year', y='avg_fatalities',group=1)) +
    geom_errorbar(aes(ymin='ci_lower', ymax='ci_upper'), width=0.2, alpha=0.7) +
    geom_line(size=1) +
    geom_point(size=3) +
    labs(
        title="Distribution of Annual Fatalities",
        x="Year",
        y="Average Fatalities With 95% Confidence Intervals",
        caption="Source: TidyTuesday dataset"
    ) +
    theme_minimal() +
    theme(
        plot_title=element_text(size=14),
        axis_title=element_text(size=12),
        axis_text_x=element_text(angle=45,vjust=1,hjust=1)
    )
)
plot.save(
  filename = "results/fatalities_time_series.pdf", 
  width = 12,
  height = 6,
  dpi = 300,
  verbose = False
)

# Close connection
conn.close()
