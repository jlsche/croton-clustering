import requests
from time import gmtime, strftime
from pathlib import Path
from preprocess.preprocess import preprocess
from cluster.clustering import clustering
from lib.utils import *
from config import *


class Pipeline:
    def __init__(self, task, chunk_size, preprocess_func, clustering_func):
        self.task = task
        self.chunk_size = chunk_size
        self.preprocess_func = preprocess_func
        self.clustering_func = clustering_func
        self.factory_path = factory_path

    def start(self):
        df = self.preprocess_func(self.task)
        self.df_indice = self.clustering_func(self.task, df, self.chunk_size, self.factory_path)
        return self



if __name__ == '__main__':
    # request own instance id from Aliyun
    #instance_id = requests.get('http://100.100.100.200/latest/meta-data/instance-id').content
    #instance_id = instance_id.decode('utf-8')
    instance_id = 'A54321'

    # request to get task id
    start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    resp = requests.post('{}/{}?{}={}'.format(controller_url, instance_id, 'start_time', start_time)).json()
    task_id = resp['id']
    cthr = resp['cthr']
    gthr = resp['gthr']


    pipeline = Pipeline(task=task_id, chunk_size=2000, preprocess_func=preprocess, clustering_func=clustering)

    pipeline.start()
    
    #concat_csv_files(pipeline.factory_path, result_filepath)

    # update status to redis
    end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    req = '{}/{}?{}={}&{}={}'.format(controller_url, task_id, 'action', 'check', 'end_time', end_time)
    resp = requests.put(req)

    
    # call Claude's API to start stage2 of clustering.
    #resp = requests.get('{}?taskid={}&cthr={}&gthr={}'.format(claude_url, task_id, cthr, gthr))


