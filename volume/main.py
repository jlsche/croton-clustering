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
        self.save_path = '{}/{}'.format(factory_path, task)
        Path(self.save_path).mkdir(exist_ok=True, parents=True)


    def start(self):
        df = self.preprocess_func(self.task, self.save_path)
        self.df_indice = self.clustering_func(self.task, df, self.chunk_size, self.save_path)
        return self



if __name__ == '__main__':
    # request own instance id from Aliyun
    #instance_id = requests.get('http://100.100.100.200/latest/meta-data/instance-id').content
    #instance_id = instance_id.decode('utf-8')
    instance_id = 'A54321'

    '''
    # request to get task id
    start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    resp = requests.post('{}/{}?{}={}'.format(controller_url, instance_id, 'start_time', start_time)).json()
    task_id = resp['id']
    cthr = resp['cthr']
    gthr = resp['gthr']
    '''
    task_id = '1108'
    cthr = 0.9
    gthr = 0.3

    pipeline = Pipeline(task=task_id, chunk_size=2000, preprocess_func=preprocess, clustering_func=clustering)

    pipeline.start()
    
    #concat_csv_files(pipeline.factory_path, result_filepath)

    # update status to redis
    end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    req = '{}/{}?action={}&end_time={}'.format(controller_url, task_id, 'check', end_time)
    resp = requests.put(req)

    # call Claude's API to start stage2 of clustering.
    _url = '{}?csvpath={}/{}&clusterthreshold={}&groupthreshold={}'.format(claude_url, factory_path, task_id, cthr, gthr)
    print(_url)
    #resp = requests.get(_url)


