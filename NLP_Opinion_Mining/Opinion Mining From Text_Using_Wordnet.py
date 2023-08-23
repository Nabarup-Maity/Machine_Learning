# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:00:01 2018

@author: NABARUP
"""
from nltk.corpus import wordnet as wn
import pandas as pd
import re, string
import nltk
#from nltk.corpus import sentiwordnet as swn

xls_file = pd.ExcelFile("pm_qualities_data.xlsx")

#print(xls_file.__class__)
#print(xls_file.sheet_names)
file = xls_file.parse("Sheet1")
#print(file)
file_low = []
for i in range(0,len(file)):
    file_low.append(file.iloc[i,0].lower())

#print(file_low)
#print(len(file_low))
#print(file_low[0])
#print(file_low[5])

##############    removing puntuation,commas and replacing space
file_no_punc = []
for i in range(0,len(file_low)):
    out = re.sub('[%s]' % re.escape(string.punctuation),'',file_low[i])
    file_no_punc.append(out)

#print(file_no_punc[0]) # 2st row in exel
#print(file_no_punc[5]) #7th

################################   tokenising with nltk(tokenise each row)

file_token = []
for i in range(0,len(file_no_punc)):
    file_token.append(nltk.word_tokenize(file_no_punc[i]))

#print(len(file_token))
#print(file_token[0])
#print(file_token[5])

'  1 .  #############################################################################'
'######################   Form the vocabulary of the data set.#######################=296'

#print("========= putting into a single list =========")
vocabulary = []
for i in range(0,len(file_token)):
    for j in range(0,len(file_token[i])):
        vocabulary.append(file_token[i][j])
      
#print('len(vocabulary)')
#print(len(vocabulary))
#print(vocabulary)
#print(vocabulary[0])

'############## consider only the nouns and adjectives and simply ignore the other words,'
'############## since the objective is to find the qualities of the PM.'

'(a)tagging with nltk=296'
tagged = nltk.pos_tag(vocabulary)
#print(len(tagged))
   


'(b) take only the nouns and adjectives = 168'
'nouns'
noun_adj = [word for word, pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS'
                                or pos == 'NNPS' or pos == 'JJ' or pos == 'JJS' or pos=='JJR' )]
    
#print(len(noun_adj))
#print('noun_adj')
#print(noun_adj)

 
'(c) Find the frequency of each word and order the words in order of decreasing frequency.'

from collections import Counter
word_count = Counter(noun_adj)
#print('word_count')
#print(word_count)
#print('len(word_count)')
#print(len(word_count))

#print(word_count.most_common(5))


'2. ###   Find the synonyms for each word (using Wordnet synsets) and include them in the vocabulary.'


'a.. ########################### finding the noun and adjective and verb synsets'

#print('finding the noun and adj synsets')

noun_adj_verb_syn = []
for words in set(word_count):
    syn = wn.synsets(words,wn.ADJ)
    syn1 = wn.synsets(words,wn.NOUN) # to extract the synonyms that are nouns
#    syn2 = wn.synsets(words,wn.VERB)
    #noun_adj_verb_syn.append(words)
    noun_adj_verb_syn.append(syn)
    noun_adj_verb_syn.append(syn1)
#    noun_adj_verb_syn.append(syn2)
 

#print('noun_adj_verb_syn')
#print(noun_adj_verb_syn)
#print('length of (noun_adj_verb_syn)')
#print(len(noun_adj_verb_syn))


'############    removing the empty lists==> [[],[],[]]'
noun_adj_verb_syn = [x for x in noun_adj_verb_syn if x != []]


'#############    after removing the empty lists noun_adj_verb_syn=>145'

#print('after removing the empty lists noun_adj_verb_syn')
#print(noun_adj_verb_syn)
#print(len(noun_adj_verb_syn))  #  the number of subarray

#print(noun_adj_verb_syn[0][0].name())
#print(noun_adj_verb_syn[0][1].name())


'b ..   ############# take each synset and add to new vocabulary'
new_voc=set()

for i in range(0,len(noun_adj_verb_syn)):
    for j in range(0,len(noun_adj_verb_syn[i])):
        new_voc.add(noun_adj_verb_syn[i][j].name()) # unique_words is  set object
        
#print('take each synset and add to new vocabulary')        
#print('new_voc') 
#print(new_voc)        
#print(len(new_voc)) #all

'3. #####  Find the derivationally related forms of each word, if any and add them to the vocabulary.'

new_list = []
for i in range(0,len(noun_adj_verb_syn)):
    for j in range(0,len(noun_adj_verb_syn[i])):
        new_list.append(noun_adj_verb_syn[i][j].lemmas()[0].derivationally_related_forms())



'total==>>615'
#print('len(new_list)')
#print(len(new_list))

'# remove the blank list==>325'
#print('# remove the blank list==>325')
new_list = [x for x in new_list if x != []]
#print('new_list')        
#print(new_list)
#print('new_list 0:10')    
#print(new_list[0:10])


#print('len(new_list)')
#print(len(new_list))

'# for each lemma take their names unique==>307'
new_list_1 = []
for i in range(0,len(new_list)):
    for j in range(0,len(new_list[i])):
        new_list_1.append(new_list[i][j].name())
#print(len(new_list_1))
#new_list_1 = set(new_list_1)   # set object unique
#print('new_list_1')
#print(new_list_1)
#print(len(new_list_1))



'# find their noun and adj synsets of the names(as they are only string)'
noun_adj_verb_synset_of_new_list_1 = []
for name in set(new_list_1):
    synname = wn.synsets(name,wn.NOUN)
    synname1 = wn.synsets(name,wn.ADJ)
    noun_adj_verb_synset_of_new_list_1.append(synname)
    noun_adj_verb_synset_of_new_list_1.append(synname1)

'# remove the empty lists'
noun_adj_verb_synset_of_new_list_1 = [x for x in noun_adj_verb_synset_of_new_list_1 if x != []]
#print(noun_adj_verb_synset_of_new_list_1[0:5])

'# add these names to new_voc list'
for i in range(0,len(noun_adj_verb_synset_of_new_list_1)):
    for j in range(0,len(noun_adj_verb_synset_of_new_list_1[i])):
        new_voc.add(noun_adj_verb_synset_of_new_list_1[i][j].name())
            # new_voc is set object
#
#print('len(new_voc)')
#print(len(new_voc))
#print('new_voc after derivationally related forms of each word ')
#print(new_voc)
#


b = []
for words in set(new_voc):
    b.append(words)

#print("b=>757")
#print(b)
#print(b[4])
#print(len(b))


print('clustering')

total_cluster = []
threshold = 0.87
for i in range(len(b)):
    cluster=[]
    if i < len(b):
        for j in range(0,len(b)):
               syn1=wn.synset(b[i])
               syn2=wn.synset(b[j])
               sim=syn1.wup_similarity(syn2)
               if sim is not None and sim > threshold :
                              cluster.append(b[j])
        total_cluster.append(cluster)

            
#
#print("\n after clustering using a threshold \n")
#print(len(total_cluster))
#print(total_cluster)
total_cluster = [x for x in total_cluster if x != []] # empty cluster removed"




#print('len(total_cluster)')
#print(len(total_cluster))
#print(total_cluster)
#print(total_cluster[0])
#print(total_cluster[1])

########### SPLITTING
a=[]
for i in range(0,len(total_cluster)):
    final_cluster1=[]
    for j in range(0,len(total_cluster[i])):
        t=total_cluster[i][j].split('.')
        for x in range(0,len(t)):
            if(len(t[x]))>=3:
                final_cluster1.append(t[x])
                ABC=set(final_cluster1)
                XYZ=list(ABC)
        a.append(XYZ)
        
#print("a")
#print(len(a))
#
#print(a)
### Recalculate the frequency of each cluster and order them in decreasing order of frequency.


final_cluster1=[]
for i in range(0,len(a)):
    final_cluster2=[]
    for j in range(0,len(a[i])):
        COUNT=0
        if a[i][j] in word_count:
            COUNT=len(a[i])
#            print(COUNT)
        if COUNT >=2:       
            final_cluster2.append(a[i])     
            final_cluster2.append(COUNT)
            final_cluster1.append(final_cluster2)
            break


#print('word_count')
#print(word_count)
print('final_cluster')
print(len(final_cluster1))
#print(final_cluster1)




        
#print('len(final_cluster1)')
#print(len(final_cluster1))
#print('len(word_count)')
#print(len(word_count))


print("1===============================================")
df = pd.DataFrame(final_cluster1,columns=("clusters","count"))
print("===============================================")
df = df.sort_values(by = 'count',ascending=0)
print(df.head(5))


print("===============================================")

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('final_cluster___1.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()





#======================end
