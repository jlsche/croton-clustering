# coding: utf-8

from config import *

import re
import emoji
import jieba
import requests
import pandas as pd
from pathlib import Path

class Preprocess:
    """
    """
    def __init__(self, task, role_filepath):
        self.initialize(task, role_filepath)

    def initialize(self, task, role_filepath):
        if Path(role_filepath).exists():
            jieba.load_userdict(role_filepath)
        else:
            print('No role file')

    def fit(self, df, roles, stopwords):
        df.text = df.text.apply(remove_star_score)
        df.text = df.text.apply(remove_punctuations, args=(punctuations, ))
        df['tokens'] = df.text.apply(tokenize)
        df['ns_tokens'] = df.tokens.apply(remove_stopwords, args=(stopwords, ))
        df.ns_tokens = df.ns_tokens.apply(remove_emoji)

        # 由相同詞彙組成的句子(無論順序)視為相同的句子
        df['unique_text'] = df.ns_tokens.apply(lambda _list: ' '.join(set(_list)))
        # 是否應該刪除重複的句子
        #duplicate_text_indexes = get_duplicate_index(df.unique_text)
        vocab_indice = build_vocab(df.ns_tokens)
        # 將句子改以詞彙編號表示
        df['text_in_ids'] = df.ns_tokens.apply(text_to_id, args=(vocab_indice, ))

        df['length'] = df.ns_tokens.str.len()
        df = df.sort_values(by=['text_in_ids', 'length'])

        df['role'] = df.ns_tokens.apply(get_role, args=(roles, ))
        df.ns_tokens = df.ns_tokens.apply(lambda _list: ' '.join(_list))
        self.df = df[['source', 'ns_tokens', 'role']]
        return self


    

def preprocess(task, save_path): 
    print('\nReading raw files...', flush=True)
    rawdata_url = '{}/{}/{}'.format(data_baseurl, task, raw_filename)
    role_url = '{}/{}/{}'.format(data_baseurl, task, role_filename)
    pov_url = '{}/{}/{}'.format(data_baseurl, task, pov_filename)

    role_filepath = '{}/{}'.format(save_path, role_filename) 
    pov_filepath = '{}/{}'.format(save_path, pov_filename) 

    # copy files to ./data
    resp = requests.get(role_url)
    if resp.status_code == 200:
        with open(role_filepath, 'wb') as handle:
            handle.write(resp.content)
    else:
        print('Error reading role.csv. Please make sure there is one.')

    resp = requests.get(pov_url)
    if resp.status_code == 200:
        with open(pov_filepath, 'wb') as handle:
            handle.write(resp.content)
    else:
        print('Error reading pov.csv. Please make sure there is one.')

    df = read_raw(rawdata_url)
    roles = read_role(role_filepath)
    stopwords = pd.read_csv(stopwords_filepath, names=['stopwords'], squeeze=True, encoding='utf-8')
    print('Done reading all source files.', flush=True)

    print('Preprocessing data...', flush=True)
    handler = Preprocess(task, role_filepath)
    handler.fit(df, roles, stopwords)
    print('Done preprocessing.', flush=True)
    return handler.df


def read_role(path):
    try:
        roles = pd.read_csv(path, names=['role'], squeeze=True, encoding='utf-8').tolist()
        roles = [x[:-4] for x in roles]
    except:
        roles = []
    finally:
        return roles

def read_raw(path): 
    df = pd.read_table(path, sep=',', encoding='utf-8')
    df = df.loc[:, ['text']]
    df['source'] = df.text.iloc[:]
    df = df[:6000]
    return df

def tokenize(text):
    return jieba.lcut(text)
    
def remove_punctuations(text, punctuations):
    """ Remove punctuations, numbers and English letters from text.
        
        Input:
            text: comment, str.
        Returns:
            _: processed text, str.
    """
    text = text.replace("\n", "").replace("\r", "")
    no_punc = text.translate(str.maketrans(punctuations, ' ' * len(punctuations)))
    return re.sub('[ a-zA-Z0-9]', '', no_punc)

def remove_emoji(tokens):
    return [x for x in tokens if x not in emoji.UNICODE_EMOJI]

def remove_stopwords(tokens, stopwords):
    return [x for x in tokens if x not in stopwords]

def remove_star_score(text):
    return text.replace('[星星]', '').replace('[半星]', '')

def get_role(tokens, roles):
    """ Get roles appear in text. 
        
        Input:
            tokens: tokenized text, list.
            roles: character names, list.
        Returns:
            _: role name (or multiple, zero), str.
    """
    role_appear = [role in tokens for role in roles]
    role_count = role_appear.count(True)

    if role_count == 0:
        return 'zero'
    elif role_count == 1:
        index = role_appear.index(True)
        return roles[index]
    else:
        return 'multiple'

def build_vocab(corpus):
    from collections import Counter
    vocabs_count = Counter([word for text in corpus for word in text])
    vocab_indice = {word: idx for idx, (word, _) in enumerate(vocabs_count.most_common())}
    return vocab_indice

def text_to_id(tokens, vocab_indice):
    int_tokens = [vocab_indice[x] for x in tokens]
    return ' '.join(str(x) for x in sorted(set(int_tokens)))



