# ALP-Corpus
## Alemannic Language Processing Corpus - a project towards MundArtificial Intelligence

This is the project repository for my Master's Thesis:

## "Schaffe, schaffe, Datenbank baue: NLP methods for folk songs in Swiss German dialects"

The full pipeline of the project runs in this order:

1. **Data_Collection.ipynb** catalogs some of the code used to collect the texts
2. **Corpus.ipynb** was used to produce the graphs in the thesis 
3. **Load_Training_Corpora.ipynb** Gets the training corpora for the dialect Normalizer and calculates the baseline ERR
4. **Train_Normalizer.ipynb** trains and saves the normalizer
5. **Test_Normalizer.ipynb** normalizes the ALP corpus of folk songs
6. **Embedded_Topic_Model.ipynb** sets up and models the topics. Code for the Weights & Biases hyperparameter sweep configuration is included *(private file - please contact me for access)*.

The remaining python scripts are called by various functions. 

The ArchiMob corpus on which the Normalizer is trained is available here:
https://drive.switch.ch/index.php/s/vYZv9sNKetuPYTn

The resources used for augmenting the MFR procedure are available online:
- WUS https://drive.switch.ch/index.php/s/chlu1xuLzfQ0kBi
- Bilexicon https://github.com/mainlp/dialect-BLI/blob/main/bli_data/bilexicon/als/bilexicon.csv

Additionally, I have provided a Google Drive with pre-trained embeddings as KeyedVectors, as well as the pre-trained Normalizer used. 
https://drive.google.com/drive/folders/1eXGLqmpj-HPLrI0hue45Y6jAjISuoE6H?usp=sharing

All of the above resources are best placed in the same local repository so that the notebooks all run properly. 

The full paper is hosted here too:
[msc-samuel-reed-12180974.pdf](https://github.com/parser-tongue/ALP-Corpus/files/12213151/msc-samuel-reed-12180974.pdf)
