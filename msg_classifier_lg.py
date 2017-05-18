
# coding: utf-8

from sklearn.externals import joblib
import os.path
import json
from collections import OrderedDict
import re
import jieba
import jieba.analyse

class TextMining:
    def __init__(self,file_name):
        self.keyword_dict = None
        self.file_name = file_name
        self.key_dict = self.get_keyword_dict()
    def get_keyword_dict(self,refresh=False):
        if self.keyword_dict == None or refresh == True:
            if os.path.isfile(self.file_name):
                with open(self.file_name,'r') as infile:
                    keyword_file = json.load(infile, object_pairs_hook=OrderedDict)
                self.keyword_dict = keyword_file
            else:
                print self.file_name+" doesn't exist"
                return 
        return self.keyword_dict
    def _make_ML_X(self,msg_list,print_out=False):
        #key_dict = self.get_keyword_dict()
        ML_X = []
        for msg in msg_list:
            tmp = []
            has_url = 1 if len(re.findall("(?P<url>https?://[^\s]+)", msg))>0 else 0
            msg_len = len(msg)
            tmp.append(has_url)
            tmp.append(msg_len)
            if print_out:
                print 'has_url : ',has_url
                print 'msg_len : ',msg_len
            for k in self.key_dict:
                message_jieba = jieba.analyse.extract_tags(msg,0)
                match = list(set(message_jieba).intersection(self.key_dict[k]))
                if print_out:
                    print 'match '+k+' : ',','.join(match)
                tmp.append(len(match))
            ML_X.append(tmp)
        return ML_X

# jieba setup
jieba.set_dictionary("./archive/dict.txt.big")
jieba.analyse.set_stop_words("./archive/stop_words.txt")
clf = joblib.load('./archive/classifier_lg_model.pkl')
text_min = TextMining('archive/keyword_2.json')
print("Loading model OK!!")

def msg_predict(msg):

    #msg = "新北市警察局土城分局警備隊~關心你！最近FB有一個測年齡的，那個不要去點他，因為只要你點下去，你的資料、照片、姓名…等等，都會給他們使用，請傳下去吧，別讓身邊周遭的朋友受害了！ 新北市警察局土城分局警備隊~關心你！(!?)新版 “身份證算命” 不要玩喔！ 請告訴你的好友要注意， 不法集團利用算命程式，收集身份證字號等資料，他們會要人輸入號碼後算出，千萬別玩，請轉貼分享出去！有毒 ！(NO)千萬別玩！"

    # Transforming string to numerical feature vector
    msg_feature_vector = text_min._make_ML_X([msg])

    # Loading trained machine learning model
    #clf = joblib.load('archive/classifier_lg_model.pkl')

    # Predicting the class of feature vector
    msg_class = clf.predict(msg_feature_vector)

    # 0 : chat 
    # 1 : objective information 
    # 2 : subjective information
    print int(msg_class[0])





