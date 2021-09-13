import urllib3
import json
import re
import sys
from time import time
import signal
import getopt


def download_site(url, pool=None, decode=True):
    """
    Fetching the contents from url.
    args:
        url (str): The url!
        pool (urllib3.PoolManager): The pool that we use to fetch the url
            If it is "None", it will create a pool.
        decode (bool): If False, return the raw website (object).
                       If True, return the decoded page
    return:
        site content and a dict of extra information (elapsed time)
    """
    if pool is None:
        pool = urllib3.PoolManager()
    t1 = time()
    try:
        site = pool.request('GET', url)
        if decode:
            site = site.data.decode("utf-8")
        error = 'No error'
    except Exception as e:
        error = str(e)
        print('Problem with requesting %s' % (url))
        site = urllib3.response.HTTPResponse('<!DOCTYPE html><html><body><h1>INVALID</h1></body></html>')
        site.status = 404
        if decode:
            site = 'INVALID URL!'
    elapsed_time = time() - t1
    return site, {'fetching time (s)': elapsed_time, 'error':error}


def match_site(url, regex_list, pool=None, unique=False):
    """
    Read an url and return matched patterns
    args:
        url (str): The url
        regex_list (list): a list contains regex strings
        pool (urllib3.PoolManager): The pool that we use to fetch the url
            If it is "None", it will create a pool.
        unique (bool): If true, it remove the matched redundancies
    return:
        a dict in which the keys are the regex strings and values are
            a list of matched values from the url.
        another dict of extra information
    """
    content, info = download_site(url, pool=pool, decode=True)
    matched = {}
    t1 = time()
    for regex in regex_list:
        matched[regex] = re.findall(regex, content)
    processing_time = time() - t1
    info['processing time (s)'] = processing_time
    return matched, info


def load_input_file(input_file):
    """
    Read the samples from a normal file with the following format or a json:
        > url1
        regex1
        regex2
        > url2
        regex3
        regex4  
    args:
        input file (str): address of the file
    """
    if '.json' in input_file:
        try:
            all_samples = json.load(open(input_file, 'r'))
        except:
            print("Error in reading the json file")
            sys.exit(2)
    else:
        with open(input_file, 'r') as f:
            lines = f.read().split('\n')
            url_dict = {}
            all_samples = []
            key = ''
            for line in lines:
                if '>' in line:
                    line = line.replace(' ', '') # To handle a user mistake for not entering space
                    if url_dict != {}:
                        all_samples.append(url_dict)
                    url_dict = {}
                    key = line[1:]
                    url_dict[key] = []
                elif line:
                    url_dict[key].append(line)
            all_samples.append(url_dict)
    return all_samples


def download_all(input_file, output_file, unique=False):
    """
    Find all the patterns for each website from input_file and write the log in output_file
    args:
        input_file (str): address for the input json file
        output_file (str): address for the output json file
    """
    
    def signal_handler(sig, frame): # Handling an intrupt and writing the results so far
        print('Interrupted by user! Results are saved in %s' % (output_file))
        json.dump(all_matched, open(output_file, 'w+'), indent=2)
        sys.exit(2)
    signal.signal(signal.SIGINT, signal_handler)

    pool = urllib3.PoolManager()
    all_matched = []
    for s_id, sample in enumerate(load_input_file(input_file)):
        url, regex_list = list(sample.items())[0]
        matched, info = match_site(url, regex_list, pool=pool, unique=unique)
        matched = {url: matched}
        for key in info:
            matched[url][key] = info[key]
        all_matched.append(matched)
    json.dump(all_matched, open(output_file, 'w+'), indent=2)


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('$ python3 find.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('$ python3 find.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    download_all(input_file, output_file)

if __name__ == "__main__":
    main(sys.argv[1:])