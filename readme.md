
## How I Approached To This Solution

I started off by extracting data from the links given in the Input.xlsx using the request module of python. Then I extracted the data from the html elements and stored it. Then I calculated the all the variables that are asked to find out. Then I stored them in the output.xlsx file.

## Running The Program

To run the program you should have python3 and pip3 install in your local.

First of all, clone this project using git from the command
or just paste the folder in your local system.

```bash
git clone https://github.com/mdrehan369/BlackCofferInternship.git
```
Now navigate to the folder and open the terminal there. In the terminal, write the following command to create a virtual environment

```bash
pip install virtualenv
virtualenv my_env

# To activate virtual environment on windows:
my_env\Scripts\activate

# To activate virtual environment on Linux or Mac OS:
source my_env/bin/activate
```

Now install all the dependencies by the following command

```bash
pip install -r requirements.txt
```
Now run the python file using the following command
```bash
python extract.py
```

## Dependies
- beautifulsoup4
- bs4
- html5lib
- nltk
- openpyxl
- pandas
- requests
