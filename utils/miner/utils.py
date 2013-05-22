import subprocess
import re
from conf import CLASS_BLACKLIST
import random
import string

def replace_classnames(code):
    char_set = string.ascii_lowercase
    result = code
    for item in CLASS_BLACKLIST:
        if "%s(" % item in result:
            rand = ''.join(random.sample(char_set*6,6))
            result = result.replace(item, rand)
    return result


def run(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, error = p.communicate()
    yield output


def sanitize(string):
    "Converts parameters and stuff to be correctly evaluated."
    # Remove double parentesis
    sane = string.strip().replace('))', ')')
    # Boolean values
    sane = sane.strip().replace('false', 'False')
    sane = sane.strip().replace('true', 'True')
    # Convert float values to string
    regex = re.compile('([\-]?\d?\.?\d\F)')
    sane = regex.sub("'\1'", sane)
    # Convert rest t
    regex = re.compile('([, |\(])([\w+\d+\.]+)')
    sane = regex.sub(r'\1"\2"', sane)
    sane = replace_classnames(sane)
    return sane
