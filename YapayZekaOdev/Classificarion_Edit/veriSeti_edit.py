# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 18:07:50 2019

@author: Ugur
"""

import pandas as pd
import numpy as np

#%% data değişkenine siteden çekilen excel dosyası arayüz ile import edilir
# Daha önceden oluşturulmuş verisetine ek veriler eklenir.
data = veri_ekcsv[veri_ekcsv.Lig.notnull()]
data = data[(data.IY!='ERT') & (data.IY!=' ')& (data.IY!='Yrdk.')]

#%%
#İlk yarı ve maç sonu golleri ayrı bir özellik olarak eklenir.
data["IY-EvSahibi"]=[(each).split(" ")[0] for each in data["IY"]]
data["IY-Deplasman"]=[(each).split(" ")[3] for each in data["IY"]]
data["MS-EvSahibi"]=[(each).split(" ")[0] for each in data["MS"]]
data["MS-Deplasman"]=[(each).split(" ")[3] for each in data["MS"]]
#%%Veri steindeki handikak bölümünü içeren özellikler çıkartılır 
data.drop("h", axis=1, inplace=True)
data.drop("h.1", axis=1, inplace=True)

#%% Boş değerlere 1 değeri atanır ve tüm değerler floata çevrilir.
data.fillna(" ")
data = data.replace({' ':"1.0"})
data = data.apply(pd.to_numeric, errors='ignore')

#%% Daha sonra eğitim için gereken sonuç durumları veriSetine eklenir.
data.loc[data["MS-EvSahibi"] < data["MS-Deplasman"], 'MS-Sonuc'] = 2
data.loc[data["MS-EvSahibi"] == data["MS-Deplasman"], 'MS-Sonuc'] = 0
data.loc[data["MS-EvSahibi"] > data["MS-Deplasman"], 'MS-Sonuc'] = 1
data.loc[data["MS-EvSahibi"]+ data["MS-Deplasman"] < 3, 'MS-Gol'] = 0
data.loc[data["MS-EvSahibi"]+ data["MS-Deplasman"] >= 3, 'MS-Gol'] = 1
data.loc[data["IY-EvSahibi"] < data["IY-Deplasman"], 'IY-Sonuc'] = 2
data.loc[data["IY-EvSahibi"] == data["IY-Deplasman"], 'IY-Sonuc'] = 0
data.loc[data["IY-EvSahibi"] > data["IY-Deplasman"], 'IY-Sonuc'] = 1
data.loc[data["IY-EvSahibi"]+ data["IY-Deplasman"] < 2, 'IY-Gol'] = 0
data.loc[data["IY-EvSahibi"]+ data["IY-Deplasman"] >= 2, 'IY-Gol'] = 1
data.loc[(data["MS-EvSahibi"] >0)  & (data["MS-Deplasman"] >0 ) , 'KG-Sonuc'] = 1
data.loc[(data["MS-EvSahibi"] == 0) |  (data["MS-Deplasman"] == 0) ,'KG-Sonuc'] = 0

#%% önceki verieti okunur ve ek veriseti ile birleştirilir.
data2=pd.read_csv("veritabani_v3.csv")
data3 = pd.concat([data,data2],sort=False, ignore_index=True)
data3.to_csv("veritabani_v3.csv",index=False)

#%%
import matplotlib.pyplot as plt
import seaborn as sns
#data3=pd.read_csv("veritabani_v3.csv")
sns.countplot(data3["IY-Sonuc"])
plt.title("IY-Sonuc",color="green")
plt.show()



