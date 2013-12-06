import os
import sys
import re
import numpy as np
import scipy as sci
import string

nonalphanum = "~`!@#$%^&*()_'+=-\][|}{;:\"/.,?><0123456789"

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
        
        
#Top level module that will be calling the rest of the scripts


#this is just a temp dictionary for testing, we will use the
#real dictionary for our implementation
f3 = open( "word_vectors.txt",'r' )
f3.flush()

lines = f3.readlines()
num_words = int( lines[ 0 ].split()[ 0 ] )
vec_size = int( lines[ 0 ].split()[ 0 ] )

dicVec = []
word_vectors = np.ndarray( shape = ( 71289, 200 ), dtype = float )
#hash initialization
dictionary = {}
index = 0
print 'here\n'
for line in lines[ 1 : ]:
    word = line.split()[0]
    usable_vec = map( float, line.split()[ 1 : ] )
    dicVec += [ word ]
    #hashmap that maps word(string) to index(int)(starts from 0)
    dictionary[word] = index
    
    #word_vectors can be indexed as an array using index[dictionary[word]]
    word_vectors[ index ] = map( float, line.split()[ 1 : ] )
    #print word_vectors
    index = index + 1
    print index

low = np.percentile( word_vectors, 0.5 )
high = np.percentile( word_vectors, 99.5 )
word_vectors = np.clip( word_vectors, low, high )
#min_word = np.amin( word_vectors )
#max_word = np.amax( word_vectors )
#word_vectors = ( word_vectors - min_word ) / ( max_word - min_word )

np.save( "word_vec_reg_array", word_vectors )
"""
np.save( "dictionary", dictionary )
np.save( "dictionary_vector", dicVec )

word_vectors = np.load( "word_vec_array.npy" )
"""
#list of list of words
lets = [ 'AA', 'AB', 'AC', 'AD' ]
nums = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
listOfLines = []
wiki_source = 'AA\wiki_01'

