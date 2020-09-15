import sys
import math
import itertools
import collections
from random import choice
from copy import deepcopy
from string import ascii_letters, digits
from ngram_score import *

# Decrypt functions
def morseToADFGVX(code):
    new_code = ""
    i = 0
    while i < len(code):
        if code[i:i+3] == ".-/":
            new_code += "A"
            i += 3
        elif code[i:i+4] == "-../":
            new_code += "D"
            i += 4
        elif code[i:i+5] == "..-./":
            new_code += "F"
            i += 5
        elif code[i:i+4] == "--./":
            new_code += "G"
            i += 4
        elif code[i:i+5] == "...-/":
            new_code += "V"
            i += 5
        elif code[i:i+5] == "-..-/":
            new_code += "X"
            i += 5
        else:
            print("UNRECOGNISED MORSE CODE FOUND FOR ADFGVX!")
            return ""
    return new_code

def decryptPolybius(code, polybius_square):
    new_code = ""
    for i in range(0,len(code),2):
        new_code += polybius_square[(code[i],code[i+1])]
    return new_code

def inv_column_transpose(s, keyword):
    kw_sorted_indices = (i for i,k in sorted(enumerate(keyword), key=lambda t: t[1]))
    shorter_cols = range(len(keyword) - (len(keyword) - len(s)%len(keyword)), len(keyword))
    col_len = len(s)//len(keyword) + 1
    k = 0
    columns = dict()
    for c in kw_sorted_indices:
        length = col_len - int(c in shorter_cols)
        columns[c] = s[k:k+length]
        k += length  
    return "".join(columns[i%len(keyword)][i//len(keyword)] for i in range(len(s)))

# Frequency analysis and index of coincidence
def calcIC(code):
    frequencies = collections.Counter(code)
    fsum = 0.0
    for el in (ascii_letters + digits):
        fsum += frequencies[el] * (frequencies[el] - 1)
    N = len(code)
    return fsum / (N*(N-1))

def frequencyAnalysis(code, numberOfChars):
    i = 0
    totalParts = 0
    frequencies = {}
    while i < len(code):
        partToInspect = code[i:i+numberOfChars]
        if partToInspect not in frequencies:
            frequencies[partToInspect] = 0
        frequencies[partToInspect] += 1
        i += numberOfChars
        totalParts += 1
    frequenciesPercentage = {}
    for item in frequencies:
        frequenciesPercentage[item] = float(frequencies[item]/totalParts)*100
    return frequenciesPercentage

def get_frequencies(frequency_file):
    frequencies = open(frequency_file, 'r')
    result = {}
    total = 0
    line = frequencies.readline()
    while line != "":
        result[line[0]] = int(line[2:])
        total += int(line[2:])
        line = frequencies.readline()
    for key in result.keys():
        result[key] = float(result[key]/total)
    return sorted(result.items(), reverse = True, key=lambda t: t[1])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Use: python3 decode_try.py [input_file.txt] [language]")
    else:
        maxPermKeyLength = 12
        # Load and decode morse code file.
        print("Start Decoding of " + sys.argv[1])
        codeFile = open(sys.argv[1], 'r')
        code = codeFile.read()
        code = morseToADFGVX(code)
        print("Decoding done.")
        # Set up objects for statistical analysis.
        quadgram_file = "data/frequencies/" + sys.argv[2] + "_quadgrams.txt"
        letter_order = [t[0] for t in get_frequencies("data/frequencies/" + sys.argv[2] + "_monograms.txt")]
        fitness = ngram_score(quadgram_file)
        results = {}
        for keyLength in range(1, maxPermKeyLength+1):
            # Bruteforce the permutations for every key length.
            for i in itertools.permutations(range(keyLength), keyLength):
                nonPermCode = inv_column_transpose(code, i)
                # Fill the polybius square by linking bigrams 
                # with alphanumeric elements based on frequency.
                nonPermCodeFreq = sorted(frequencyAnalysis(nonPermCode, 2).items(), reverse = True, key=lambda t: t[1])
                polybius_square = {}
                for index, item in enumerate(nonPermCodeFreq):
                    polybius_square[(item[0][0], item[0][1])] = letter_order[index]
                decryptCode = decryptPolybius(nonPermCode, polybius_square)
                ic = calcIC(decryptCode)
                # If the index of coincidence is high, we can assume 
                # the code is no longer a permutation.
                if ic > 0.08:
                    print("Deciphering monoalphabetic substitution")
                    highestScore = fitness.score(decryptCode.lower())
                    tries = 0
                    while True:
                        # Switch two letters at random of the polybius_square.
                        randEl1 = choice(list(polybius_square.keys()))
                        randEl2 = choice(list(polybius_square.keys()))
                        temp_polybius_square = deepcopy(polybius_square)
                        temp_polybius_square[randEl1] = polybius_square[randEl2]
                        temp_polybius_square[randEl2] = polybius_square[randEl1]
                        decryptCode = decryptPolybius(nonPermCode, temp_polybius_square)
                        score = fitness.score(decryptCode.lower())
                        # If the result is closer to the target language, print it.
                        if score > highestScore:
                            highestScore = score
                            polybius_square = temp_polybius_square
                            tries = 0
                            print("Fitness score: ", score)
                            print("Permutation: ", i)
                            for key, value in polybius_square.items():
                                print(key, ": ", value)
                            print(decryptCode)
                            print("")
                        tries += 1
                        if tries > 10000:
                            sys.exit()
