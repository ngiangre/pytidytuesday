import requests
import duckdb
import requests

def list_github_repo_files(repo: str) -> list:
  if not isinstance(repo, str):
    raise TypeError("repo must be a string in the format 'owner/repo/path/to/directory'")

  url = f"https://api.github.com/repos/{repo}"
  response = requests.get(url)

  if response.status_code != 200:
    raise ValueError(f"GitHub API request failed with status code {response.status_code}: {response.text}")

  files = response.json()
  
    # Ensure the API response is a list (directory contents), not a dict (like a single file or repo metadata)
  if not isinstance(files, list):
    raise ValueError("The provided repo path does not point to a directory or is invalid.")

  # Safely extract file names
  file_names = []
  for file in files:
    if 'name' in file:
      file_names.append(file['name'])

  return file_names

def inject_files_into_duckdb(file_urls: list, db_path: str = ":memory:") -> duckdb.DuckDBPyConnection:
    """
    Loads multiple CSV files directly into DuckDB, one table per file.

    Args:
        file_urls (list): List of URLs pointing to CSV files.
        db_path (str): Path to the DuckDB database file. Defaults to in-memory.

    Returns:
        duckdb.DuckDBPyConnection: Connection to the DuckDB database with the tables loaded.
    """

    if not isinstance(file_urls, list):
        raise TypeError("file_urls must be a list of URLs.")
    
    conn = duckdb.connect(database=db_path)

    for file_url in file_urls:
        if not isinstance(file_url, str):
            print(f"Skipping invalid URL (not a string): {file_url}")
            continue

        table_name = file_url.split("/")[-1].split(".")[0]
        table_name = table_name.replace("-", "_").replace(" ", "_")

        try:
            # DuckDB can read HTTP/HTTPS CSV files directly!
            conn.execute(f"""
                CREATE OR REPLACE TABLE {table_name} AS 
                SELECT * FROM read_csv_auto('{file_url}')
            """)
            print(f"Loaded {file_url} into table '{table_name}'")
        except Exception as e:
            print(f"Error loading {file_url} into DuckDB: {e}")
            continue

    return conn
