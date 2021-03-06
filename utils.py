from math import sqrt
import numpy as np
from models import Catalan, Url
from matplotlib import cm
import pandas as pd
import logging

def readDM(dm_file):
    dm_dict = {}
    with open(dm_file) as f:
        dmlines=f.readlines()
    f.close()

    #Make dictionary with key=row, value=vector
    for l in dmlines:
        items=l.rstrip().split()
        row=items[0]
        vec=[float(i) for i in items[1:]]
        vec=np.array(vec)
        dm_dict[row]=vec
    return dm_dict

def readUrls(url_file):
    urls = {}
    f = open(url_file,'r')
    for l in f:
        l=l.rstrip('\n').split(',')
        if len(l) == 6:
            u = Url(id=l[0],url=l[1],title=l[2],freqs=l[3],vector=convert_to_array(l[4]),snippet=l[5])
            urls[u.url]=u
    f.close()
    return urls

def normalise(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def convert_to_array(vector):
      return np.array([float(i) for i in vector.split(' ')])


def get_db_vector(word):
    '''For DB version.'''
    word_db = Catalan.query.filter(Catalan.word == word).first().vector
    return convert_to_array(word_db)

def cosine_similarity(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Vectors must be of same length")
    num = np.dot(v1, v2)
    den_a = np.dot(v1, v1)
    den_b = np.dot(v2, v2)
    return num / (sqrt(den_a) * sqrt(den_b))

def sim_to_matrix(dm_dict,vec,n):
    cosines={}
    c=0
    for k,v in dm_dict.items():
        try:
            cos = cosine_similarity(vec, v)
            cosines[k]=cos
            c+=1
        except:
            pass
    c=0
    neighbours = []
    for t in sorted(cosines, key=cosines.get, reverse=True):
        if c<n:
            if t.isalpha():
                print(t,cosines[t])
                neighbours.append(t)
                c+=1
        else:
            break
    return neighbours

def sim_to_matrix_url(url_dict,vec,n):
    cosines={}
    for k,v in url_dict.items():
        logging.exception(v.url)
        try:
            cos = cosine_similarity(vec, v.vector)
            cosines[k]=cos
        except:
            pass
    c=0
    neighbours = []
    for t in sorted(cosines, key=cosines.get, reverse=True):
        if c<n:
            #print(t,cosines[t])
            neighbour = [t,url_dict[t].title,url_dict[t].snippet]
            neighbours.append(neighbour)
            c+=1
        else:
            break
    return neighbours

def make_figure(m_2d, labels):
    cmap = cm.get_cmap('nipy_spectral')

    existing_m_2d = pd.DataFrame(m_2d)
    existing_m_2d.index = labels
    existing_m_2d.columns = ['PC1','PC2']
    existing_m_2d.head()

    ax = existing_m_2d.plot(kind='scatter', x='PC2', y='PC1', figsize=(10,6), c=range(len(existing_m_2d)), colormap=cmap, linewidth=0, legend=False)
    ax.set_xlabel("A dimension of meaning")
    ax.set_ylabel("Another dimension of meaning")

    for i, word in enumerate(existing_m_2d.index):
        logging.exception(word+" "+str(existing_m_2d.iloc[i].PC2)+" "+str(existing_m_2d.iloc[i].PC1))
        ax.annotate(
            word,
            (existing_m_2d.iloc[i].PC2, existing_m_2d.iloc[i].PC1), color='black', size='large', textcoords='offset points')

    fig = ax.get_figure()
    cax = fig.get_axes()[1]
    cax.set_visible(False)

    from io import BytesIO
    figfile = BytesIO()
    fig.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    import base64
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png
