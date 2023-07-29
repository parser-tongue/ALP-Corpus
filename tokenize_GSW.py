import string
PUNCT = ['«', '»', '.', ',',':', '!', '?', ';', '"', '(',')' ,'[',']',"•","♪"] # custom punctuation list which does not include apostrophes or hyphens

def tokenize(line,punct):
    line.strip()
    line = line.replace("’","'")  
    line = line.replace("d'","d' ")  # the following lines separate the articles/prepositions from the nouns
    line = line.replace("D'","D' ")  
    line = line.replace("z'","z' ")  
    line = line.replace("Z'","Z' ")
    line = line.replace("'s"," 's")
    line = line.replace("'n"," 'n")

    for p in punct:
        line = line.replace(p, ' '+p+' ')
    line = [token.rstrip(string.punctuation) for token in line.split()] # removes trailing punctuation 
    return [token.lower() for token in line if token not in PUNCT and token]