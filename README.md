# imdb top 20 movie scraper

## How to install project from terminal:

1. Clone the repository
```
git clone https://github.com/horimre/imdb.git
```
2. Go to the project folder
```
cd imdb
```
3. Create a virtual environment (venv) with the following command:
```
python -m venv .venv
```
Once the command is finished, your virtual environment is ready.
 
4. Activate the virtual environment:
```
source .venv/bin/activate
```
Once activated you will see the name of the environment within the terminal
```console
(.venv) (base) horimre@Imre-MBP imdb % 
```
  
5. Install requirements:
  ```
  pip install -r requirements.txt
  ```
  
## How to execute the script from terminal and check the output file:

Inside the virtual environment execute the following commands:
1. Run script:
```
python imdb.py
```
The script produces an output file called "imdb_top_20.csv".

You can open it from the project folder, or print out its content inside the terminal.

2. Clear the terminal screen:
```
clear
```
3. Print out the content of the output file:
```
cat imdb_top_20.csv
```
4. You can also check the file with Quick Look with the following command:
```
qlmanage -p imdb_top_20.csv 2>/dev/null
```
Close quick look with yor mouse or Ctrl+C

## How to execute unit tests from terminal and check coverage report:
Inside the virtual environment execute the following commands:
1. Run unittests
```
pytest
```
2. Check code coverage:
```
pytest --cov-config=.coveragerc --cov
```
3. Generate html reports:
```
pytest --cov-report=html:coverage-report --cov
```
This will generate a subfolder called coverage-report inside the project folder containing a html report about the code coverage (index.html)

## Deactivate virtual environment from terminal:
After you finished running the code and unittests/coverage report, you can deactive the virtual environment with the following command:
```
deactivate
```
