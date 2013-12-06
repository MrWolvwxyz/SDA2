import os
import sys
import re
import scipy as sci
import numpy
import string
import cPickle
import gzip
import time

import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams

from dae_class import dA
from theano_class import theano_top

corruption_level = 0.2 #[ 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]
learning_rate = [ 0.1, 1, 10, 100, 1000 ]
batch_size = [ 1000.0, 2000.0, 3000.0, 5000.0 ]
testing_epochs = 10
weight_reg = [ 0.01, 0.03, 0.05, 0.1, 0.5, 1, 5, 10 ]
sparsity_param = [ 0.01, 0.03, 0.05, 0.1, 0.5, 1, 5, 10 ]
sparsity_penalty = [ 0.5, 1, 3, 5, 10 ]
stopping_condition = 0.000001
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
                        
                                        
                        theanos = theano_top( autoencoder, stopping_condition, corruption, rate,
                                            '10_train.npy', '10_test.npy', size )                
                                        
                        theanos.run_train( size, 10 )                
                                    
                        theanos.run_test( size, testing_epochs )                
                        
"""
x = T.matrix('x')
rng = numpy.random.RandomState(123)
theano_rng = RandomStreams(rng.randint(2 ** 30))
autoencoder = dA( numpy_rng=rng, weight_reg=0.05, sparsity = 0.05,
            sp_penalty = 3, theano_rng=theano_rng, input=x, n_visible=2000,
            n_hidden = 4000, sentence_length = 10 )     

                
theanos = theano_top( autoencoder, stopping_condition, 0.2, 10,
                    '10_train.npy', '10_test.npy', 1000.0 )                
                
theanos.run_train( 1000.0, 20 )                
            
theanos.run_test( 1000.0, testing_epochs )                
                                
                                                
                                                                
                                                                                
                                                                                                                