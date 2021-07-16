import base64
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from tempfile import NamedTemporaryFile
import fpdf
from fpdf import FPDF
import scipy
from scipy import stats
from sklearn.neighbors import KernelDensity
import matplotlib.gridspec as grid_spec

import latex




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


if paginaseleciona=='FIG4':

    st.title(paginaseleciona)

    st.write('OBS: O texto no eixo RELAXATION pode ser editado')

    st.write('Espere um pouco, a figura pode demorar a renderizar')

    ynames = ['k',r'$\gamma$',r'$\alpha$','TYPE OF RELAXATION']
    ys=EDIALL[['k','γ','α','CLUSTER']].iloc[:].values
    ymins = ys.min(axis=0)
    ymaxs = ys.max(axis=0)
    dys = ymaxs - ymins
    ymins -= dys * 0.05  # add 5% padding below and above
    ymaxs += dys * 0.05

    ymaxs[1], ymins[1] = ymins[1], ymaxs[1]  # reverse axis 1 to have less crossings
    dys = ymaxs - ymins

    # transform all data to be compatible with the main axis
    zs = np.zeros_like(ys)
    zs[:, 0] = ys[:, 0]
    zs[:, 1:] = (ys[:, 1:] - ymins[1:]) / dys[1:] * dys[0] + ymins[0]

    fig, host = plt.subplots(figsize=(14,7))

    axes = [host] + [host.twinx() for i in range(ys.shape[1] - 1)]
    for i, ax in enumerate(axes):
        ax.set_ylim(ymins[i], ymaxs[i])
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        if ax != host:
            ax.spines['left'].set_visible(False)
            ax.yaxis.set_ticks_position('right')
            ax.spines["right"].set_position(("axes", i / (ys.shape[1] - 1)))


    host.set_xlim(0, ys.shape[1] - 1)
    host.set_xticks(range(ys.shape[1]))
    host.set_xticklabels(ynames, fontsize=30)
    host.tick_params(axis='x', which='major', pad=7)
    host.spines['right'].set_visible(False)
    host.xaxis.tick_top()
    
    #host.set_title('Parallel Coordinates Plot — Iris', fontsize=18, pad=12)

    colors = plt.cm.Pastel1.colors
    legend_handles = [None for _ in ['PL','EXP']]
    for j in range(ys.shape[0]):
        # create bezier curves
        verts = list(zip([x for x in np.linspace(0, len(ys) - 1, len(ys) * 3 - 2, endpoint=True)],
                         np.repeat(zs[j, :], 3)[1:-1]))
        codes = [Path.MOVETO] + [Path.CURVE4 for _ in range(len(verts) - 1)]
        path = Path(verts, codes)
        if EDIALL['CLUSTER'].values[j]==0:
            patch = patches.PathPatch(path, facecolor='none', lw=1.0, alpha=0.05,edgecolor='#1F3C4E'  )#EXP
        else:
            patch = patches.PathPatch(path, facecolor='none', lw=5.0, alpha=0.5,edgecolor='#FAC949' )#PL
        legend_handles[EDIALL['CLUSTER'].values[j]] = patch
        host.add_patch(patch)
    plt.tight_layout()
    st.pyplot(fig)


    export_as_pdf = st.button("Se quiser fazer o download dessa figura")

    if export_as_pdf:
        st.write('ESPERE UM POUCO, JÁ JÁ  O LINK SERÁ CRIADO')
        pdf = FPDF(orientation = 'L', unit = 'in', format=(7,14))
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:

                plt.savefig(tmpfile.name,dpi=300)
                pdf.image(tmpfile.name, 0, 0, 14, 7)
                filename=pdf.output(dest="S").encode("latin-1")
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
        st.markdown(html, unsafe_allow_html=True)


if paginaseleciona=='FIG5':

    st.title(paginaseleciona)
    st.write(r'k=[500,1000] e $\gamma$=[50,100]')

    st.write('Espere um pouco, a figura pode demorar a renderizar')

    fig,ax=plt.subplots(figsize=(10,7))
    ax.set_ylabel(r'P($\alpha$)',fontsize=30)
    ax.set_xlabel(r'$\alpha$',fontsize=30)
    ax.bar(apl,ccPL,width=1.0*(0.05/2),color='#FAC949',label='PL')
    ax.bar(aexp,ccEXP,width=1.0*(0.05/2),color='#1F3C4E',label='EXP')


    x=dfaux[dfaux['CLUSTER']==1]['α'].copy()
    y=dfaux[dfaux['CLUSTER']==0]['α'].copy()
    kdex = stats.gaussian_kde(x,bw_method=0.4)
    kdey = stats.gaussian_kde(y,bw_method=0.2)
    xx = np.linspace(0.5,1.0, 1000)
    yy= np.linspace(0.5,1.0, 1000)
    plt.xticks(np.linspace(0.5,1.0,6),rotation=0,fontsize=30)
    plt.yticks(fontsize=30)
    ax.legend(loc=4,shadow=True,fontsize=30)

    st.pyplot(fig)

    export_as_pdf = st.button("Se quiser fazer o download dessa figura")

    if export_as_pdf:
        st.write('ESPERE UM POUCO, JÁ JÁ  O LINK SERÁ CRIADO')
        pdf = FPDF(orientation = 'L', unit = 'in', format=(7,10))
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:

                plt.savefig(tmpfile.name,dpi=300)
                pdf.image(tmpfile.name, 0, 0, 10, 7)
                filename=pdf.output(dest="S").encode("latin-1")
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
        st.markdown(html, unsafe_allow_html=True)


