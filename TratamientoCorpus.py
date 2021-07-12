import os
import pandas as pd
from IPython.display import display
import re
import string

##Lee el corpus, limpia
def LimpiarCadena(Cadena):
    Cadena = Cadena.lower()#Minusculas
    Cadena = re.sub('\[.*‘’“”…«»?¿\]\%', ' ', Cadena)#Quitamos texto encerrado
    Cadena = re.sub('[%s]' % re.escape(string.punctuation), ' ', Cadena)#Puntuacion
    Cadena = re.sub('\w*\d\w*', '', Cadena)#Cadenas que tengan nros?
    Cadena = re.sub('\n', ' ', Cadena)#Salto de linea
    Cadena = re.sub('  ', ' ', Cadena)#Doble espacio
    return Cadena
    
#============
#Lectura de todo el corpus
#============

Nombres = os.listdir('./Corpus/')
Anios = ["2016","2017","2018","2019","2020","2021"]

NombresAnios = ( [] ,[] ,[] ,[] ,[] ,[] )
CorpusAnios = ( [] ,[] ,[] ,[] ,[] ,[] )

'''
NombreLegislaturas = ( [] ,[] ,[] ,[] ,[] ,[] ,[],[],[],[])
Legislaturas = ["Segunda Legislatura Ordinaria 2016",
                "Tercera Legislatura Ordinaria 2020",
                "Primera Legislatura Ordinaria 2018",
                "Primera Legislatura Ordinaria 2020",
                "Primera Legislatura Ordinaria 2017",
                "Cuarta Legislatura Ordinaria 2020",
                "Segunda Legislatura Ordinaria 2017",
                "Primera Legislatura Ordinaria 2019",
                "Segunda Legislatura Ordinaria 2020",
                "Primera Legislatura Ordinaria 2016"]
CorpusLegislaturas = ( [] ,[] ,[] ,[] ,[] ,[] ,[],[],[],[])
'''
Corpus_Total = []
Nombres_Total= []

Corpus_2016 = pd.DataFrame()
Corpus_2017 = pd.DataFrame()
Corpus_2018 = pd.DataFrame()
Corpus_2019 = pd.DataFrame()
Corpus_2020 = pd.DataFrame()
Corpus_2021 = pd.DataFrame()

Corpus_df = pd.DataFrame()

#Corpus_Legislaturas = [pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]

for Nombre in Nombres:
    with open('./Corpus/'+Nombre, 'r') as Txt:
        Texto = Txt.read().split("\n")
        #=========Corpus por Años=========
        #if Texto[0][26:] in Anios:
        #    print()
        #else:
        #    print(Nombre)
        Posicion = Anios.index(Texto[0][-4:])
        CorpusAnios[Posicion].append(Texto[2][20:] + " " + Texto[6][20:])
        NombresAnios[Posicion].append(Nombre)

        #=========Corpus Legislaturas=========
        #if Texto[7][20:] in Legislaturas:
        #    print()
        #else:
        #    print(Nombre)
        '''
        Pos2 = Legislaturas.index(Texto[7][20:])
        CorpusLegislaturas[Pos2].append(Texto[2][20:] + " " + Texto[6][20:])
        NombreLegislaturas[Pos2].append(Nombre)
        '''
        #========Corpus Total=========
        Corpus_Total.append(Texto[2][20:] + " " + Texto[6][20:])
        Nombres_Total.append(Nombre)


#Legislaturas=set(Legislaturas)

#for a in Legislaturas:
#    print(a)
'''
#print(len(Legislaturas))
for i in range(len(Corpus_Legislaturas)-1):
    Corpus_Legislaturas[i]['Codigos']= NombreLegislaturas[i]
    Corpus_Legislaturas[i]['Corpus']= CorpusLegislaturas[i]
'''
Corpus_df['Codigos']=Nombres_Total
Corpus_df['Corpus']=Corpus_Total

print(Corpus_df)

Corpus_2016['Codigos']=NombresAnios[0]
Corpus_2017['Codigos']=NombresAnios[1]
Corpus_2018['Codigos']=NombresAnios[2]
Corpus_2019['Codigos']=NombresAnios[3]
Corpus_2020['Codigos']=NombresAnios[4]
Corpus_2021['Codigos']=NombresAnios[5]

Corpus_2016['Corpus']=CorpusAnios[0]
Corpus_2017['Corpus']=CorpusAnios[1]
Corpus_2018['Corpus']=CorpusAnios[2]
Corpus_2019['Corpus']=CorpusAnios[3]
Corpus_2020['Corpus']=CorpusAnios[4]
Corpus_2021['Corpus']=CorpusAnios[5]

#============
#Tratamiento 1
#============
Limpieza = lambda x: LimpiarCadena(x)
#CorpusLimpio = pd.DataFrame(Corpus_2016.Corpus.apply(Limpieza))
Corpus_2016['Corpus'] = pd.DataFrame(Corpus_2016.Corpus.apply(Limpieza))#No perdemos el nombre
Corpus_2017['Corpus'] = pd.DataFrame(Corpus_2017.Corpus.apply(Limpieza))#No perdemos el nombre
Corpus_2018['Corpus'] = pd.DataFrame(Corpus_2018.Corpus.apply(Limpieza))#No perdemos el nombre
Corpus_2019['Corpus'] = pd.DataFrame(Corpus_2019.Corpus.apply(Limpieza))#No perdemos el nombre
Corpus_2020['Corpus'] = pd.DataFrame(Corpus_2020.Corpus.apply(Limpieza))#No perdemos el nombre
Corpus_2021['Corpus'] = pd.DataFrame(Corpus_2021.Corpus.apply(Limpieza))#No perdemos el nombre
Corpus_df['Corpus'] = pd.DataFrame(Corpus_df.Corpus.apply(Limpieza))
'''
for i in range(len(Corpus_Legislaturas)-1):
    Corpus_Legislaturas[i]['Corpus'] = pd.DataFrame(Corpus_Legislaturas[i].Corpus.apply(Limpieza))
'''
def ExportarCorpus(DirectorioExportacion, Datos,NombreArchivo):
    Contenido = []
    for k in Datos.index:
        Contenido.append(Datos["Codigos"][k] + "\n" + Datos["Corpus"][k]+"\n")
    with open(DirectorioExportacion + NombreArchivo, "w") as output:
        output.writelines(Contenido)


#El directorio de exportacion debe de ser diferente al directorio del corpus principal
DirectorioExp = "./Corpus Procesados/"

#CORPUS POR AÑOS
ExportarCorpus(DirectorioExp, Corpus_2016,"Corpus_2016.txt")
ExportarCorpus(DirectorioExp, Corpus_2017,"Corpus_2017.txt")
ExportarCorpus(DirectorioExp, Corpus_2018,"Corpus_2018.txt")
ExportarCorpus(DirectorioExp, Corpus_2019,"Corpus_2019.txt")
ExportarCorpus(DirectorioExp, Corpus_2020,"Corpus_2020.txt")
ExportarCorpus(DirectorioExp, Corpus_2021,"Corpus_2021.txt")
'''
#CORPUS POR LEGISLATURAS
for i in range(len(Corpus_Legislaturas)-1):
    ExportarCorpus(DirectorioExp, Corpus_Legislaturas[i],"Corpus_"+Legislaturas[i]+".txt")
'''
#CORPUS TOTAL
ExportarCorpus(DirectorioExp, Corpus_df,"Corpus_Tratado.txt")   



