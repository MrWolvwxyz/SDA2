import os
import sys
import re
import numpy as np
import scipy as sci
import string

class sentence:

        #Instantiation function
        def __init__( self, word_list, word_vecs ):
            self.words = word_list
            self.size = len( word_list )
            #Maybe do one last check for non-alphanumerics here
            self.data = [ word_vecs[ dictionary[ word_list[ i ] ] ] for i in range( self.size ) ]

        def sent_print( self ):
            print self.size, self.words,  self.data, '\n'

        def get_size( self ):
            return self.size


#create the dictionary and rescale the value
f3 = open("word_vectors.txt", "r")
f3.flush()

lines = f3.readlines()
num_words = int( lines[ 0 ].split()[ 0 ] )
vec_size = int( lines[ 0 ].split()[ 0 ] )

dicVec = []
word_vectors = np.ndarray( shape = ( 71289, 200 ), dtype = float )
#initialize dictionary
dictionary = {}
index = 0
#print 'here\n'
for line in lines[ 1: ]:
    word = line.split()[0]
    usable_vec = map( float, line.split()[ 1 : ] )
    dicVec += [ word ]
    #hashmap that maps word(string) to index(int)(starts from 0)
    dictionary[word] = index

    #word_vectors can be indexed as an array using index[dictionary[word]]
    word_vectors[ index ] = map( float, line.split()[ 1 : ] )
    #print word_vectors
    index = index + 1
    #print index

#cut off the largest and smallest 10% and rescale all value to uni(0,1)
low = np.percentile( word_vectors, 10 )
high = np.percentile( word_vectors, 90 )
word_vectors = np.clip( word_vectors, low, high )
word_vectors = ( word_vectors -low ) / ( high - low )
#print word_vectors[100]

np.save( "word_vec_reg_array", word_vectors )

#input 3-word sentence
f = open("3_word_sentences.txt","r+")
f.seek(0)
sentences = f.readlines()
num_sentence = len(sentences)
#check whether words in sentence are in the dictionary
listOfLines = []
listOfLineIndexes = []

for sen in sentences:
    sen_split = sen.split('\n')
    #print len(sen_split)
    s = sen_split[0]
    #print s
    valid = True
    tempList = []
    tempIndexes = []
    word = s.split(' ')
    #print len(word)
    for w in word:
        #print w
        if w in dictionary:
            tempIndexes.append( dictionary[ w ])
            tempList.append(word_vectors[dictionary[w]])
            #print len(tempList)
        else:
            valid = False
            num_sentence = num_sentence - 1
            #print len(tempList)
            break
    if(valid):
         listOfLines.append(tempList)
         listOfLineIndexes.append(tempIndexes)

f.close()
#print len(listOfLines)

#training_set = sentence(listOfLines, word_vectors)
size = num_sentence
shapes = 3 * 200

final_set = np.ndarray(shape = (size, shapes), dtype = float)

final_set = np.array(listOfLines, float)

perm = np.random.permutation( len( final_set ) )
index_80 = 0.8 * len( perm )
np.save( 'train', final_set[ perm[ : index_80 ] ])
np.save( 'test', final_set[ perm[index_80 :  ] ])





