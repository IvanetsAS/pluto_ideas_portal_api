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
        corpus_length += len([lose_non_russian_alphabet(token).lower() for token in word_tokenize(text)
                              if lose_non_russian_alphabet(token)])
    return corpus_length / len(texts)


def compute_idf(request, texts):
    request = {lose_non_russian_alphabet(token).lower() for token in word_tokenize(request)
               if lose_non_russian_alphabet(token)}

    count = {}
    for text in texts:
        text = [lose_non_russian_alphabet(token).lower() for token in word_tokenize(text)
                if lose_non_russian_alphabet(token)]
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
    stop_words = set(stopwords.words('russian'))
    request = []
    for token in word_tokenize(check_object['user_text']):
        token = lose_non_russian_alphabet(token).lower()
        if token and token not in stop_words:
            request.append(token)

    document = []
    for token in word_tokenize(check_object['idea_text']):
        token = lose_non_russian_alphabet(token).lower()
        if token and token not in stop_words:
            document.append(token)

    freq_dict = compute_frequency_dictionary(request, document)

    relevance = 0
    for word in request:
        relevance += IDF[word] * (freq_dict[word] * 3) / (freq_dict[word] + 2 * (0.25 + 0.75 * len(document) / AVGDL))
    return check_object['group_id'], check_object['idea_id'], relevance, check_object['idea_text']


def get_relevance_list(user_text, ideas_path):
    # user_text = sys.argv[1]
    # ideas_path = sys.argv[2]

    user_text = "Мне не хватает общения, поговорите со мной!"
    ideas_path = "../../data/data.json"
    with open(ideas_path, encoding='UTF-8') as file:
        groups = json.load(file)

    server_texts = []
    for group in groups:
        server_texts += [
            {'group_id': group['group_id'], 'idea_id': idea['id'], 'idea_text': idea['text'], 'user_text': user_text}
            for idea in group['ideas']]
    AVGDL = compute_avgdl([text['idea_text'] for text in server_texts])
    IDF = compute_idf(user_text, [text['idea_text'] for text in server_texts])

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
