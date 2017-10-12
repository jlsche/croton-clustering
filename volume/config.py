# coding: utf-8
import string

#base_url = 'http://172.16.123.213'
base_url = 'http://192.168.10.16'
claude_url = '{}:{}/{}'.format(base_url, 3006, '')
controller_url = '{}:{}/{}'.format(base_url, 8011, 'jobs')
data_baseurl = '{}:{}/{}/{}'.format(base_url, 8000, 'static', 'data')

#log_host = '{}:{}'.format('172.16.123.213', 3000)
log_host = '{}:{}'.format('192.168.10.16', 3000)
log_url = '/log'

raw_filename = 'rawdata.csv'
role_filename = 'role.csv'
pov_filename = 'pov.csv'
stopwords_filename = 'stopwords.csv'

data_path = './data'
rawdata_filepath = '{}/{}'.format(data_path, raw_filename)
role_filepath = '{}/{}'.format(data_path, role_filename)
pov_filepath = '{}/{}'.format(data_path, pov_filename)
stopwords_filepath = '{}/{}'.format(data_path, stopwords_filename)

result_path = './result'
factory_path = '{}/{}'.format(result_path, 'factory')
result_filepath = '{}/{}'.format(result_path, 'cluster_result.csv')


punctuations = string.punctuation + '—：！？，～。:、“”；［］「」（）『』＠＄《》【】⊙ˇ＃-＂…　·． ︶♫★ง•｡ò∀ó✪▽♛→´◡❁✲๑˙ ﾟლ⌒ε╭°╮√ω＼✧ㅁ'
