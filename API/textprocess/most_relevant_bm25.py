import json
import math
import re
import sys
from multiprocessing.pool import Pool

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

AVGDL = 0
IDF = {}


def lose_non_russian_alphabet(text):
    return re.sub('[^а-яА-ЯёЁ]', '', text)


def compute_frequency_dictionary(request, document):
    count = {}
    for word in document:
        if word in request:
            if word in count:
                count[word] += 1
            else:
                count[word] = 1

    for word in request:
        if word not in count:
            count[word] = 0

    return {word: c / len(document) for word, c in count.items()}


def compute_avgdl(texts):
    corpus_length = 0
    for text in texts:
        corpus_length += len(text)
    return corpus_length / len(texts)


def compute_idf(request, texts):
    count = {}
    for text in texts:
        for word in request:
            if word in text:
                if word in count:
                    count[word] += 1
                else:
                    count[word] = 1

    for word in request:
        if word not in count:
            count[word] = 0
        else:
            count[word] = math.log2(len(texts) / count[word])

    return count


def compute_relevance(check_object):
    freq_dict = compute_frequency_dictionary(check_object['user_text'], check_object['idea_text'])
    relevance = 0
    for word in check_object['user_text']:
        relevance += IDF[word] * (freq_dict[word] * 3) / (
                    freq_dict[word] + 2 * (0.25 + 0.75 * len(check_object['idea_text']) / AVGDL))
    return check_object['group_id'], check_object['idea_id'], relevance, check_object['idea_text']


def get_relevance_list(user_text, ideas_path):
    global AVGDL
    global IDF

    with open(ideas_path, encoding='UTF-8') as file:
        groups = json.load(file)

    stop_words = set(stopwords.words('russian'))
    request = []
    for token in word_tokenize(user_text):
        token = lose_non_russian_alphabet(token).lower()
        if token and token not in stop_words:
            request.append(token)

    server_texts = []
    for group in groups:
        for idea in group['ideas']:
            document = []
            for token in word_tokenize(idea['text']):
                token = lose_non_russian_alphabet(token).lower()
                if token and token not in stop_words:
                    document.append(token)

            server_texts.append(
                {'group_id': group['group_id'], 'idea_id': idea['id'], 'idea_text': document, 'user_text': request})

    AVGDL = compute_avgdl([text['idea_text'] for text in server_texts])
    IDF = compute_idf(request, [text['idea_text'] for text in server_texts])

    result = []
    for srt in server_texts:
        result.append(compute_relevance(srt))
    result.sort(key=lambda x: x[2], reverse=True)
    for res in result[0:5]:
        print(res)

    # with Pool() as pool:
    #     result = pool.map(compute_relevance, server_texts)
    #     result.sort(key=lambda x: x[1])
    #
    #     for res in result[:5]:
    #         print(res)

    return result


get_relevance_list("Мне не хватает общения, поговорите со мной!", "../../data/data.json")
