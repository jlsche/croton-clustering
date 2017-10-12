# coding: utf-8
import pandas as pd

'''
def save_result(df_indice, path):
    sentence_list = []
    size_list = []
    for role, df_list in df_indice.items():
        for df in df_list:
            sentence_list.append(',  '.join(df.source))
            size_list.append(len(df))
    result = pd.DataFrame({'count': size_list, 'members': sentence_list})
    result.sort_values(by=['count'], ascending=False).to_csv(path, index=False)
'''

def concat_csv_files(from_path, to_path):
    import glob
    df_list = []
    all_csv = glob.glob(from_path + '/*.csv')
    for _csv in all_csv:
        df = pd.read_csv(_csv)
        df_list.append(df)
    dataframe = pd.concat(df_list, ignore_index=True)
    dataframe.sort_values(by=['count'], ascending=False).to_csv(to_path, index=False)
    