for let in lets:
    wiki_source = let + wiki_source[ 2 : ]
    if let != 'AD':
        print let
        for ii in range( 10 ):
            wiki_source = wiki_source[ : 8 ] + nums[ ii ] + wiki_source[ 9 : ]
            for i in range( 10 ):
               	wiki_source = wiki_source[ : 9 ] + nums[ i ]
               	#Splitting paragraphs into sentences here
               	f = open( 'new_text.txt', 'r+' )
               	f2 = open( wiki_source, 'r' )
               	for line in f2:
    		  for matchedtext in re.findall(r'(?<=\. ).*?(?=[.])', line ):
    		      matchedtext = re.sub( r'\([^)]*\)', '', matchedtext )
    		      if re.search( '[<>]', matchedtext ) == None:    
    		          f.write( matchedtext )
    		          f.write( '\n' )
    		#We want the lines written earlier by the paragraph splitter
           	#So we set that file back to the beginning and read dat shit
                f.seek( 0 )
                sentences = f.readlines()
                    
                #list of list of dictionary indices that correspond to words
                listOfLineIndices = []
                #Flag to make sure we only store words that are in our dictionary
                valid_sentence = True
                for line in sentences:
                    tempLineIndices = []
                    for i in line.split():
                        i = re.sub( r'[^\x00-\xff]', '', i )
                        i = i.translate( None, nonalphanum )
                        i = string.lower( i )
                        #Or here fix
                        if i in dictionary:
                            tempLineIndices.append( dictionary[ i ] )
                        else:
                            #-1 indicates that the word is not in the dictionary
                            valid_sentence = False
                            tempLineIndices.append( -1 )
                    if ( valid_sentence and ( len( line.split() ) > 1 ) and ( len( line.split() ) < 20 ) and ( string.find( string.ascii_uppercase, line[ 0 ] ) != -1 ) ):
                        listOfLines.append( map( string.lower, line.translate( None, nonalphanum ).split() ) )
               	        listOfLineIndices.append( tempLineIndices )
                    valid_sentence = True
                    
                f.truncate()
                f2.close()
    else:
       print let
       for ii in range( 5 ):
            wiki_source = wiki_source[ : 8 ] + nums[ ii ] + wiki_source[ 9 : ]
            for i in range( 10 ):
               	wiki_source = wiki_source[ : 9 ] + nums[ i ]
               	#Splitting paragraphs into sentences here
               	f = open( 'new_text.txt', 'r+' )
               	f2 = open( wiki_source, 'r' )
               	for line in f2:
            		  for matchedtext in re.findall(r'(?<=\. ).*?(?=[.])', line ):
            		      matchedtext = re.sub( r'\([^)]*\)', '', matchedtext )
            		      if re.search( '[<>]', matchedtext ) == None:    
            		          f.write( matchedtext )
            		          f.write( '\n' ) 
        		          
           	#We want the lines written earlier by the paragraph splitter
           	#So we set that file back to the beginning and read dat shit
                f.seek( 0 )
                sentences = f.readlines()
                    
                #list of list of dictionary indices that correspond to words
                listOfLineIndices = []
                #Flag to make sure we only store words that are in our dictionary
                valid_sentence = True
                for line in sentences:
                    tempLineIndices = []
                    for i in line.split():
                        i = re.sub( r'[^\x00-\xff]', '', i )
                        i = i.translate( None, nonalphanum )
                        i = string.lower( i )
                        #Or here fix
                        if i in dictionary:
                            tempLineIndices.append( dictionary[ i ] )
                        else:
                            #-1 indicates that the word is not in the dictionary
                            valid_sentence = False
                            tempLineIndices.append( -1 )
                    if ( valid_sentence and ( len( line.split() ) > 1 ) and ( len( line.split() ) < 20 ) and ( string.find( string.ascii_uppercase, line[ 0 ] ) != -1 ) ):
                        listOfLines.append( map( string.lower, line.translate( None, nonalphanum ).split() ) )
               	        listOfLineIndices.append( tempLineIndices )
                    valid_sentence = True
                    
                f.truncate()
                f2.close()
                    #line_mat = sci.array( listOfLines )
                    #ind_mat = sci.array( listOfLineIndices )

#print listOfLines
#print listOfLineIndices
#print line_mat.shape, ind_mat.shape

print len( listOfLines )

#Or here for the fix
#This is a list of sentence objects for each sentence in the wiki_nn files
training_set = [ sentence( listOfLines[ i ], word_vectors ) for i in range( len( listOfLines ) ) ] 

#This will be a list of lists of sentences where training_buckets[ 0 ] will be
#all sentences of size 2, etc. to training_buckets[ 17 ]
training_buckets = [ [ training_set[ 0 ] ] ]

for i in range( 17 ):
	training_buckets.append( [ training_set[ 0 ] ] )

for example in training_set:
	training_buckets[ example.get_size() - 2 ].append( example )

for i in range( 18 ):
	training_buckets[ i ].pop( 0 )
	
sizes = [ len( training_buckets[ i ] ) for i in range( 18 ) ]

shapes = [ ( 200 * ( i + 2 ) ) for i in range( 18 ) ]

for i in range( len( sizes ) ):
	print sizes[ i ], shapes[ i ]
	
final_set = [ np.ndarray( shape = ( sizes[ i ], shapes[ i ] ), dtype = float ) for i in range( 18 ) ]

for i in range( 18 ):
        for j in range( len( training_buckets[ i ] ) ):
	   final_set[ i ][ j, : ] = np.array( training_buckets[ i ][ j ].data, float ).reshape( ( i + 2 ) * 200 )


for i in xrange(18):
	perm = np.random.permutation( len( final_set[ i ] ) )
	index_80 = 0.8 * len( perm )
	index_20 = 0.2 * len( perm )
	np.save( '%i_train' %(i + 2), final_set[ i ][ perm[ : index_80 ] ] )
	np.save( '%i_test' %(i + 2), final_set[ i ][ perm[ index_80 : ] ] )
	



