
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

plt.rcParams.update({'font.size': 22})
plt.rc('font',**{'family':'serif','serif':['Times']})
plt.rc('font',**{'family':'serif','serif':['Times']})
plt.rc('text', usetex=True)

EDIALL=EDIALL.astype({'CLUSTER':'int64'})

EDIALL.drop('Unnamed: 0',axis=1,inplace=True)
alfas=EDIALL['α'].value_counts().sort_index().index.values.copy()

dfaux=EDIALL[(EDIALL['k']>500)&(EDIALL['γ']>50)].copy()

ccPL=[];ccEXP=[];apl=[];aexp=[]
for a in alfas:
    c1=len(dfaux[(dfaux['CLUSTER']==1)&(dfaux['α']==a)])
    c0=len(dfaux[(dfaux['CLUSTER']==0)&(dfaux['α']==a)])
    ct=c1+c0
    ccEXP.append(c0/ct)
    ccPL.append(c1/ct)
    apl.append(a-(0.05/4))
    aexp.append(a+(0.05/4))


if corpl=='':
    corpl='#FAC949'
if corexp=='':
    corexp='#1F3C4E'

coresC={'PL':corpl,'EXP':corexp}

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Arroxe no download!!!</a>'

if paginaseleciona=='NENHUMA':
    st.title('NENHUMA FIGURA FOI SELECIONADA')

    st.write(" Por favor, selecione no menu ao lado a figura que queira editar e suas respectivas cores.")



if paginaseleciona=='FIG6':

  
    fig,ax=plt.subplots(figsize=(10,7))
   
    df=pd.DataFrame({'A':[1,2,3],'B':[10,20,30]})
    ax.plot(df.A,df.B)
    st.pyplot(fig)
































