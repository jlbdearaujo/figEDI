
import base64
import streamlit as st
import pandas as pd
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches
from tempfile import NamedTemporaryFile
import fpdf
from fpdf import FPDF
import scipy
from scipy import stats
from sklearn.neighbors import KernelDensity
import matplotlib.gridspec as grid_spec
import matplotlib.pyplot as plt


EDIALL=pd.read_csv('EDIALL_old.csv',sep=';')


st.sidebar.title('FIGURAS DO CLAÚDIO LUCAS')
st.sidebar.write('Jorge Luiz')

listaclasse=['NENHUMA','FIG3a','FIG3b','FIG4','FIG5','FIG6']
paginaseleciona=st.sidebar.selectbox('Selecione a figura que deseja visualizar',listaclasse)

corpl=st.sidebar.text_input("Coloque sua cor em hexadecimal para o PL")
corexp=st.sidebar.text_input("Coloque sua cor em hexadecimal para o EXP")
st.sidebar.write('Se as cores não forem escolhidas, os padrões serão adotadas por mim :)')

trans = st.sidebar.slider('Nível de transparência', 0.0, 1.0, 0.5)

st.sidebar.write('O nível de transparência ajuda a ver o comportameto das figuras 3a e 3b')




if corpl=='':
    corpl='#FAC949'
if corexp=='':
    corexp='#1F3C4E'

coresC={'PL':corpl,'EXP':corexp}

if paginaseleciona=='NENHUMA':
    st.title('NENHUMA FIGURA FOI SELECIONADA')

    st.write(" Por favor, selecione no menu ao lado a figura que queira editar e suas respectivas cores.")



if paginaseleciona=='FIG6':

  
    fig,ax=plt.subplots(figsize=(10,7))
   
    df=pd.DataFrame({'A':[1,2,3],'B':[10,20,30]})
    ax.plot(df.A,df.B)
    st.pyplot(fig)

    






























