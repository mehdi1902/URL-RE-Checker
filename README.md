# URL-RE-Checker
Checking some regex for each URL from a list

# Usage
```$ python3 find.py -i input.json -o output.json```

One can create a `test.json` file with `N` samples using:
```$ python3 find.py -t N```
in which `N` is an int.

## input_file
It supports both `.json` and normal files as input. Format of the normal file would be:
```
> url1
regex1
regex2
> url2
regex3
regex4
regex5
```
Note: Name of a json file MUST be `*.json` otherwise it would be considered as a normal file. 

## templates
There is a template file (`regex_templates`) in which you can specify some regex strings in this format:
```
#some_names1
regex1
#some_names2
regex2
```
In this case, instead of using a regex in the input file, you can use #EMAIL for example. You can add your own regex templates in the file as well.

# Requirements
The only requirement is urllib3 which you can install using pip:

```$ pip3 install urllib3```

or using the requirements.txt file provided here:

```$ pip3 install -r requirements.txt```
