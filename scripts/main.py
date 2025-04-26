def main():
    import pandas as pd

    # Load the Stata file
    data = pd.read_stata('farsp2009.dta')
    
    # View the first few rows to verify it loaded correctly
    print(data.head())


if __name__ == "__main__":
    main()
