import com.thothink.read.JsonFileReader as reader
import com.thothink.write.XlsWriter as writer
import com.thothink.constants.constant as constant
import pandas as pd
import re
from nltk.corpus import stopwords
import string
from fuzzywuzzy import fuzz

# Stop Words
stop_punc = list(string.punctuation) + ['™']
stop_list = ["Singapore", "singapore", "Sentosa", "sentosa","Package", "package","the" ,"The", "Sale", "sale", "OFF", "Ticket", "ticket", "Open", "open", "In", "in", "of" "KLOOK","Klook","klook"]
stop_list.extend(stopwords.words("english"))
stop_list.extend(stop_punc)

#File Paths
PROMO_FILE = "KlookResults"
ATTRACTION_FILE = "All_fixed"


def json_to_excel():
    file_path = constant.PATH_OUT
    file_name = "KlookResults"
    data = reader.parse(file_path / file_name)
    df = pd.DataFrame(data)
    writer.write_df(file_path / file_name, df)



def match_promotions():
    promos = reader.parse(constant.PATH_OUT / PROMO_FILE)
    attractions = reader.parse(constant.PATH_OUT / ATTRACTION_FILE)
    sentosa_attractions = reader.parse(constant.PATH_OUT / "sentosa", encoding="utf-8")
    attractions.extend(sentosa_attractions)
    attraction_names = [pre_process(attraction["attractions"]) for attraction in attractions]
    promo_best_matches = [get_max_ratio(promo, attraction_names) for promo in promos]  # get best match attraction for promo
    filtered_promos = [promo for promo in promo_best_matches if promo[3] >= 30]  # filter promos by threshold > 30
    promos_df = pd.DataFrame(filtered_promos)
    writer.write_df(constant.PATH_OUT / "promos_match", promos_df)


def pre_process(name):
    processed = " ".join([word for word in name.split(" ") if word not in stop_list])
    processed = re.sub("\[(.*?)\]|\((.*?)\)", "", processed).replace('™', '').replace('®', '')
    print(processed)
    return processed


def get_max_ratio(promo, attractions):
    processed_promo = pre_process(promo["name"])
    score = 0
    bestscore = 0
    bestmatch = ""
    for attraction in attractions:
        score = fuzz.token_set_ratio(processed_promo, attraction)
        if score > bestscore:
            bestscore = score
            bestmatch = attraction
    return (promo["name"], processed_promo, bestmatch, score)




if __name__ == "__main__":
    match_promotions()

