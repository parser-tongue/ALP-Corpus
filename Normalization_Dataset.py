from torch.utils import data
from pytorch_pretrained_bert import BertTokenizer

class Normalization(data.Dataset):
    def __init__(self, labelled_sents, label2idx, multigrams):
        self.tokenizer = BertTokenizer.from_pretrained('bert-swiss-lm', do_lower_case=True, never_split=multigrams)
        self.label2idx = label2idx
        sents, label_list = [], [] # list of lists
        for sent in labelled_sents:
            words = [normalization[0] for normalization in sent]
            labels = [normalization[1] for normalization in sent]
            sents.append(["[CLS]"] + words + ["[SEP]"])
            label_list.append(["<pad>"] + labels + ["<pad>"])
        self.sents, self.label_list = sents, label_list

    def __len__(self):
        return len(self.sents)

    def __getitem__(self, idx):
        words, labels = self.sents[idx], self.label_list[idx] # words, labels: string list
        # We give credits only to the first piece.
        x, y = [], [] # list of ids
        is_heads = [] # list. 1: the token is the first piece of a word
        for w, l in zip(words, labels):
            tokens = self.tokenizer.tokenize(w) if w not in ("[CLS]", "[SEP]") else [w]
            xx = self.tokenizer.convert_tokens_to_ids(tokens)
            is_head = [1] + [0]*(len(tokens) - 1)
            l = [l] + ["<pad>"] * (len(tokens) - 1)  # <PAD>: no decision
            l = [each.replace(" ","-") for each in l]
            yy = [self.label2idx[each] for each in l]  # (L,)

            x.extend(xx)
            is_heads.extend(is_head)
            y.extend(yy)
        assert len(x)==len(y)==len(is_heads), "len(x)={}, len(y)={}, len(is_heads)={}".format(len(x), len(y), len(is_heads))

        # seqlen
        seqlen = len(y)

        # to string
        words = " ".join(words)
        labels = [label.replace(" ","-") for label in labels]
        labels = " ".join(labels)

        return words, x, is_heads, labels, y, seqlen