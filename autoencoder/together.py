import os
import sys
import re
import scipy as sci
import numpy
import string
import cPickle as pickle
import gzip
import time

import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams

from dae_class import dA
from theano_class import theano_top

class sentence:

    #Instantiation function
    def __init__( self, word_list, word_vecs ):
        self.words = word_list
        self.size = len( word_list )
        #Maybe do one last check for non-alphanumerics here
        print self.words, self.size
        self.data = [ word_vecs[ dictionary[ word_list[ i ] ] ] for i in range( self.size ) ]

    def sent_print( self ):
        print self.size, self.words,  self.data, '\n'

    def get_size( self ):
        return self.size

"""
#hyperparameters we're currently not using
corruption_level = 0.2 #[ 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]
learning_rate = [ 0.1, 1, 10, 100, 1000 ]
batch_size = [ 1000.0, 2000.0, 3000.0, 5000.0 ]
weight_reg = [ 0.01, 0.03, 0.05, 0.1, 0.5, 1, 5, 10 ]
sparsity_param = [ 0.01, 0.03, 0.05, 0.1, 0.5, 1, 5, 10 ]
sparsity_penalty = [ 0.5, 1, 3, 5, 10 ]
"""
EPOCHS = 10
STOPPING_VALUE = 0.000001
NUM_VISIBLE = 600 #3 word sentences
NUM_HIDDEN = 0.5* NUM_VISIBLE
# parameters for calling dA function

"""
for sparse_penalty in sparsity_penalty:
    for size in batch_size:
        for weight_penalty in weight_reg:
            for rate in learning_rate:
                for sparsity2 in sparsity_param:
                    for corruption in corruption_level:
                        x = T.matrix('x')
                        rng = numpy.random.RandomState(123)
                        theano_rng = RandomStreams(rng.randint(2 ** 30))
                        autoencoder = dA( numpy_rng=rng, weight_reg=weight_penalty, sparsity = sparsity2,
                                    sp_penalty = sparse_penalty, theano_rng=theano_rng, input=x, n_visible=2000,
                                    n_hidden = 4000, sentence_length = 10 )


                        theanos = theano_top( autoencoder, STOPPING_VALUE, corruption, rate,
                                            '10_train.npy', '10_test.npy', size )

                        theanos.run_train( size, 10 )

                        theanos.run_test( size, EPOCHS )

"""
x = T.matrix('x')
rng = numpy.random.RandomState(123)
theano_rng = RandomStreams(rng.randint(2 ** 30))


#we will be using less hidden units than visible units
autoencoder = dA( numpy_rng=rng, weight_reg=0.085, sparsity = 0.05,
            sp_penalty = 0.03, theano_rng=theano_rng, input=x, n_visible=NUM_VISIBLE,
            n_hidden = NUM_HIDDEN, sentence_length = 10 )


theanos = theano_top( autoencoder, STOPPING_VALUE, 0.2, 10,
                    '10_train.npy', '10_test.npy', 5000.0 )

theanos.run_train( 5000.0, EPOCHS)

word_vectors = numpy.load( "" )
dictionary = pickle.load( open( "dictionary.p", 'r+' ) )

new_string = 's'

new_sentence = sentence( new_string.split(), word_vectors )

input_sentence = numpy.array( new_sentence.data, float ).reshape( 2000 )

theanos.get_results( input_sentence, numpy.array( [ 1, 0, 1, 1, 1, 0, 1, 1, 1, 1 ] ) )
