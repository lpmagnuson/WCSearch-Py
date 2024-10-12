# WCSearch-Py

This script returns the number of holdings for OCLC numbers for a given group (consortia), state, and total holdings. 

## Requirements

Python3  
WSKey for the WorldCat Search API v2

## Usage

After cloning the repository, copy sample_config.yml to config.yml and edit:

Add WSKey and Secret  
Change [group symbol](https://help.oclc.org/Resource_Sharing/WorldShare_Interlibrary_Loan/Policies_Directory_guide/080OCLC_profiled_groups) and state (per ISO 3166-2) to desired values.

The script expects OCLC numbers to be found in a CSV utf-8 file called "oclc_test.csv" in a column with OCLC as the header. The input file can have any other columns; the holdings information will be appended in added columns in the output file. The CSV file must be in the same directory as this repository.

Run the script:
```
python3 oclc-counts.py
```

Output will be stored in a file called output-oclc-holdings.csv.

## License

[MIT](https://choosealicense.com/licenses/mit/)
