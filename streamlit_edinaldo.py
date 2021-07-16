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




if paginaseleciona=='FIG6':

    st.title(paginaseleciona)
   
    st.write('Espere um pouco, a figura pode demorar a renderizar')


    #plt.rcParams.update({'font.size': 40})

    #c1aux=EDIALL[EDIALL['CLUSTER']==1].copy()
    #data_to_plot=[c1aux[c1aux['α']==0.5]['expP'].values,c1aux[c1aux['α']==0.55]['expP'].values,c1aux[c1aux['α']==0.6]['expP'].values,c1aux[c1aux['α']==0.65]['expP'].values]
   
    fig,ax=plt.subplots(figsize=(10,7))
    x1 = [1,2,3,4]
    squad = [0.50,0.55,0.60,0.65]
    plt.ylabel(r'$\beta$',fontsize=40)
    #plt.xticks(x1,squad,fontsize=40)
    plt.xlabel(r'$\alpha$',fontsize=40)
    ax.xaxis.set_tick_params(width=3)
    ax.yaxis.set_tick_params(width=3)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    #bp=plt.boxplot(data_to_plot,labels=squad)
    plt.plot([1,2,3,4],[10,20,30,40])
    st.pyplot(fig)

    

   






























