# -*- coding: utf-8 -*-
"""
Created on Fri May  3 15:11:05 2019

@author: vefa
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB


#%% Veriseti okunur
data=pd.read_csv("veritabani_v3.csv")
#%% Maç sonucu tahmini için eğitim ve teste uygun düzenleme yapılır.
data.drop(["MS"],axis=1,inplace=True)
data.drop(["IY"],axis=1,inplace=True)
y=data["MS-Gol"].values
X=data.drop(["MS-Deplasman"],axis=1)
X.drop(["MS-EvSahibi"],axis=1,inplace=True)
X.drop(["IY-EvSahibi"],axis=1,inplace=True)
X.drop(["IY-Deplasman"],axis=1,inplace=True)
X.drop(["Lig"],axis=1,inplace=True)
X.drop(["Ev Sahibi"],axis=1,inplace=True)
X.drop(["Misafir"],axis=1,inplace=True)
X.drop(["MS-Gol"],axis=1,inplace=True)
X.drop(["MS-Sonuc"],axis=1,inplace=True)
X.drop(["IY-Gol"],axis=1,inplace=True)
X.drop(["IY-Sonuc"],axis=1,inplace=True)
X.drop(["KG-Sonuc"],axis=1,inplace=True)
#%% En başarı sınıflandırıcı bulunur ve modelleri kaydedilir
models=[GaussianNB(),
       RandomForestClassifier(n_estimators=100),
       KNeighborsClassifier(n_neighbors=5),
       DecisionTreeClassifier(),
       svm.SVC(kernel='rbf') 
       ]

def best_model_classification(models,y,name,show_metrics=False):
        x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.1,random_state=1)
        print("En iyi Sınıflandırıcı bulunuyor....", end="\n\n")
        best_clf=None
        best_acc=0
        for clf in models:
            clf.fit(x_train, y_train)
            y_pred=clf.predict(x_test)
            acc=metrics.accuracy_score(y_test, y_pred)
            print(clf.__class__.__name__, end=" ")
            print("Başarı oranı:{:.3f}".format(acc))

            if best_acc<acc:
                best_acc=acc
                best_clf=clf
                best_y_pred=y_pred
        
        print("En iyi Sınıfılandırıcı:{}".format(best_clf.__class__.__name__))
        pickle.dump(best_clf, open(name, 'wb'))   
#  Tahminler ve gerçek değerler arası ilişkiler gösterilir.
        if show_metrics:
            mat = confusion_matrix(y_test,best_y_pred)
            sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False   )
            plt.xlabel('true label')
            plt.ylabel('predicted label');
              

#%%
name="MS_gol-tahmin.model"
best_model_classification(models,y,name,show_metrics=True)


#%%IY gol tahmini
name = "IY_gol-tahmin.model"
y=data["IY-Gol"].values
best_model_classification(models,y,name,show_metrics=True)

#%% KG sonucu tahmini
y=data["KG-Sonuc"].values
name = "KG-tahmin.model"
best_model_classification(models,y,name,show_metrics=True)

