# ALP-Corpus
## Alemannic Language Processing Corpus - a project towards MundArtificial Intelligence

This is the project repository for my Master's Thesis:

## "Schaffe, schaffe, Datenbank baue: NLP methods for folk songs in Swiss German dialects"

The full pipeline of the project runs in this order:

1. **Data_Collection.ipynb** catalogs some of the code used to collect this texts
2. **Corpus.ipynb** was used to produce the graphs in the thesis 
3. **Load_Training_Corpora.ipynb** Gets the training corpora for the Normalizer and calculates the baseline ERR
4. **Train_Normalizer.ipynb** trains and saves a sequence labeller
5. **Test_Normalizer.ipynb** normalizes the ALP corpus of folk songs
6. **Embedded_Topic_Model.ipynb** set up and models the topics. Code for the last hyperparameter sweep configuration is still present.

The remaining files are called by various functions. 
