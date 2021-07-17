"""

Chapter 2 - Regular Expression - Exercises 
from Speech and Language Processing by Martin and Jurafsky, 3e
freely available draft dated December 2020

"""

__author__ = 'Vaibhav Mittal'
__date__ = '2021/07/03'

from re import finditer, compile
import numpy as np
# # from https://regexone.com/references/python

## RegEx to find the set of all alphabetic strings

regex = compile(r'[A-Za-z]+')
target = 'abc012!@#abc!@#a bcb	1'

for i in finditer(regex, target):
    print(i)

# <re.Match object; span=(0, 3), match='abc'>
# <re.Match object; span=(9, 12), match='abc'>
# <re.Match object; span=(15, 16), match='a'>
# <re.Match object; span=(17, 20), match='bcb'>

## Find the set of all lowercase alphabetic strings eding in a 'b'

regex = compile(r'[a-z]+b')
target = 'abc012!@#abcb!@#a bcb	1abb#bbba AB Ab'

for i in finditer(regex, target):
    print(i)

# # <re.Match object; span=(0, 2), match='ab'>
# # <re.Match object; span=(9, 13), match='abcb'>
# # <re.Match object; span=(18, 21), match='bcb'>
# # <re.Match object; span=(22, 25), match='abb'>
# # <re.Match object; span=(26, 29), match='bbb'>

## Find the set of all strings from the alphabet a, b such that each 'a' is 
## immediately preceded by and immediately followed by 'b'

regex = compile(r'aab')
target = 'aabababababbbabaaababaababaaaabaabaabababababababababa'

for i in finditer(regex, target):
    print(i)

# # <re.Match object; span=(0, 3), match='aab'>
# # <re.Match object; span=(16, 19), match='aab'>
# # <re.Match object; span=(21, 24), match='aab'>
# # <re.Match object; span=(28, 31), match='aab'>
# # <re.Match object; span=(31, 34), match='aab'>
# # <re.Match object; span=(34, 37), match='aab'>

# # the look-behind and look-ahead operators could also have been used here

## Find the set of all strings with two consecutive repeated words (eg. "Humbert Humbert"
## and "the the" but not "the bug" or "the big bug")


regex = compile(r'(\w+)\s+\1\b')
target = "Humbert Humbert the Humbert big the the big bug"

for i in finditer(regex, target):
    print(i)

# # <re.Match object; span=(0, 15), match='Humbert Humbert'>
# # <re.Match object; span=(32, 39), match='the the'>

## All strings that start at the beginning of the line with an integer an 
## that end at the end of the line with a word

regex = compile(r'^\d.*\w$')
target = r"12Humbert Humbert the Humbert big the the big bug\nHumbert Humbert the Humbert big the the big bug\nHumber humbert is"

for i in finditer(regex, target):
    print(i)

# # <re.Match object; span=(0, 98), match='12Humbert Humbert the Humbert big the the big bug>

## all strings that have both the word 'grotto' and the word 'raven' in them but 
## not words like 'grottos' that merely contain the word 'grotto'.

regex =  compile(r'(\bgrotto\b.*\braven\b)|(\braven\b.*\bgrotto\b)')
target = r"Humbert had a grotto and a raven in Germany\nHumbert likes grottos\nHumbert likes that raven"

for i in finditer(regex, target):
    print(i)

# # <re.Match object; span=(14, 92), match='grotto and a raven in Germany\\nHumbert likes gro>


### Minimum Edit Distance


def min_edit_distance(source, target, del_cost = 1, ins_cost = 1, sub_cost = 2):
    """
    A function which takes a source and target (string) and returns the minimum edit distance (integer)
    """
    n = len(source)
    m = len(target)
    D = np.zeros((n+1, m+1))
    for i in range(1, n+1):
        D[i, 0] = D[i-1, 0] + del_cost
    for j in range(1, m+1):
        D[0, j] = D[0, j-1] + ins_cost
    
    for i in range(1, n+1):
        for j in range(1, m+1):
            deletion = D[i-1, j] + del_cost
            insertion = D[i, j-1] + ins_cost
            substitution = D[i-1, j-1] + calculate_sub_cost(source[i-1], target[j-1], sub_cost)
            D[i, j] = min(deletion, insertion, substitution)
    return D[n, m]

def calculate_sub_cost(source, target, sub_cost = 2):
    """
    A function to calculate substitution costs taking the substitution or non-substitution into account
    """
    
    if source == target:
        return 0
    else:
        return sub_cost

med = min_edit_distance("intention", "execution", del_cost = 1, ins_cost = 1, sub_cost = 2)
print(med)
