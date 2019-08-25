# Boring preliminaries
from __future__ import division
import re
import math
import string
from collections import Counter

TEXT = open('big.txt').read()
print(len(TEXT))

def tokens(text):
    "List all the word tokens (consecutive letters) in a text. Normalize to lowercase."
    return re.findall('[a-z|-]+', text.lower())


WORDS = tokens(TEXT)
#print(type(WORDS))

COUNTS = Counter(WORDS)

#print (COUNTS.most_common(10))

def known(words):
    "Return the subset of words that are actually in the dictionary."
    return {w for w in words if w in COUNTS}

def edits0(word): 
    "Return all strings that are zero edits away from word (i.e., just word itself)."
    return {word}

def edits2(word):
    "Return all strings that are two edits away from this word."
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}

def edits1(word):
    "Return all strings that are one edit away from this word."
    pairs      = splits(word)
    deletes    = [a+b[1:]           for (a, b) in pairs if b]
    transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
    replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
    inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def splits(word):
    "Return a list of all possible (first, rest) pairs that comprise word."
    return [(word[:i], word[i:]) 
            for i in range(len(word)+1)]

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def pdist(counter):
    "Make a probability distribution, given evidence from a Counter."
    N = sum(counter.values())
    return lambda x: counter[x]/N

P = pdist(COUNTS)


def Pwords(words):
    "Probability of words, assuming each word is independent of others."
    return product(P(w) for w in words)

def product(nums):
    "Multiply the numbers together.  (Like `sum`, but with multiplication.)"
    result = 1
    for x in nums:
        result *= x
    return result


sentence = "his is a neverbeforeseen test"
print (Pwords(tokens(sentence)))

def memo(f):
    "Memoize function f, whose args must all be hashable."
    cache = {}
    def fmemo(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    fmemo.cache = cache
    return fmemo


def splits(text, start=0, L=20):
    "Return a list of all (first, rest) pairs; start <= len(first) <= L."
    return [(text[:i], text[i:]) 
            for i in range(start, min(len(text), L)+1)]


@memo
def segment(text):
    "Return a list of words that is the most probable segmentation of text."
    if not text: 
        return []
    else:
        candidates = ([first] + segment(rest) 
                      for (first, rest) in splits(text, 1))
        return max(candidates, key=Pwords)

def correct(word):
    "Find the best spelling correction for this word."
    # Prefer edit distance 0, then 1, then 2; otherwise default to word itself.
    candidates = (known(edits0(word)) or 
                  known(edits1(word)) or 
                  known(edits2(word)) or 
                  [word])
    return (candidates)
    #return max(candidates, key=COUNTS.get)

def wordcorrection(word): 
    "Most probable spelling correction for word."
    return max(correct(word), key=COUNTS.get)

output = []
word = 'working memory'
word = word.replace(" ", "_")
word = word.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=_+"})
correction = list(correct(word))
candidate = wordcorrection(word)

print("test")
print(word)
print(correction)
print(candidate)


if len(correction) == 1 and word == correction[0] and len(list(known(edits0(word)))) == 0:
    print("input and spell corrected are same and invalid word")
    seg = segment(word)
    if len(seg)>1:
        print("word splitting")
        output = seg.copy()
    else:
        print("spell checking")
        output = correction.copy()

else:
    print("spell checking")
    output = correction.copy()
print("output list")
print(output)