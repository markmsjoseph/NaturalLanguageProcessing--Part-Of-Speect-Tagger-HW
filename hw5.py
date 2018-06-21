import string
from collections import defaultdict
from collections import Counter
import math
import re
from operator import itemgetter

dict = {}
d = defaultdict(int)
id =()
file = open('cran.qry', 'r')
flag = False# used to get a sentence that may go into more than 1 lines
sentence = ""

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ]


for line in file:
    if(line.startswith(".W")):
        continue

    elif(line.startswith(".I")):
            line1 = line.split(" ")
            oldID = line1[1]
            id = oldID.replace("\n", "")

    else:
        for c in line:
            if(c == "."):
                flag = True
            else:
                    sentence = sentence + c
        if(flag):
            newSent = sentence.replace("\n", " ")

            #remove punctuation and digits from string
            exclude = set(string.punctuation)
            s = ''.join(ch for ch in newSent if ch not in exclude and not ch.isdigit())

            #update dictionary with id and string without punctuation
            dict.update({id:s})
            flag = False
            sentence = "" # if new query we reset the sentence string


# create an array with the words that are filtered completely and add them to dictionary
for key, value in dict.items():
    arr = []
    filteredStopWords = []
    for word in value.split():
        arr.append(word)
    # filter words that are common and add them to a new array
    for i in range(len(arr)):
        flag=True
        for j in range(len(closed_class_stop_words)):
            if(arr[i] == closed_class_stop_words[j]):
                flag = False
                break
            if(j == len(closed_class_stop_words)-1 and flag == True):
                filteredStopWords.append(arr[i])
    # add array to dictionary
    dict[key] = filteredStopWords

print("\n")
wordsDict = {}
# count the number of occurances of each non stop word in each query
for key, value in dict.items():
        counts = Counter(value)
        for i in counts:
            tup = ("answer", "tfidf")
            wordsDict.update({i:tup})



# put each word into a dicionary as the key and the value will be the number of times it occurs in a query
for key, value in wordsDict.items():
        wordInQuery = 0
        # if the word occurs in a query increment the counter
        for array in dict.values():
                # if the word is in the array increment the counter
                if key in array:
                   wordInQuery = wordInQuery + 1
                #change the value in the dictionary
                wordsDict[key] = (wordInQuery, "tfidf")

# calculate idf score for each wordd
for key, value in wordsDict.items():
        idf = math.log(len(dict)/value[0])
        wordsDict[key] = (value[0], idf)

# print idf score for each word, we have to print
# after we are finished with the dict for thr value to update
for key, value in wordsDict.items():
        print( "IDF for " + str(key)+ " = " + str(value[1]) )
print("\n")
print("\n")

tfDict = {}
for key, value in dict.items():
        print("Query Vector " + str(key)+ " = " + str(value))
        print("Number of occurances of each non-stop word in this query are:")

        counts = Counter(value)
        for i in counts:
            tuple = wordsDict.get(i)
            wordFrequency = counts[i]
            idf = tuple[1]
            tfidf = wordFrequency * idf
            tfDict.update({i:tfidf})
             #print(str(i) + ' and freq: ' + str(wordFrequency) + " and idf: " + str(idf) + " and" + str(tfidf))
            print( "Word: " +str(i) + "\tCount: " + str(counts[i]) + " TF-IDF: " + str(tfidf))
        print("\n")

print("\n\n\n\n ========================================= PART 3 ================================================\n\n\n\n")


file2 = open('cran.all.1400', 'r')
arr = []# this will hold the array of lines

# for each line, place it as an index in the array
for line in file2:
    line1 = line.replace("\n"," ")
    arr.append(line1)

ids=[] # this will hold the id number
arrayOfSentences = [] # this will hold the sentences

# get all of the sentences
for i in range(len(arr)):
    # if it is an id line put it in an id array
    if arr[i].startswith(".I"):
        ln = arr[i].split()
        id = ln[1]
        ids.append(id)
    # save the start of sentence
    if arr[i].startswith(".W"):
        start = i
    if ((arr[i].startswith(".I") and i>0) or arr[i] == arr[len(arr)-1] ):
        sentence = ""
        between = i
        # +1 is to get rid of .W
        words = arr[start+1:between+1]
        # put these indicies of words into a string
        for j in range(len(words)):
            if(words[j]).startswith(".I"):
                continue
            else:
                sentence = sentence + words[j]
        #remove punctuation and digits from string
        exclude = set(string.punctuation)
        s = ''.join(ch for ch in sentence if ch not in exclude and not ch.isdigit())
        arrayOfSentences.append(s)
        # print(arrayOfSentences)



# the ids and sentences are in two different arrays so make them into 1 element pairs
arrayOfTuples = []
for i in range(len(ids)):
    tup = ((ids[i]),(arrayOfSentences[i]))
    arrayOfTuples.append(tup)


abstractsDict={}
for i in range(len(arrayOfTuples)):
    abstractsDict.update({arrayOfTuples[i][0]:arrayOfTuples[i][1]})

