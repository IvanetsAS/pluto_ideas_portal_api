import json
import re

from navec import Navec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def lose_non_russian_alphabet(text):
    return re.sub('[^а-яА-ЯёЁ]', '', text)


def get_token_list(text, stop_words):
    document = []
    for token in word_tokenize(text):
        token = lose_non_russian_alphabet(token).lower()
        if token and token not in stop_words:
            document.append(token)
    return document


def compute_text_vector(text, vector_dict):
    pass


def compute_text_distance(srt, vector, vector_dict):
    text_vector = compute_text_vector(srt['idea_text'], vector_dict)


def get_relevance_list(user_text, ideas_path, vector_dict):
    with open(ideas_path, encoding='UTF-8') as file:
        groups = json.load(file)

    stop_words = set(stopwords.words('russian'))
    request = get_token_list(user_text, stop_words)

    server_texts = []
    for group in groups:
        for idea in group['ideas']:
            document = get_token_list(idea['text'], stop_words)
            server_texts.append(
                {'group_id': group['group_id'], 'idea_id': idea['id'], 'idea_text': document})

    request_vector = compute_text_vector(request, vector_dict)
    result = []
    for srt in server_texts:
        result.append(compute_text_distance(srt, request_vector, vector_dict))
    result.sort(key=lambda x: x[2], reverse=True)
    for res in result[0:5]:
        print(res)

    return result


navec = Navec.load("../../data/navec_hudlit_v1_12B_500K_300d_100q.tar")
get_relevance_list("Мне не хватает общения, поговорите со мной!", "../../data/data.json", navec)
