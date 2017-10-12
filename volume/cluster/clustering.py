# coding: utf-8
import multiprocessing
import pandas as pd
import numpy as np
from cluster.pic import start_pic
from config import *
from lib.http_logger import Log


def clustering(task_id, df, chunk_size, save_path):
    log_url = '{}/{}'.format('/log', task_id)
    logger = Log(__name__, log_host, log_url).logger

    for role in df.role.unique():
        sub_df = df[df.role == role]
        logger.info("Clustering character {}, comment count: {}".format(role, len(sub_df)))
        if len(sub_df) == 0:
            #print('skip', flush=True)
            continue
        # stage1
        chunks = assign_jobs(sub_df, chunk_size)
        logger.info('Processing stage1 of {}, job count: {}'.format(role, len(chunks)))
        _clusters = start_job(role, 1, chunks, task_id)

        # stage2
        #chunks = assign_jobs(sub_df, chunk_size)
        logger.info('Processing stage2 of {}, job count: {}'.format(role, len(_clusters)))
        #_clusters = start_job(role, 2, chunks)
        _clusters = start_job(role, 2, _clusters, task_id)

        # stage3
        #chunks = assign_jobs(sub_df, chunk_size)
        logger.warn('Done stage2 of {}, # of clusters'.format(role, len(_clusters)))
        typical_points, typical_indexes = get_typical(_clusters)
        logger.warn('Processing stage3 of {}, done get_typical()'.format(role))
        sub_df_typical = pd.concat(typical_points, axis=1).transpose()
        logger.warn('Processing stage3 of {}, done concate()'.format(role))

        chunks = assign_jobs(sub_df_typical, chunk_size)
        logger.info('Processing stage3 of {}, job count: {}'.format(role, len(chunks)))
        clusters = start_job(role, 3, chunks, task_id)

        clusters = merge(clusters, typical_indexes, _clusters)

        sentence_list = []
        size_list = []
        for temp_df in clusters:
            sentence_list.append(',  '.join(temp_df.source))
            size_list.append(len(temp_df))
        result = pd.DataFrame({'count': size_list, 'members': sentence_list})
        path = '{}/{}_{}.csv'.format(save_path, 'cluster_result_', role)
        result.sort_values(by=['count'], ascending=False).to_csv(path, index=False, encoding='utf-8')



def get_typical(clusters):
    """ Get the representative point from each clusters.
    """
    points = [df.iloc[0] for df in clusters]
    indexes = [df.index[0] for df in clusters]
    return points, indexes


def merge(key_clusters, typical_indexes, child_clusters):
    clusters = []
    for key_cluster in key_clusters:
        key_indexes = key_cluster.index

        members = []
        for index in key_indexes:
            i = typical_indexes.index(index)
            members.append(child_clusters[i])
        df = pd.concat(members)
        clusters.append(df)
    return clusters


def assign_jobs(df, chunk_size):
    """ Split dataframe equally to chunks.
    """
    if len(df) >= chunk_size:
        return np.array_split(df, len(df) // chunk_size)
    else:
        return [df]


def start_job(role, stage, chunks, task_id):
    # Too many processess opend will crash.
    pool = multiprocessing.Pool(4)
    results = []
    
    #try:
    for i in range(len(chunks)):
        result = pool.apply_async(start_pic, args=(role, stage, i, chunks[i], task_id, ))
        results.append(result)
    #catch:
    pool.close()
    pool.join()
    results = [x.get() for x in results]
    clusters = [df for df_list in results for df in df_list]
    return clusters
        
