import os

import constants.constant as constant
import read.JsonFileReader as json_reader
import write.JsonFileWriter as json_writer


def accumulate_results(out_dir, acc_file_name):
    data = []
    for file_name in os.listdir(str(out_dir)):
        file_data = json_reader.parse(out_dir / file_name)
        data.extend(file_data)
    print(len(data))
    json_writer.write(out_dir / acc_file_name, data)


def merge_attributes(out_dir, merged_file_name):
    key_stats = collect_attr_dict(out_dir / constant.FILE_MS_KEY_STAT, constant.ATTR_KEY_STAT)
    fin_stats = collect_attr_dict(out_dir / constant.FILE_MS_FIN_STAT, constant.ATTR_FIN_STAT)
    print(len(key_stats.items()))
    print(len(fin_stats.items()))
    data = []
    ''' for all tickers, create single entry containing key stats, fin stats and append to data list '''
    for ticker in key_stats:
        data.append({constant.ATTR_SYMBOL: ticker,
                     constant.ATTR_KEY_STAT: key_stats[ticker],
                     constant.ATTR_FIN_STAT: fin_stats[ticker]})
    print(len(data))
    json_writer.write(out_dir / merged_file_name, data)


def collect_attr_dict(file_path, attr_name):
    attr_dict = {}  # dict of {ticker: attrData}
    attr_data = json_reader.parse(file_path)
    for item in attr_data:
        ticker = item[constant.ATTR_SYMBOL]
        attr_dict[ticker] = item[attr_name]
    return attr_dict


if __name__ == "__main__":
    accumulate_results(constant.PATH_OUT/'20220220_Mstar', constant.FILE_MS_STAT)
