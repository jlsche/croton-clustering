# coding: utf-8

import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from lib.http_logger import Log
from config import *

#logger = Log(__name__, './log_pic.txt').logger
#logger = Log(__name__, log_host, log_url).logger

def pic(F, eps, max_iter=1000):

    def fit(F):
        FF = np.dot(F, F.T)
        d = np.dot(FF, np.ones(F.shape[0]))
        D = np.diag(d)
        inv_D = np.matrix(D).I
        N = np.diag(1.0 / np.sqrt(np.diag(FF)))
        return inv_D, N

    def init_vector(F):
        FF = np.dot(F, F.T)
        size = FF.shape[0]
        ones_vec = np.matrix(np.ones(size)).T   
        vector = np.dot(FF, ones_vec)
        normalized_vector = vector / np.sum(vector)       
        return normalized_vector, size

    def project(vector, F, N, inv_D):
        p1 = np.dot(N, vector)
        p2 = np.dot(F.T, p1)
        p3 = np.dot(F, p2)
        p4 = np.dot(N, p3)
        p5 = np.dot(inv_D, p4)
        return p5
    
    def delta(vector1, vector2):
        return np.sum(np.fabs(vector2 - vector1))

    def normalize(vector):
        max_val = vector.max()
        min_val = vector.min()
        if max_val == min_val:
            # case that elements of input F are all the same
            return vector
        else:
            return (vector - min_val) / (max_val - min_val)

    inv_D, N = fit(F) 
    _vec, size = init_vector(F)
    for i in range(max_iter):
        if (i + 1 % 100) == 0:
            pass
            #logger.info('Iteration {}'.format(i))
            pass
        _vec2 = project(_vec, F, N, inv_D)
        _delta = delta(_vec, _vec2)
        _vec = _vec2

        if (_delta * size) < eps:
            #logger.info('Stop at iteration {} with delta: {}.'.format(i, _delta))
            break
    return normalize(_vec)




class PIC(MiniBatchKMeans):
    """
    """
    def __init__(self, n_clusters, eps, pic_max_iter=800, init='k-means++', batch_size=100,
                 verbose=False, kmeans_max_iter=800, random_state=0):
        self.n_clusters = n_clusters
        self.eps = eps
        self.pic_max_iter = pic_max_iter
        self.init = init
        self.batch_size = batch_size
        self.verbose = verbose
        self.kmeans_max_iter = kmeans_max_iter
        self.random_state = random_state

    def _check_fit_data(self, X):
        pass

    def fit(self, F):
        # check_fit_data(F)
        reduced_matrix = pic(F, self.eps, self.pic_max_iter)

        kmeans = MiniBatchKMeans(n_clusters=self.n_clusters, init=self.init, 
                                 batch_size=self.batch_size, verbose=self.verbose, 
                                 max_iter=self.kmeans_max_iter, random_state=self.random_state)

        self.labels_ = kmeans.fit_predict(reduced_matrix)
        self.distances_ = kmeans.transform(reduced_matrix).min(axis=1)

        return self

def vectorize(df):
    tfidf_vec = TfidfVectorizer()
    F = tfidf_vec.fit_transform(df.ns_tokens).toarray()

    zeros_index = np.where(~F.any(axis=1))[0]
    _df = df.iloc[~df.index.isin(zeros_index)]
    F = F[~np.all(F == 0, axis=1)]
    return F, _df


def start_pic(role, stage, patch_idx, df, task_id):
    log_url = '{}/{}'.format('/log', task_id)
    logger = Log(__name__, log_host, log_url).logger
    try:
        #logger.warn('Worker({}, {}, {}) activate, loading: {}'.format(role, stage, patch_idx, len(_df)))
        if len(df) == 1:
            return [df.loc[:]]
        F, _df = vectorize(df)
        pic = PIC(n_clusters=int(np.sqrt(len(_df)/2)), eps=(1.0e-5/len(_df)))
        pic.fit(F)

        return [_df.iloc[np.where(pic.labels_ == i)] for i in np.unique(pic.labels_)]
    except Exception as ex:
        print(repr(ex))
        return [df.loc[:]]

