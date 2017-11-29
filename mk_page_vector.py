""" Make page representation as the WEIGHTED sum of the most 'important'
words in the page (obtained via entropy calculation)
"""

import re
import numpy as np
from utils import normalise, cosine_similarity, convert_to_array

num_dimensions = 400

stopwords = ["", "(", ")", "a", "about", "an", "and", "are", "around", "as", "at", "away", "be", "become", "became",
             "been", "being", "by", "did", "do", "does", "during", "each", "for", "from", "get", "have", "has", "had",
             "he", "her", "his", "how", "i", "if", "in", "is", "it", "its", "made", "make", "many", "most", "not", "of",
             "on", "or", "s", "she", "some", "that", "the", "their", "there", "this", "these", "those", "to", "under",
             "was", "were", "what", "when", "where", "which", "who", "will", "with", "you", "your"]


def compute_text_vector(title,text,dm_dict):
    vbase = np.zeros(num_dimensions)
    text = title+" "+text
    text = re.findall(r"[\w']+|[.,!?;']", text.lower())
    for w in text:
        if w not in stopwords and w in dm_dict:
             vbase+=dm_dict[w]
    return vbase

def compute(u,body,dm_dict):
    s = compute_text_vector(u.title,body, dm_dict)
    u.vector = s
    return u

