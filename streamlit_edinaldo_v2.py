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

    st.title(paginaseleciona)
    st.write(r'$\beta$')

    st.write('Espere um pouco, a figura pode demorar a renderizar')


    plt.rcParams.update({'font.size': 40})

    c1aux=EDIALL[EDIALL['CLUSTER']==1].copy()
    data_to_plot=[c1aux[c1aux['α']==0.5]['expP'].values,c1aux[c1aux['α']==0.55]['expP'].values,c1aux[c1aux['α']==0.6]['expP'].values,c1aux[c1aux['α']==0.65]['expP'].values]
   
    fig,ax=plt.subplots(figsize=(10,7))
    x1 = [1,2,3,4]
    squad = [0.50,0.55,0.60,0.65]
    plt.ylabel(r'$\beta$',fontsize=40)
    plt.xticks(x1,squad,fontsize=40)
    plt.xlabel(r'$\alpha$',fontsize=40)
    ax.xaxis.set_tick_params(width=3)
    ax.yaxis.set_tick_params(width=3)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    bp=plt.boxplot(data_to_plot,labels=squad)
    plt.plot([1,2,3],[10,20,30])
    st.pyplot(fig)

    
    export_as_pdf = st.button("Se quiser fazer o download dessa figura")
    

    if export_as_pdf:
        st.write('ESPERE UM POUCO, JÁ JÁ  O LINK SERÁ CRIADO')
        pdf = FPDF(orientation = 'L', unit = 'in', format=(7,10))
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:

                plt.savefig(tmpfile.name,dpi=300,bbox_inches='tight')
                pdf.image(tmpfile.name, 0, 0, 10, 7)
                filename=pdf.output(dest="S").encode("latin-1")
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
        st.markdown(html, unsafe_allow_html=True)






























