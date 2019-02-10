## CSV REPORT PROCESSING SCRIPT

This python script will process your reports.
Input format: UTF-8 or UTF-16 CSV file (with any kind of line endings), with columns: date(MM/DD/YYYY), state name, number of impressions and CTR percentage.

example input:

01/21/2019,Mandiana,883,0.38%  
01/21/2019,Lola,76,0.78%  
01/21/2019,Fāryāb,919,0.67%  
01/22/2019,Lola,201,0.82%  
01/22/2019,Beroun,139,0.61%  
01/22/2019,Mandiana,1050,0.93%  
01/23/2019, 🐱 ,777,0.22%  
01/23/2019,Gaoual,72,0.7%  
01/23/2019,Lola,521,0.19%  
01/24/2019,Beroun,620,0.1%  
01/24/2019,Unknown,586,0.86%  
01/24/2019, 🐱 ,1082,0.68%  

example output:  

2019-01-21,AFG,919,6  
2019-01-21,GIN,959,4  
2019-01-22,CZE,139,1  
2019-01-22,GIN,1251,12  
2019-01-23,GIN,593,2  
2019-01-23,XXX,777,2  
2019-01-24,CZE,620,1  
2019-01-24,XXX,1668,12  

### GETTING STARTED

1. Checking Python version.
    - To be able to use this script you'll need to have Python installed, you can check whether you have it installed or not by typing in terminal:  
`python3 --version`  
or:  
`python --version`  
    - This script was written using version 3.7.0 and it is advised to use the same version, but script should work with 3.6 version as well.  
    -If you don't have Python installed you can go to [Python.org](https://www.python.org/downloads/) to download it.

1. Creating Virtual Environment  
    - To create a virtual environment, decide upon a directory where you want to place it, and run the venv module as a script with the directory path:  
    `python3 -m venv tutorial-env`  
    - Once you’ve created a virtual environment, you may activate it.  
    `source tutorial-env/bin/activate`  
2. Download  
    - You need to clone repository to your local destination  
    `$ cd path/to/your/workspace`  
    `git clone https://github.com/henryy07/csv_report_processing.git`
    - if you have established ssh connection to github you can use this link to clone repo:  
    `git clone git@github.com:henryy07/csv_report_processing.git`  
3. Requirements
    - Once your virtual environment is activated and project is cloned you need to install requirements:  
    `$ pip install -r requirements.txt`  

### USAGE


- File requirements:
    - file type: csv files only
    - accepted encoding type: 'UTF-8', 'UTF-16'
    - csv file fields need to be comma separated and have no quoting 
    - input format: UTF-8 or UTF-16 CSV file (with any kind of line endings), with columns: date
(MM/DD/YYYY), state name, number of impressions and CTR percentage

- Using this script is very simple you need to just type this command:  
`python main.py -f path/of/file/to/process -nf path/of/new/file`  
or optionally:  
`python main.py --file_path path/of/file/to/process --new_file_path path/of/new/file` 

- Script should process your csv report and write new file with the destination you chose(if it exists)
- Output format: UTF-8 CSV file with Unix line endings, with columns: date (YYYY-MM-DD),
three letter country code (or XXX for unknown states), number of impressions, number of
clicks (rounded, assuming the CTR is exact). Rows are sorted lexicographically by date
followed by the country code.
- Technologies used:
    - Python 3.7.0
        - Pandas
        - Pycountry
        - Chardet   



