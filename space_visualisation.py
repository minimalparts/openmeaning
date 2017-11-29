from flask import render_template, request, jsonify
from sklearn.decomposition import PCA
import logging

from utils import sim_to_matrix, sim_to_matrix_url, readDM, make_figure, readUrls
from htmlparser import extract_from_url
import mk_page_vector
from openviz import app

pca = PCA(n_components=2)
target_word = "meaning"
dm_dict_en = readDM("./openviz/spaces/english.dm")
dm_dict_ca = readDM("./openviz/spaces/catalan.dm")
url_dict_en = readUrls("./openviz/spaces/url_english.csv")
url_dict_ca = readUrls("./openviz/spaces/url_english.csv")

language_codes = {}
language_codes["English"]=[dm_dict_en, url_dict_en, "en"]
language_codes["Catalan"]=[dm_dict_ca, url_dict_ca, "ca"]

def compute(target_word, language):
    error=""
    if language != "":
        dm_dict = language_codes[language][0]
        dictionary = language_codes[language][2]
    else:
        dm_dict = language_codes["English"][0]
        dictionary = language_codes["English"][2]
    logging.exception(language)
    if target_word not in dm_dict:
        target_word="error"
        error="<img src='http://www.openmeaning.org/static/sad-robot.png' width='100%'/><br><b>Sorry, the computer has not learnt this word yet. Try again!</b>"

    neighbours = sim_to_matrix(dm_dict,dm_dict[target_word], 50)

    '''Make figure'''
    m = []
    labels = []
    for n in neighbours[:10]:
        labels.append(n)
        m.append(dm_dict[n])
    pca.fit(m)
    m_2d = pca.transform(m)
    figdata_png = make_figure(m_2d,labels)

    '''Return more neighbours, with dictionary links'''
    neighbour_links = ""
    for n in neighbours:

        new_link="<a href='https://"+dictionary+".wiktionary.org/wiki/"+n+"'/>"+n+"</a> | "
        neighbour_links+=new_link
    return figdata_png, error, neighbour_links


def neighbour_urls(target_url, language):
    error=""
    if language != "":
        dm_dict = language_codes[language][0]
        url_dict = language_codes[language][1]
    else:
        dm_dict = language_codes["English"][0]
        url_dict = language_codes["English"][1]
    logging.exception(language)
    if target_url not in url_dict:
        u, body_str = extract_from_url(target_url)
        u = mk_page_vector.compute(u,body_str,dm_dict)
        url_dict[u.url]=u
    neighbours = sim_to_matrix_url(url_dict,url_dict[target_url].vector, 50)
    logging.exception(neighbours)
    return neighbours

@app.route("/viz/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        img, error, neighbours = compute("paraula","Catalan")
        return render_template("viz/index.html", target=img.decode('utf8'), error=error, neighbours=neighbours, language="English")
    language = request.form["language"]
    target_word = request.form["target_word"].lower()
    img, error, neighbours = compute(target_word, language)
    return render_template("viz/index.html", target=img.decode('utf8'), error=error, neighbours=neighbours, language=language)

@app.route("/urls/", methods=["GET", "POST"])
def url_index():
    if request.method == "GET":
        neighbours = []
        return render_template("urls/index.html", neighbours=neighbours, language="English")
    language = request.form["language"]
    target_url = request.form["target_url"].lower()
    neighbours = neighbour_urls(target_url, language)
    return render_template("urls/index.html", neighbours=neighbours, language=language)


@app.route('/vectors/<word>/')
def return_vector(word):
    v = list(dm_dict_en[word])
    return jsonify(vector=v)
