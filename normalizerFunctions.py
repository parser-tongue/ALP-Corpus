from pytorch_pretrained_bert import BertModel
import torch
import torch.nn as nn

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# define normalization dictionary update function
def update_norm_dict(utterance, norm_counts, multigrams):
    """ 
    updates norm_counts dictionary with new normalizations of the form
    dict['wordform']= {'normalization': int}
    """
    for word, norm in utterance: 
        if " " in norm:
            norm = norm.replace(" ","-") # handles one-to-many normalizations, by treating them as single lexical units 
            multigrams.append(norm)
        if " " in word:     # handles many-to-one normalizations
            word = word.replace(" ","-")  
        try:
            norm_count = norm_counts[word] # if the surface word has been encountered before...
            try:
                norm_count[norm] += 1 # ...update the count of the current nomalization
            except KeyError:
                norm_count = {norm: 1} # ... or if the current normalization is new, add it to the count dictionary
                norm_counts[word].update(norm_count)
        except KeyError:
            norm_count = {norm: 1} # else add a new count for the first normalization of newly encountered words
            norm_counts[word] = norm_count
    return norm_counts

class Training_Corpus(object):
    def __init__(self,folder_path, method):
        self.word_norm_pairs = method(folder_path)
        self.norm_dict = {}
        self.multigrams = []
        for l in self.word_norm_pairs:
            update_norm_dict(l, self.norm_dict,self.multigrams)
        self.labels = set([norm for _,norm_dict in self.norm_dict.items() for norm in norm_dict.keys()])


class Token_Classifier(nn.Module):
    def __init__(self, label2idx, idx2label):
        super().__init__()
        self.label2idx = label2idx
        self.idx2label = idx2label
        vocab_size = len(label2idx)
        self.bert = BertModel.from_pretrained('bert-swiss-lm')

        self.fc = nn.Linear(768, vocab_size) # this is just the ouput shape for BertModel
        self.device = device

    def forward(self, x, y):
        x = x.to(device) # (N, L). int64
        y = y.to(device) # (N, L). int64
        with torch.set_grad_enabled(self.training):
            self.bert.train(self.training)
            encoded_layers, _ = self.bert(x)
            enc = encoded_layers[-1]
        logits = self.fc(enc)
        y_hat = logits.argmax(-1)
        return logits, y, y_hat
    
    def normalize(self, x):
        self.bert.eval()
        with torch.no_grad():
            encoded_layers, _ = self.bert(x)
            enc = encoded_layers[-1]
        logits = self.fc(enc)
        prediction = logits.argmax(-1)
        return prediction
