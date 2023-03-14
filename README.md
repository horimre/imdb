# imdb top 20 movie scraper

## Installation guide:

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

windows:
  ```
  .venv\Scripts\activate.bat
  ```
mac\linux:
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
  
## How to execute the script from terminal:

Inside the virtual environment execute the script with the following command:
```
python imdb.py
```
The scipt produces two output files. Open them from the project folder.

## How to execute unit tests and check coverage report:
Inside the virtual environment execute the following commands:
1. Run unittests
```
coverage run imdb_test.py
```
2. Check code coverage:
```
coverage report
```
3. Generate html reports:
```
coverage html
```
This will generate a subfolder called htmlcov inside the project folder, and html reports about the code coverage (eg. imdb_py.html)

## Deactivate virtual environment:
After you finished running the code and unittests/coverage report, you can deactive the virtual environment with the following command:
```
deactivate
```
