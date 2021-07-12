#Librerias
from TratamientoCorpus import Nombres_Total
import os
import re
import string
import pandas as pd
import nltk
import nltk.stem
import spacy
import es_core_news_sm
import spacy_spanish_lemmatizer
import numpy as np
import matplotlib.pyplot as plt
import operator
from wordcloud import WordCloud
from matplotlib.pyplot import title
from nltk.corpus import stopwords
from IPython.display import display
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer 
from PIL import Image

# Nombrar archivos resultado
NombreTotales = 'TFIDF.csv'
NombreNube = 'tf_idfWordCloud.png'
NombreArchivo = 'Corpus_Tratado.txt'

# Descargamos soportes para la biblioteca NLTK
nltk.download('stopwords')
stop_words = stopwords.words('spanish')

#Extendemos stopWords
words=['ley','propone','nacional','interés','pública','necesidad','artículo','declara','modifica','modificar','declarar','provincia','decreto','departamento','perú','distrito','artículos','así', 'año','través','núm','proponer','aahh','aautógrafa', 'público', 'establecer']
stop_words.extend(words)

# Leemos el CorpusTratado.txt
with open("./Corpus Procesados/"+NombreArchivo,"r") as trat:
    listaleyes = trat.read().split("\n")
titulos = []
textos = []
for k in range(len(listaleyes)-1):
    if k % 2 ==0:
        titulos.append(listaleyes[k]) # Obtenemos títulos
    else:
        textos.append(listaleyes[k]) # Obtenemos Leyes

dict = {}
corpus = []
for Data in textos:
    corpus = nltk.sent_tokenize(Data)

dict['texto'] = textos
df = pd.DataFrame(dict)

# Realizamos la lematización y tokenización 
nlp = spacy.load("es_core_news_sm") # Cambiamos idioma lemmatizer
for i in range(0, len(df)):
    cadena = df['texto'][i]
    lemmat = nlp(cadena)
    nuevo = ""
    for palabra in lemmat:  # Lematización
        if(len(palabra)<=2 or len(palabra)>=15):
            continue
        nuevo = nuevo + palabra.lemma_+' '
    nuevo = nuevo.split(' ')
    cad = []
    for token in nuevo: # Tokenización
        if token in stop_words:
            continue
        cad.append(token)
    cadena = ' '.join(cad)
    corpus.append(cadena)

# Creamor el BOW del corpus 
bow_corpus = CountVectorizer().fit(corpus)
count_tokens=bow_corpus.get_feature_names()
word_count = bow_corpus.fit_transform(corpus)
corpus_vect = bow_corpus.transform(corpus)
df_count_vect=pd.DataFrame(data=corpus_vect.toarray(),columns=count_tokens)
display(df_count_vect)  
#df_count_vect.to_csv(NombreMatriz) # Guardamos el BOW en archivo csv

# Creamos el ITF del corpus 
tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count)
df_idf = pd.DataFrame(tfidf_transformer.idf_,index=bow_corpus.get_feature_names(),columns=['idf'])
df_idf.sort_values(by=['idf'])
df_idf.to_csv('./ITF.csv')

# Creamos el BOW - TF-IDF del corpus 
bow_corpus = TfidfVectorizer().fit(corpus)
word_count = bow_corpus.fit_transform(corpus)
count_tokens=bow_corpus.get_feature_names()
corpus_vect = bow_corpus.transform(corpus)
#print(format(corpus_vect.toarray()))
print(count_tokens)
#df_count_vect.to_csv(NombreMatriz) # Guardamos el BOW en archivo csv

df_count_vect=pd.DataFrame(data=corpus_vect.toarray(),columns=count_tokens)

display(df_count_vect)  
count_words = np.asarray(corpus_vect.sum(axis=0))[0]
diccionario = {count_tokens[n]: count_words[n] for n in range(len(count_tokens))}
#print(diccionario)
sort = sorted(diccionario.items(),key=operator.itemgetter(1),reverse=True)
print(sort[0:30])

wordcloud = WordCloud(font_path = 'calibri',width=900,height=500,background_color='white',colormap='Dark2')#mask=peru_mask
wordcloud.generate_from_frequencies(frequencies=diccionario)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

with open('TFIDF.csv', 'w') as f:
    for key in diccionario.keys():
        f.write("%s,%s\n"%(key, diccionario[key]))
