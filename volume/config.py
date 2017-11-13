# coding: utf-8
import string
from pathlib import Path

base_url = 'http://172.16.124.42'
#base_url = 'http://192.168.10.16'
controller_url = '{}:8011/jobs'.format(base_url)
data_baseurl = '{}:8000/static/data'.format(base_url)

log_host = '{}:3000'.format('172.16.124.42')
#log_host = '{}:3000'.format('192.168.10.16')
log_url = '/log'

raw_filename = 'rawdata.csv'
role_filename = 'role.csv'
pov_filename = 'pov.csv'
stopwords_filename = 'stopwords.csv'

basepath = Path(__file__).resolve().parent
data_path = '{}/data'.format(str(basepath))
pov_filepath = '{}/{}'.format(data_path, pov_filename)
stopwords_filepath = '{}/{}'.format(data_path, stopwords_filename)

result_path = '{}/result'.format(str(basepath))
factory_path = '{}/factory'.format(result_path)
actual_path = '/home/lingtelli/workspace/docker/croton-clustering/volume/result/factory'
result_filepath = '{}/cluster_result.csv'.format(result_path)


punctuations = string.punctuation + '—：！？，～。:、“”；［］「」（）『』＠＄《》【】⊙ˇ＃-＂…　·． ︶♫★ง•｡ò∀ó✪▽♛→´◡❁✲๑˙ ﾟლ⌒ε╭°╮√ω＼✧ㅁ'
