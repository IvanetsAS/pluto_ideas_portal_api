import json
import math
import re

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

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
    return check_object['group_id'], check_object['idea_id'], relevance


def preprocess_sentence(sentence, stop_words, predictor):
    words = []
    for word in word_tokenize(sentence):
        token = lose_non_russian_alphabet(word).lower()
        if token and token not in stop_words:
            words.append(token)

    return [predictor.parse(word)[0].normal_form for word in words]


def get_tags(text, predictor):
    tags = []
    for word in word_tokenize(text):
        token = predictor.parse(lose_non_russian_alphabet(word).lower())[0]
        if str(token.tag).split(',')[0] == 'NOUN':
            tags.append(token.normal_form)
    return tags


def get_relevance_list(user_text, groups, predictor):
    global AVGDL
    global IDF

    stop_words = set(stopwords.words('russian'))

    request = []
    for sentence in sent_tokenize(user_text):
        lemms = preprocess_sentence(sentence, stop_words, predictor)
        if lemms:
            request += lemms

    tags = get_tags(user_text, predictor)

    server_texts = []
    for group in groups:
        for idea in group['ideas']:
            document = []
            for sentence in sent_tokenize(idea['text']):
                lemms = preprocess_sentence(sentence, stop_words, predictor)
                if lemms:
                    document += lemms

            server_texts.append(
                {'group_id': group['id'], 'idea_id': idea['id'], 'idea_text': document, 'user_text': request})

    AVGDL = compute_avgdl([text['idea_text'] for text in server_texts])
    IDF = compute_idf(request, [text['idea_text'] for text in server_texts])

    result = []
    for srt in server_texts:
        result.append(compute_relevance(srt))

    return result, tags


# with open("../../data/data.json", encoding='UTF-8') as file:
#     ideas = json.load(file)
# get_relevance_list("Музыка должна быть лучше!", ideas, MorphAnalyzer())
