# coding: utf-8
import string
from pathlib import Path

base_url = 'http://172.16.123.213'
#base_url = 'http://192.168.10.16'
private_ip = 'http://172.16.123.197'
claude_url = '{}:{}/{}'.format(private_ip, 3006, 'startClustering')
controller_url = '{}:{}/{}'.format(base_url, 8011, 'jobs')
data_baseurl = '{}:{}/{}/{}'.format(base_url, 8000, 'static', 'data')

log_host = '{}:{}'.format('172.16.123.213', 3000)
#log_host = '{}:{}'.format('192.168.10.16', 3000)
log_url = '/log'

raw_filename = 'rawdata.csv'
role_filename = 'role.csv'
pov_filename = 'pov.csv'
stopwords_filename = 'stopwords.csv'

basepath = Path(__file__).resolve().parent
data_path = '{}/{}'.format(str(basepath), 'data')
pov_filepath = '{}/{}'.format(data_path, pov_filename)
stopwords_filepath = '{}/{}'.format(data_path, stopwords_filename)

result_path = '{}/{}'.format(str(basepath), 'result')
factory_path = '{}/{}'.format(result_path, 'factory')
actual_path = '/home/lingtelli/workspace/docker/croton-clustering/volume/result/factory'
result_filepath = '{}/{}'.format(result_path, 'cluster_result.csv')


punctuations = string.punctuation + '—：！？，～。:、“”；［］「」（）『』＠＄《》【】⊙ˇ＃-＂…　·． ︶♫★ง•｡ò∀ó✪▽♛→´◡❁✲๑˙ ﾟლ⌒ε╭°╮√ω＼✧ㅁ'