if paginaseleciona=='FIG3a':

    st.title(paginaseleciona)
    st.write(r'$\chi_{E}$')

    st.write('Espere um pouco, a figura pode demorar a renderizar')


    plt.rcParams.update({'font.size': 40})

    data=EDIALL[(EDIALL['α']==0.5)|(EDIALL['α']==0.6)|(EDIALL['α']==0.7)|(EDIALL['α']==0.8)|(EDIALL['α']==0.9)|(EDIALL['α']==1.0)].copy()
    countries = [x for x in np.unique(data['α'])]
    #countries=[0.5]
    colors = ['#0000ff', '#3300cc', '#660099', '#990066', '#cc0033','#cc0033']

    gs = grid_spec.GridSpec(len(countries),1)
    fig = plt.figure(figsize=(16,9))

    i = 0
    d0=data[data['CLUSTER']==0].copy()
    d1=data[data['CLUSTER']==1].copy()
    ax_objs = []
    for country in countries:
        country = countries[i]
        
        x = np.array(data[data['α'] == country].xE)
        x_d = np.linspace(EDIALL.xE.min(),EDIALL.xE.max(), 1000)

        kde = KernelDensity(bandwidth=10.0, kernel='gaussian')
        kde.fit(x[:, None])

        logprob = kde.score_samples(x_d[:, None])

        # creating new axes object
        ax_objs.append(fig.add_subplot(gs[i:i+1, 0:]))

        # plotting the distribution
        #ax_objs[-1].plot(x_d, np.exp(logprob),color="#f0f0f0",lw=2)
        #ax_objs[-1].fill_between(x_d, np.exp(logprob), alpha=1,color=colors[i])
        
        #d0
        x0=np.array(d0[d0['α'] == country].xE)
        if (len(x0)!=0):
            kde = KernelDensity(bandwidth=10.0, kernel='gaussian')
            kde.fit(x0[:, None])
            logprob = kde.score_samples(x_d[:, None])
            ax_objs[-1].plot(x_d, np.exp(logprob)/np.exp(logprob).max(),color='black',alpha=trans,lw=2)
            ax_objs[-1].fill_between(x_d, np.exp(logprob)/np.exp(logprob).max(), alpha=trans,color=coresC['EXP'])

        #d1
        x1=np.array(d1[d1['α'] == country].xE)
        if (len(x1)!=0):
            kde = KernelDensity(bandwidth=10.0, kernel='gaussian')
            kde.fit(x1[:, None])
            logprob = kde.score_samples(x_d[:, None])
            ax_objs[-1].plot(x_d, np.exp(logprob)/np.exp(logprob).max(),color='orange',alpha=trans,lw=2)
            ax_objs[-1].fill_between(x_d, np.exp(logprob)/np.exp(logprob).max(), alpha=trans,color=coresC['PL'])


        # setting uniform x and y lims
        ax_objs[-1].set_xlim(EDIALL.xE.min(),EDIALL.xE.max())
        ax_objs[-1].set_ylim(0,1.0)

        # make background transparent
        rect = ax_objs[-1].patch
        rect.set_alpha(0)

        # remove borders, axis ticks, and labels
        ax_objs[-1].set_yticklabels([])

        if i == len(countries)-1:
            ax_objs[-1].set_xlabel(r"$\chi_{E}$", fontsize=40,fontweight="bold")
        else:
            ax_objs[-1].set_xticklabels([])

        spines = ["top","right","left","bottom"]
        for s in spines:
            ax_objs[-1].spines[s].set_visible(False)

        #adj_country = country.replace(" ","\n")
        ax_objs[-1].text(-0.02,0,country,fontsize=40,ha="right")


        i += 1

    gs.update(hspace=-0.1)

    #fig.text(0.07,0.85,"Distribution of Aptitude Test Results from 18 – 24 year-olds",fontsize=20)

    plt.tight_layout()
    st.pyplot(fig)

    
    export_as_pdf = st.button("Se quiser fazer o download dessa figura")
    

    if export_as_pdf:
        st.write('ESPERE UM POUCO, JÁ JÁ  O LINK SERÁ CRIADO')
        pdf = FPDF(orientation = 'L', unit = 'in', format=(9,16))
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:

                plt.savefig(tmpfile.name,dpi=300,bbox_inches='tight')
                pdf.image(tmpfile.name, 0, 0, 16, 9)
                filename=pdf.output(dest="S").encode("latin-1")
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
        st.markdown(html, unsafe_allow_html=True)
    


