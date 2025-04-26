# pytidytuesday

A repository for exploring and performing python analyses based on `https://github.com/rfordatascience/tidytuesday`.

# Structure

This repository uses uv to set up the project environment for python (pyproject.toml, uv.lock, and .python-version) and the *.Rproj file sets the project working directory (I am using Rstudio as my IDE on Posit Cloud).

Each script in *scripts/* analyzes one or a collection of datasets for a tidytuesday week period. Any figures. or outputs created go into the *results* folder and is prefixed by the name of the script from which it came from.

# Usage

`uv run scripts/fatal-car-crashes.py`




