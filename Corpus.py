from bs4 import BeautifulSoup
from bs4.element import Declaration
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import pandas as pd
from datetime import date
import time
import re

ubicacion = '.\chromedriver.exe'
 #Ruta del driver
driver = webdriver.Chrome(executable_path=ubicacion)

home_link = "https://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2016.nsf/Local%20Por%20Numero%20Inverso?OpenView"
driver.get(home_link)

texto = []
pg_amount = 2
base = "https://www2.congreso.gob.pe"
count = 0
num = 1
page = BeautifulSoup(driver.page_source,'html.parser')
tables = page.find_all("table")
for i in range(1, pg_amount+1):    
    for row in tables[2].findAll("tr"):
        cells = row.find_all('td')
        texto.clear()
        for cell in cells:
            if(cell.find('a')):
                a = cell.find('a')
                url = a.attrs['href']
                texto.append(url)
            if(cell.text!=''):
                texto.append(cell.text)   
        if(texto!=[]):
            driver.get(base+str(texto[0]))
            page = BeautifulSoup(driver.page_source,'html.parser')
            Inputs = page.find_all("input")
            Titulo = ""
            Descripcion = ""
            Completo = 0
            for Input in Inputs:
                Input = str(Input)
                if Input.__contains__('<input name="TitIni"'):
                    Titulo=Input[42:-3]
                    Completo+=1
                elif Input.__contains__('<input name="SumIni"'):
                    Descripcion=Input[42:-3]
                    Completo+=1
                if(Completo == 2):
                    break
            #print("Titulo: "+ Titulo)
            #print(Descripcion)
            textito = texto[1].split("/")
            Archivo = open("./Corpus/"+textito[0]+"-"+textito[1]+".txt","w")
            Archivo.write(Titulo+"\n"+Descripcion)
            Archivo.close
            #print("====================")
        #print(texto) 
    time.sleep(4)
    home_link = "https://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2016.nsf/Local%20Por%20Numero%20Inverso?OpenView"
    driver.get(home_link)
    for i in range(0,i):
        next_btn = driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/p/table/tbody/tr/td[3]/a') 
        next_btn.click()   
    page = BeautifulSoup(driver.page_source,'html.parser')
    tables = page.find_all("table")
    #print(page)
print(count)
