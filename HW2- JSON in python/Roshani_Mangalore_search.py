from sets import Set
import string
from collections import OrderedDict
import json
import re
import sys


input_file = sys.argv[1]
questions=[]
pattern = r'(?<=\s){0}(?=\s)|^{0}(?=\s)|(?<=\s){0}$|^{0}$'
qlist=[]

keyword_list=[]
a=sys.argv[2]

keyword_list = a.split(" ")
klength = len(keyword_list)

with open(input_file, 'r') as f:
    d = json.load(f)


for i in range(0,len(d['data'])):
  for j in range (0,len(d['data'][i]['paragraphs'])):
      for k in range(0,len(d['data'][i]['paragraphs'][j]['qas'])):
         count = 0
         for keyword in keyword_list:
           set1=Set(string.punctuation)
           set2=Set("'")
           questions_string=set1-set2 #Handling all punctuations except apostrophes
           questions_string=''.join(questions_string)
           translator = string.maketrans(questions_string, ' ' * len(questions_string))#to replace special characters with the space
           encoded_question=(d['data'][i]['paragraphs'][j]['qas'][k]["question"].lower()).encode('ascii','ignore')
           if re.search(pattern.format(keyword.lower()),encoded_question.translate(translator)):
            count += 1
         if count==klength:
            qlist.append(OrderedDict([("id",d['data'][i]['paragraphs'][j]['qas'][k]['id']),
                                     ("question",d['data'][i]['paragraphs'][j]['qas'][k]['question']),
                                     ("answer",  d['data'][i]['paragraphs'][j]['qas'][k]['answers'][0]['text'])]))


#write into a json file
with open('1b.json', 'w') as fp:
    json.dump(qlist, fp,indent=3)
