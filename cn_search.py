#-*- coding: utf-8 -*-

from collections import Counter
from glob import glob
import pandas as pd

search_word = input("请输入你想检索的单词： ")
#search_word = "我/rr"
dict = {}

for filename in glob('*.txt'):
    with open(filename, 'r', encoding="utf-8-sig") as f:
        file = f.read()
        tokens = file.split()
        tokens_freq = len(tokens)
        search_word_freq = tokens.count(search_word)
        standard_freq = round(search_word_freq/tokens_freq*100,3)
        dict[filename] = [tokens_freq, search_word_freq, standard_freq]
df = pd.DataFrame.from_dict(dict,orient="index",columns=["総語数", search_word, "相対頻度"])
keyword = search_word.split("/")[0]
savename = keyword + ".csv"
df.to_csv(savename)