if paginaseleciona=='FIG3b':

    st.title(paginaseleciona)
    st.write(r'$\chi_{P}$')

    st.write('Espere um pouco, a figura pode demorar a renderizar')


    plt.rcParams.update({'font.size': 40})

    data=EDIALL[(EDIALL['α']==0.5)|(EDIALL['α']==0.6)|(EDIALL['α']==0.7)|(EDIALL['α']==0.8)|(EDIALL['α']==0.9)|(EDIALL['α']==1.0)].copy()
    countries = [x for x in np.unique(data['α'])]
    #countries=[0.5]
    colors = ['#0000ff', '#3300cc', '#660099', '#990066', '#cc0033','#cc0033']

    gs = grid_spec.GridSpec(len(countries),1)
    fig = plt.figure(figsize=(16,9))
    
    i = 0
    d0=data[data['CLUSTER']==0].copy()
    d1=data[data['CLUSTER']==1].copy()
    ax_objs = []
    for country in countries:
        country = countries[i]
        
        x = np.array(data[data['α'] == country].xP)
        x_d = np.linspace(EDIALL.xP.min(),6, 1000)

        kde = KernelDensity(bandwidth=1., kernel='gaussian')
        kde.fit(x[:, None])

        logprob = kde.score_samples(x_d[:, None])

        # creating new axes object
        ax_objs.append(fig.add_subplot(gs[i:i+1, 0:]))

        # plotting the distribution
        #ax_objs[-1].plot(x_d, np.exp(logprob),color="#f0f0f0",lw=2)
        #ax_objs[-1].fill_between(x_d, np.exp(logprob), alpha=1,color=colors[i])
        
        #d0
        x0=np.array(d0[d0['α'] == country].xP)
        if (len(x0)!=0):
            kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
            kde.fit(x0[:, None])
            logprob = kde.score_samples(x_d[:, None])
            ax_objs[-1].plot(x_d, np.exp(logprob)/np.exp(logprob).max(),color='black',alpha=trans,lw=2)
            ax_objs[-1].fill_between(x_d, np.exp(logprob)/np.exp(logprob).max(), alpha=trans,color=coresC['EXP'])

        #d1
        x1=np.array(d1[d1['α'] == country].stdP)
        if (len(x1)!=0):
            kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
            kde.fit(x1[:, None])
            logprob = kde.score_samples(x_d[:, None])
            ax_objs[-1].plot(x_d, np.exp(logprob)/np.exp(logprob).max(),color='orange',alpha=trans,lw=2)
            ax_objs[-1].fill_between(x_d, np.exp(logprob)/np.exp(logprob).max(), alpha=trans,color=coresC['PL'])


        # setting uniform x and y lims
        ax_objs[-1].set_xlim(EDIALL.xP.min(),6)
        ax_objs[-1].set_ylim(0,1.0)

        # make background transparent
        rect = ax_objs[-1].patch
        rect.set_alpha(0)

        # remove borders, axis ticks, and labels
        ax_objs[-1].set_yticklabels([])

        if i == len(countries)-1:
            ax_objs[-1].set_xlabel(r"$\chi_{P}$", fontsize=40,fontweight="bold")
        else:
            ax_objs[-1].set_xticklabels([], fontsize=40)

        spines = ["top","right","left","bottom"]
        for s in spines:
            ax_objs[-1].spines[s].set_visible(False)

        #adj_country = country.replace(" ","\n")
        ax_objs[-1].text(-0.02,0,country,fontsize=40,ha="right")


        i += 1

    gs.update(hspace=-0.1)

    

    plt.tight_layout()

    st.pyplot(fig)

    
    export_as_pdf = st.button("Se quiser fazer o download dessa figura")
    

    if export_as_pdf:
        st.write('ESPERE UM POUCO, JÁ JÁ  O LINK SERÁ CRIADO')
        pdf = FPDF(orientation = 'L', unit = 'in', format=(9,16))
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:

                plt.savefig(tmpfile.name,dpi=300,bbox_inches='tight')
                pdf.image(tmpfile.name, 0, 0, 16, 9)
                filename=pdf.output(dest="S").encode("latin-1")
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
        st.markdown(html, unsafe_allow_html=True)


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
    plt.ylabel(r'$\beta $',fontsize=40)
    plt.xticks(x1,squad,fontsize=40)
    plt.xlabel(r'$\alpha $',fontsize=40)
    ax.xaxis.set_tick_params(width=3)
    ax.yaxis.set_tick_params(width=3)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    bp=plt.boxplot(data_to_plot,labels=squad)

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






























