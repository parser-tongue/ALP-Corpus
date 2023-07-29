from torch.utils import data
from pytorch_pretrained_bert import BertTokenizer

class Testing(data.Dataset):
    def __init__(self, songs):
        self.tokenizer = BertTokenizer.from_pretrained('bert-swiss-lm', do_lower_case=True)
        tokenized_lines = []
        for song in songs:
            for line in song:
                tokenized_lines.append(["[CLS]"] + line + ["[SEP]"])
        self.lines = tokenized_lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, idx):
        line = self.lines[idx] # words: string list
        # We give credits only to the first piece.
        x = []
        is_heads = [] # list. 1: the token is the first piece of a word
        for word in line:
            if word:
                tokens = self.tokenizer.tokenize(word) if word not in ("[CLS]", "[SEP]") else [word]
                xx = self.tokenizer.convert_tokens_to_ids(tokens)
                is_head = [1] + [0]*(len(tokens) - 1)
                x.extend(xx)
                is_heads.extend(is_head)
        
        assert len(x)==len(is_heads), "len(x)={}, len(is_heads)={}".format(len(x), len(is_heads))
        # to string
        seqlen = len(x)
        return line, x, is_heads, seqlen