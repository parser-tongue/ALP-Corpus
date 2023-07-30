import json
import os
from collections import Counter
from tokenize_GSW import tokenize, PUNCT

def find_first_vowel_index(word, vowel):
    vowels = "aäeioöôuü"
    if vowel == True:
        return next((index for index, char in enumerate(word) if char in vowels), -1)
    else:
        return next((index for index, char in enumerate(word) if char not in vowels), -1)

def find_suffix(word):
    backword = word[::-1]
    last_vowel = find_first_vowel_index(backword, True)
    last_consonant = last_vowel + 1 + find_first_vowel_index(backword[last_vowel+1:],False)
    suffix = backword[:last_consonant][::-1]
    return suffix

def get_rhymes(stanza):
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890$£äöüàé*%&"
    scheme = ""
    endrhymes = dict()
    halfrhymes = dict()
    i = -1
    for line in stanza:
        tokens = tokenize(line,PUNCT)
        if tokens:
            ending = tokens[-1:][0]
            endrhyme = find_suffix(ending)
            try:
                scheme += endrhymes[endrhyme]
            except KeyError:
                try:
                    scheme += endrhymes[endrhyme[:-1]]
                except KeyError:
                    try:
                        scheme += halfrhymes[endrhyme]
                    except KeyError:
                        i += 1
                        endrhymes[endrhyme] = alphabet[i]
                        halfrhymes[endrhyme[:-1]] = alphabet[i]
                        scheme += alphabet[i]
    return scheme

def get_stanzas(song):
    stanzas, rhyme_scheme, current_stanza = [],[],[]
    rhymes = ""
    if len(song[1].strip())>0:     # Ignore first two lines of songs with titles (songs with an empty second line):
        start = 0
    else:
        start = 2
    for line in song[start:]:
        if line:
            if len(line.strip())>0:  
                current_stanza.append(line)
            else: 
                stanzas.append(current_stanza)
                rhymes = get_rhymes(current_stanza)
                rhyme_scheme.append(rhymes)
                current_stanza = []   
    stanzas.append(current_stanza)
    return stanzas, rhyme_scheme

folder = "Corpus_JSON/"
# rawtext = "DataCollection/"
dest_folder = "Corpus_JSON/"
corpus_texts = []

song_ids = {}
i = 0
for filename in os.listdir(folder):
    with open(folder+filename) as file:
        print(" ")
        song_json = json.load(file)
        song_ids[i] = filename
        song = song_json['raw_text']
        stanzas, rhyme_schemes = get_stanzas(song)
        print(rhyme_schemes)
        scheme_counts = Counter(rhyme_schemes)
        total_schemes = len(rhyme_schemes)
        most_common_scheme, most_common_count = scheme_counts.most_common(1)[0]
        if most_common_count > total_schemes / 2:
            if len(most_common_scheme) > 15:
                rhyme_scheme = "freeform"
            else:
                rhyme_scheme = most_common_scheme
        else:
            rhyme_scheme = "irregular" 
        print(rhyme_scheme)
        song_json["num_stanzas"] = len(rhyme_schemes)
        if all(len(item) == len(rhyme_schemes[0]) for item in rhyme_schemes):
            if len(rhyme_schemes[0]) == 2:
                stanza_pattern = "couplets"
            elif len(rhyme_schemes[0]) == 4:
                stanza_pattern = "quatrains"
            elif len(rhyme_schemes[0]) == 3:
                stanza_pattern = "tercets"   
            elif len(rhyme_schemes[0]) == 5:
                stanza_pattern = "cinquains"  
            elif len(rhyme_schemes[0]) == 6:
                stanza_pattern = "sestets"  
            elif len(rhyme_schemes[0]) == 7:
                stanza_pattern = "septets"  
            elif len(rhyme_schemes[0]) == 8:
                stanza_pattern = "octets"  
            elif len(rhyme_schemes[0]) == 9:
                stanza_pattern = "nonets" 
            else:
                stanza_pattern = "other"
        else:
            stanza_pattern = "irregular"    
        print(stanza_pattern)
        song_json["rhyme_scheme"] = rhyme_scheme
        song_json["stanza_pattern"] = stanza_pattern
        keys_to_remove = ["endrhymes", "tokenized_text", "keywords"]
        for key in keys_to_remove:
            song_json.pop(key, None)
    with open(dest_folder+filename, 'w') as file:
        json.dump(song_json, file, ensure_ascii=False, indent=4)
    i+=1