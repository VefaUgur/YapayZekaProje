# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Arayüz için erişilecek fonksiyon tanımlanır.
# deneme değişkenin internetten çekilen oranlar ile oluşturulur.
def skorTahmin(deneme):
    
    import numpy as np 
    import pandas as pd
    import pickle
        
    deneme=np.array(deneme)
#önceden hazırlanan sınıflandırma modelleri yuklenir. 
    Ms_tahmin = pickle.load(open("MS-tahmin.model", 'rb'))
    Iy_tahmin = pickle.load(open("IY-tahmin.model", 'rb'))
    Iy_gol_tahmin = pickle.load(open("IY_gol-tahmin.model", 'rb'))
    MS_gol_tahmin = pickle.load(open("MS_gol-tahmin.model", 'rb'))
    KG_tahmin = pickle.load(open("KG-tahmin.model", 'rb'))

#deneme ile modellerde tahminler üretilir.    
    MS=Ms_tahmin.predict(deneme)
    Iy=Iy_tahmin.predict(deneme)
    MS_gol=MS_gol_tahmin.predict(deneme)
    KG=KG_tahmin.predict(deneme)
    IY_gol=Iy_gol_tahmin.predict(deneme)   

#Tahmin edilen değerlerin birleştirmesiyle sistem olası skor tahminlerinin çıkarımını yapar.    
    if(MS_gol==0):
        if(KG==1):
            if(MS == 1 ):
                Skor="2-1"
            elif(MS==0):
                Skor="1-1"
            elif(MS==2): Skor = "2-1"
        elif(KG==0): 
            if(MS==1):
                Skor="1-0 / 2-0"    
            elif (MS==0):
                Skor="0-0"
            elif(MS==2) : Skor="0-1 / 0-2"    
    else :
        if(KG==1):
            if(MS == 1 ):
                Skor="2-1 / 3-1  / 3-2"
            elif (MS==0):
                Skor="2-2"
            elif(MS==2):
                Skor = "1-2 / 1-3 / 2-3"
        elif(KG==0): 
            if(MS==1):
                Skor="3-0 / 4-0"    
            elif (MS==0):
                Skor="0-0"
            elif(MS==2) :Skor="0-3 / 0-4" 
        
    if(MS_gol ==0 ): MS_gol = "Alt"
    else : MS_gol = "Üst"     
    
    if(KG ==0 ): KG = "KG yok"
    else : KG = "KG var"  
    
    if(MS ==0 ): MS = "Berabere"
    elif(MS ==1) : MS = "Ev Sahibi"  
    else: MS="Deplasman"
#Arayüzde gösterilmek üzere değişkenler return edilir.
    return MS,MS_gol,KG,Skor         