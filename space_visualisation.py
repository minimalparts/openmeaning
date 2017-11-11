from flask import render_template, request, jsonify
from sklearn.decomposition import PCA
import logging

from utils import sim_to_matrix, get_db_vector, readDM, make_figure
from openviz import app

pca = PCA(n_components=2)
target_word = "meaning"
dm_dict = readDM("./openviz/spaces/catalan.dm")

def compute(target_word):
    error=""

    if target_word not in dm_dict:
        target_word="error"
        error="<img src='static/sad-robot.png' width='100%'/><br><b>Sorry, the computer has not learnt this word yet. Try again!</b>"

    neighbours = sim_to_matrix(dm_dict,target_word, 50)

    '''Make figure'''
    m = []
    labels = []
    for n in neighbours[:10]:
        labels.append(n)
        m.append(get_db_vector(n))
    pca.fit(m)
    m_2d = pca.transform(m)
    figdata_png = make_figure(m_2d,labels)

    '''Return more neighbours, with dictionary links'''
    neighbour_links = ""
    for n in neighbours:
        new_link="<a href='https://ca.wiktionary.org/wiki/"+n+"'/>"+n+"</a> | "
        neighbour_links+=new_link
    return figdata_png, error, neighbour_links

@app.route("/viz/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        img, error, neighbours = compute("paraula")
        return render_template("viz/index.html", target=img.decode('utf8'), error=error, neighbours=neighbours)
    target_word = request.form["target_word"].lower()
    img, error, neighbours = compute(target_word)
    return render_template("viz/index.html", target=img.decode('utf8'), error=error, neighbours=neighbours)

@app.route('/vectors/<word>/')
def return_vector(word):
    v = list(dm_dict[word])
    return jsonify(vector=v)
