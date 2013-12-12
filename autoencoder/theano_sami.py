import os
import sys
import re
import scipy as sci
import string
import math
import cPickle as pickle
import gzip
import datetime

import time

import numpy

import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams
from theano import pp
import dae_class



class theano_top:

    def __init__( self, da, stop_val, corruption, rate, train_path, test_path, batch_size,epochs ):
        #self.fid = open( 'output.txt', 'r+' )
        self.model = da
        self.stop_val = stop_val
        self.last_cost = 9999
        self.train_path = train_path
        self.test_path = test_path

        self.train_set = numpy.load( train_path )
        self.test_set = numpy.load( test_path )

        shared_train = theano.shared( self.train_set )
        self.shared_test = theano.shared( self.test_set )
        self.print_set( "train_set", shared_train )
        self.print_set( "test_set", self.shared_test )

        self.learning_rate = rate
        self.corruption_level = corruption
        self.the_batch = batch_size
        self.the_epochs = epochs

        start_index = T.lscalar()
        end_index = T.lscalar()
        cost, updates = da.get_cost_updates( corruption, rate, batch_size )
        print "update"

        train = theano.function( [ start_index, end_index ], cost, updates = updates,
            givens = { da.x : shared_train [ start_index : end_index ] } )
        print start_index
        print end_index
        print "train"
        self.test = theano.function( [], cost,
            givens = { da.x : self.shared_test } )

        #num_train_batches = math.ceil( float(len( self.train_set ) ) / float( batch_size ) )
        num_train_batches = math.ceil( len( self.train_set ) / batch_size )
        print
        start_time = time.clock()
        train_size = len( self.train_set )
        print  batch_size, num_train_batches, train_size
        #for epoch in xrange( epochs ):
        epoch = 0
        print "before epoch while"
        while epoch < epochs:
            c = []
            c2 = []
            for ind in xrange( int( num_train_batches ) ):
                #print ind
                start = ind * batch_size
                end = start + batch_size
                if end > train_size: end = train_size
                c.append( train( start, end ) )
            #numpy.save( time.strftime("%Y-%m-%d-%H:%M:%S") + str( epoch ) + 'cost', c )
            print 'Training epoch %d, cost ' % epoch, numpy.mean( c )
            c2.append( self.test() )
            print 'Testing epoch %d, cost ' % epoch, numpy.mean( c2 )
            epoch = epoch + 1
            if numpy.mean( c ) > self.last_cost:
                self.learning_rate = self.learning_rate / 2
            self.last_cost = numpy.mean( c )
            if numpy.mean( c ) <= self.stop_val:
                print ( time.clock() - start_time )
                #numpy.save( 'weights1_train', self.model.W.get_value() )
                #numpy.save( 'bias1_train', self.model.b.get_value() )
                #numpy.save( 'bias2_train', self.model.b_prime.get_value() )
                return
        #self.print_parts()
        print ( time.clock() - start_time )
        #numpy.save( 'weights1_train', self.model.W.get_value() )

    def print_set(self, name, data):
        with open( name + ".txt", "w+") as handle:
            print >>handle, "# type(python)", type(data)
            print >>handle, "# type(theano)", data.type
            print >>handle, "# dimensions  ", data.ndim
            if data.ndim == 2:
                print >>handle, "# rows(numpy) ", len(data.get_value())
                print >>handle, "# cols(numpy) ", len(data.get_value()[0])
                for row in theano.function([], data)():
                    for val in row:
                        print >>handle, "%0.3f" % val,
                    print >>handle
            elif data.ndim == 1:
                for row in theano.function([], data)():
                    print >>handle, "%d" % row
            else:
                return

    def print_parts( self ):

        self.print_set( "weights", self.model.W )
        self.print_set( "weights_prime", self.model.W_prime)
        self.print_set( "bias", self.model.b )


    def get_results( self, sentence_vector, missing_word_inds ):
        self.print_parts()
        corrupted_sentence = sentence_vector * missing_word_inds.repeat( 200 )
        hidden_activations = self.model.get_hidden_values( corrupted_sentence )
        output = self.model.get_reconstructed_input( hidden_activations )
        f = open( "word_vectors.txt", 'r' )
        lines = f.readlines()

        f2 = open( "word_vectors_test.txt", 'w' )
        for line in lines:
                 f2.write( line )
        num_corrupted = 0
        for i in range( len( missing_word_inds ) ):
           if missing_word_inds[ i ] == 0:
               line = ( "my_vector_%d " % num_corrupted )
               num_corrupted = num_corrupted + 1
               for row in theano.function([], output[ 200 * i : 200 * ( i + 1 ) ] )():
                   row = ( row - 1 ) * 2
                   line += ( str( row ) + " " )
               f2.write( line + '\n' )
