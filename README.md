## cs5293sp23-project1 (Text - Analytics Project 1)
## Author - Pranav Vichare
## Project - The Redactor
**About:**  In this project, Enron Email Dataset is used which has various emails in the form of text file. The dataset contains 1.7 Gb and more than 500,000 email messages. We have only considered 5 text files as sample data. The email has sensitive data which is to be redacted. The sensitive data is in terms of Names, Address, Gender, Dates and Phones. This sensitive data should be replaced by Redact character '█'. The redacted data should be stored with extension .redacted with original filenames. Stats files needs to be created which will contain all the data which is redacted and their indexes.

To run the code, Use the commands below in terminal or Visual Studio Code
```python
pipenv --python 3.9  #use your version of python which is installed on your system. This code is also used to create a virtual environment
pipenv install spacy #to install spacy library in virtual environment
#to install spacy en_core_web_sm model in virtual environment
pipenv install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.4.1/en_core_web_sm-3.4.1-py3-none-any.whl
pipenv install pytest #to install pytest library in virtual environment
pipenv lock #to create piplock file
```

```python
import argparse
import os
import glob
import spacy
import re
```
To run the code, Import all the libraries listed above in the python code.

To run the code from the terminal use below command:
```
pipenv run python redactor.py --input '*.txt' --names --dates --phones --genders --address --output 'files/' --stats stderr
```

### Code Explanation  
```python
#redactor.py has 6 functions as shown below.
def redact_names()
def redact_dates()
def redact_phones()
def redact_genders()
def redact_addresses()
def main()
```
The main function mentioned above will be executed and calls other functions. The input .txt files in the directory will be read. The text from each file will be sent to the remaining 5 functions from the **main()** function.
The text will be sent to each function. Spacy model **en_core_web_sm** is used. Each function will find the match from the entire text and replace it with Redact character. The redacting functions will return two variables.
The redacted terms with their stats will be stored in a .txt file. Stats will include the redacted terms and their indexes.
```
1.Redacted text
2.Redacted terms with their indexes.
```
These values are stored in the stats files.
*The output video of the execution is stored in **Output docs** folder*

### Code Output
The code output is stored in stored in stats file with name : **stderr.txt**. The stats file will have the terms redacted and their indexes and count of types of terms redacted.
![image](https://github.com/Pranavv361/cs5293sp23-project1/blob/main/Output%20docs/Stats%20file%20output.png)

### Test Output
The test cases are created in single file **test.py**. The purpose of the test.py is to check the functions with sample input and make sure we get correct output. The attached image below shows the output for test cases of all the functions.
To run the test.py using pytest library use the following code.
```
pipenv run python -m pytest .\test\test.py
```
![image](https://github.com/Pranavv361/cs5293sp23-project1/blob/main/Output%20docs/test.py%20output.png)

### Assumptions:
1. Limited values of gender terms and pronouns are assumed in an array in **redact_genders()** functions, which will be compared to the test data
```
gender_terms = ['male', 'female', 'transgender', 'cisgender','they', 'them','their', 'theirs',
                    'themselves','father','mother']
pronouns = ['he','she','him', 'her','his','men', 'women']
```
2. The redacted address is dependent on **LOC** and **GPE** for entity recognition.

### Bugs:   
1. The output of some redacted terms depends upon the Spacy model **en_core_web_sm**.
2. The single address which comprises of multiple terms will be considered as separate terms.
For example:
```python
'Norman, Oklahoma'
[('Norman', 0, 5),('Oklahoma', 8, 15)]
# Same address will be considered as two separate redacted terms but they are same part of the address
```
3. The opening bracket in the phone number is not redacted.
For example:
```python
'(405)-859-9000'
'(█████████████'  #output
# The opening bracket will not be redacted.
```
