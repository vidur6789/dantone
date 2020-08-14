import com.thothink.read.JsonFileReader as reader
import com.thothink.write.XlsWriter as writer
import com.thothink.constants.constant as constant
import pandas as pd
import re
from nltk.corpus import stopwords
import string
from fuzzywuzzy import fuzz
import textdistance



# Stop Words
stop_punc = list(string.punctuation) + ['™']
stop_list = ["Singapore", "singapore", "Sentosa", "Temple", "Shrine","sentosa","Package", "package","the" ,"The", "Sale", "sale", "OFF", "Ticket", "ticket", "Open", "open", "In", "in", "of" "KLOOK","Klook","klook"]
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
    attractions = get_attractions()
    attraction_promos = [get_matching_promotions(attraction, promos) for attraction in attractions]
    # filtered_promos = [promo for promo in promo_best_matches if promo[3] >= 0]  # filter promos by threshold > 30
    promos_df = pd.DataFrame(attraction_promos)
    writer.write_df(constant.PATH_OUT / "promos_match", promos_df)


def pre_process(name):
    processed = " ".join([word for word in name.split(" ") if word not in stop_list])
    processed = re.sub("\[(.*?)\]|\((.*?)\)", "", processed).replace('™', '').replace('®', '')
    return processed


# def get_max_ratio(promo, attractions):
#     processed_promo = pre_process(promo["name"])
#     score = 0
#     bestscore = 0
#     bestmatch = ""
#     for attraction in attractions:
#         score = fuzz.token_set_ratio(processed_promo, attraction)
#         if score > bestscore:
#             bestscore = score
#             bestmatch = attraction
#
#     print(bestscore)
#     return (promo["name"], processed_promo, bestmatch, score)


def get_matching_promotions(attraction, promos):
    attraction_name = pre_process(attraction["attractions"])
    best_score = 0
    promo_match = ""
    for promo in promos:
        score = get_similarity_score(attraction_name, promo)
        if score > best_score:
            best_score = score
            promo_match = promo["name"]
    return (attraction["attractions"], attraction_name, best_score, promo_match)


def get_similarity_score(attraction_name, promo):
    promo_name = pre_process(promo["name"])
    if len(attraction_name) >= len(promo_name):
        return fuzz.token_set_ratio(promo_name, attraction_name)
    else:
        score = []
        for start in range(0, len(promo_name) - len(attraction_name)):
            end = start + len(attraction_name)
            promo_sub_string = promo_name[start:end]
            score.append(fuzz.token_set_ratio(attraction_name, promo_sub_string))

        return max(score)


def get_attractions():
    attractions = reader.parse(constant.PATH_OUT / ATTRACTION_FILE)
    sentosa_attractions = reader.parse(constant.PATH_OUT / "sentosa", encoding="utf-8")
    attractions.extend(sentosa_attractions)
    return attractions


if __name__ == "__main__":
    match_promotions()

