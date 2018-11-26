# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 00:36:35 2018

@author: NABARUP
"""
import numpy as np
import wikipedia
import re
import nltk
from gensim.models.keyedvectors import KeyedVectors
from numpy import dot
from numpy.linalg import norm

"THIS PART IS LOADING THE VECTOR OF WORDS FOR WIKIPEDIA WORDS. THIS MAY TAKE SOME TIME "
print("PLEASE WAIT WHILE THE MODEL IS LOADING .....")
model = KeyedVectors.load_word2vec_format('D:/MACHINE LEARNING/unfound\wiki/wiki.vec')   
vocab = model.wv.vocab.keys()
index2word_set=set(vocab)

"### function to average all words vectors in a given paragraph"
def avg_sentence_vector(words, model, num_features):
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])

    if nwords>0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec

print("#############################################################")
"TAKING THE INPUT WORD/PHRASE FROM USER :"


while True:
    try:
        s=""
        word=input("ENTER WORD/PHRASE: ")
        ny = wikipedia.page(word)
    except Exception as e:
        s = str(e)
    if s!="":        
        strr=s.split("\n")
        if len(strr)==1:
            print(s)
        else :
            strr=strr[1:len(strr)-2]
            print("YOU MAY REFER TO :")
            print(strr) 
    else:
        break


#ny.sections
#ny.title
#ny.url
"PREPROCESSING THE CONTEXT"
string= ny.content
sentences=nltk.sent_tokenize(string)
temp=[]
for i in sentences:
    t=[]
    t=re.findall("(\:)",str(i)) 
    if len(t) <=1:         
            b=re.findall(r'\d{4}',i,re.I)
            c=re.findall(r'(yesterday)',i,re.I)
            d=re.findall(r'(today)',i,re.I)
            e=re.findall(r'(tomorrow)',i,re.I)
            if b or c or d or e:
                    process=re.sub(r'(\n).*?(\n)','\n',i)
                    g=re.findall("=",process)
                    while g :     
                        process=re.sub(r'(\=).*?(\n)','\n',process)
                        process=re.sub(r'(\=).*?(\n)','',process)
                        process=re.sub(r'(\=).*?(\n)','',process)
                        process=re.sub(r'(\=).*?(\=)','',process)
                        process=re.sub(r'(\n)','',process)
                        g=re.findall("=",process)
                    temp.append(process)
    else:
        continue
#    print(len(t))
    
            
"#get average vector for sentence 1"
sentence_1 = word
sentence_1_avg_vector = avg_sentence_vector(sentence_1.split(), model=model, num_features=300)
#len(sentence_1_avg_vector)
"Creating a Dictionary Where keys are the similarity scores and values are the sentences"
mydict={}
for i in temp:
    sentence_2=i
    sentence_2_avg_vector = avg_sentence_vector(sentence_2.split(), model=model, num_features=300)
    cos_sim = dot(sentence_1_avg_vector, sentence_2_avg_vector)/(norm(sentence_1_avg_vector)*norm(sentence_2_avg_vector))
    mydict[cos_sim]=i
    
"SORT THE FINAL DICTIONARY"
mydict1= sorted(mydict.items(), key=lambda item: (item[0],item[1]),reverse=True)

#print(len(mydict1))
"GIVE OUTPUT TO THE USER :"
while True:   
        num=int(input("ENTER NO OF TIMELINES :"))
        print("##########################################")
              
        if num >len(mydict1):
            print("MAX " + str(len(mydict1))+" TIMELINES AVAILABLE . TRY AGAIN >>>> ")
        else:
            for i in range(num):
                print(str(i+1) +". "+ mydict1[i][1])
                print()
            break



