from nltk.corpus import cmudict
from flask import Flask, render_template
from random import choice
from collections import defaultdict
import re

MIN_LENGTH = 3
WORD_RE = re.compile('^\w+$')

SOUNDS_LIKE = defaultdict(list)

SOUNDS_LIKE.update({
    'a' : ['EH', 'EY', 'A'],
    'b' : ['B'],
    'c' : ['K', 'CH'],
    'd' : ['D'],
    'e' : ['E','IH', 'IY'],
    'f' : ['F'],
    'g' : ['G', 'JH'],
    'h' : ['H'],
    'i' : ['I', 'AY'],
    'j' : ['J'],
    'k' : ['K'],
    'l' : ['L'],
    'm' : ['M'],
    'n' : ['N'],
    'o' : ['O', 'AA'],
    'p' : ['P'],
    'q' : ['K'],
    'r' : ['R'],
    's' : ['S'],
    't' : ['T', 'DH'],
    'u' : ['U'],
    'v' : ['V'],
    'w' : ['W'],
    'x' : ['X'],
    'y' : ['Y'],
    'z' : ['Z']
})


app = Flask(__name__)
app.debug = True
 
def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)
 
candidates = [e for e in cmudict.entries()
              if len(e[0]) > MIN_LENGTH 
              and WORD_RE.match(e[0])
              and not any(e[1][0].startswith(c) for c in SOUNDS_LIKE[e[0][0].lower()] )]
separated = {}
for l in char_range('a', 'z'):
    separated[l] = [e for e in candidates if e[0][0].lower() == l]

def get_random_dictionary():
    generated = []
    for l in char_range('a', 'z'):
        word = ("Nothing Yet :(", [])
        if len(separated[l]) > 0:
            word = choice(separated[l])
        generated.append((l, word[0], word[1]))
    return generated

@app.route("/")
def index():
    generated = get_random_dictionary()
    return render_template("index.html", dictionary=generated)

if __name__ == "__main__":
    for l, words in separated.items():
        print l, len(words)
    app.run()