#
#create an array with the words that are filtered completely and add them to dictionary
for key, value in abstractsDict.items():
    arr = []
    filteredStopWords = []
    for word in value.split():
        arr.append(word)
    # filter words that are common and add them to a new array
    for i in range(len(arr)):
        flag=True
        for j in range(len(closed_class_stop_words)):
            if(arr[i] == closed_class_stop_words[j]):
                flag = False
                break
            if(j == len(closed_class_stop_words)-1 and flag == True):
                filteredStopWords.append(arr[i])
    # add array to dictionary
    abstractsDict[key] = filteredStopWords

# for key, value in abstractsDict.items():
#         print( "ID: " + str(key)+ " Abstract: " + str(value) )
# print("\n")

print("\n")
abscount = {}
# count the number of occurances of each non stop word in each abstract
for key, value in abstractsDict.items():
        counts = Counter(value)
        for i in counts:
            tup = ("answer", "tfidf")
            abscount.update({i:tup})



# put each word into a dicionary as the key and the value will be the number of times it occurs in a query
for key, value in abscount.items():
        wordInQuery = 0
        # if the word occurs in a query increment the counter
        for array in abstractsDict.values():
                # if the word is in the array increment the counter
                if key in array:
                   wordInQuery = wordInQuery + 1
                #change the value in the dictionary
                abscount[key] = (wordInQuery, "tfidf")

# calculate idf score for each wordd
for key, value in abscount.items():
        idf = math.log(len(dict)/value[0])
        abscount[key] = (value[0], idf)

# print idf score for each word, we have to print
# after we are finished with the dict for thr value to update
for key, value in abscount.items():
        print( "IDF for " + str(key)+ " = " + str(value[1]) )
print("\n")

for key, value in abstractsDict.items():
        print("Abstract Vector " + str(key)+ " = " + str(value))
        print("Number of occurances of each non-stop word in this abstract are:")

        counts = Counter(value)
        for i in counts:
            print( "Word: " +str(i) + "\tCount: " + str(counts[i]) )
        print("\n")

print("\n\n\n\n ========================================= PART 5 ================================================\n\n\n\n")

queryVectorDict = {}

# store query number and tfidf values for each word in that vector
for key, value in dict.items():
        arr =[]
        print("Query Vector " + str(key)+ " = " + str(value))
        for i in range(len(value)):
            arr.append(tfDict.get(value[i]))
        queryVectorDict.update({key:arr})
print()

print("Query Vector TFIDF scores:")
for key, value in queryVectorDict.items():
        print("Query is " + str(key)+ ": " + str(value))
print()
for key, value in abstractsDict.items():
        print("Abstract Vector " + str(key)+ " = " + str(value))

answersDict = {}
print()
output = ""
for qkey,queryWord in dict.items():# for each query array
    print("Query "+ qkey + ": " + str(queryVectorDict.get(qkey)))
    for akey,queryAbstract in abstractsDict.items():# for each abstract array
        scoreVect = []

        for i in range(len(queryWord)):# for each element in the array
            added = "we added nothing"
            for j in range(len(queryAbstract)):# for each word in the abstract
                if queryWord[i] == queryAbstract[j]:
                    added =  "we added something"

                # # # we did not find it add 0
                if j == len(queryAbstract)-1 and added == "we added nothing":
                    scoreVect.append(0)
                elif(j == len(queryAbstract)-1 and added == "we added something"):
                    val = abscount.get(queryWord[i])
                    scoreVect.append(val[1])
        print("Abstract " + akey + ": " + str(scoreVect))# print after the  iteration of i is over

        # calculate cosine similarity for each abstract
        tot = 0
        numTopSquare = 0
        nonZeroAbs = 0
        # actual calculation for cosine similarity for 1 abstract
        for k in range(len(scoreVect)):
            arr = queryVectorDict.get(qkey)
            quer =  arr[k]
            abs = scoreVect[k]
            if abs > 0:
                nonZeroAbs = nonZeroAbs + (abs*abs)
            tot = tot + (quer * abs)
            square = quer * quer
            numTopSquare = numTopSquare + square
        denom = math.sqrt(numTopSquare * nonZeroAbs)
        #only add things that do not have a cosine similarity score of 0
        if(denom == 0):
            continue
        else:
            cosineSimilarity = tot /denom
            answer = str(qkey) + " "+ str(akey) + " " + str(cosineSimilarity) + "\n"
            output = output + answer
        # f = open('output','w')
        # f.write(str(qkey) + " "+ str(akey) + " " + str(cosineSimilarity)) # python will convert \n to os.linesep

        # tup = (akey,cosineSimilarity)
        # print("hi")
        # answersDict.update({qkey:tup})

    print()

f = open('output','w')
f.write(output)
f.close()

#====================================================== sorting =======================================

dataToSort = []
print("sorting")
out = open('output', 'r')
# read data into array in order to sort
for line in out:
    tup = line.split()
    dataToSort.append(tup)
#sorted data in newarr
newarr = sorted(dataToSort, key=lambda element: (element[0], element[2]))

f = open('finalOutput','w')
for i in range(len(newarr)):
    line = '   '.join(newarr[i])
    print(line)
    f.write(line + '\n')
f.close
