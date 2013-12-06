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
    
    def __init__( self, da, stop_val, corruption, rate, train_path, test_path, batch_size ):
        self.fid = open( 'output.txt', 'r+' )
        self.model = da
        self.stop_val = stop_val
        self.last_cost = 9999
        self.train_path = train_path
        self.test_path = test_path
        
        self.train_set = numpy.load( train_path )
        self.test_set = numpy.load( test_path )
        
        self.shared_train = theano.shared( self.train_set )
        self.shared_test = theano.shared( self.test_set )
        self.print_set( self.shared_train, "train_set" )
        self.print_set( self.shared_test, "test_set" )
        
        self.learning_rate = rate
        self.corruption_level = corruption
        
        self.start_index = T.lscalar()
        self.end_index = T.lscalar()
        self.cost, self.updates = da.get_cost_updates( corruption, rate, batch_size )
        
        self.train = theano.function( [ self.start_index, self.end_index ], self.cost, updates = self.updates,
            givens = { da.x : self.shared_train [ self.start_index : self.end_index ] } )
        self.test = theano.function( [ self.start_index, self.end_index ], self.cost, updates = self.updates,
            givens = { da.x : self.shared_test [ self.start_index : self.end_index ] } )
    
        
    def print_set(self, data, name):
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
        #tilde_x = self.model.get_corrupted_input(self.model.x, self.corruption_level)
        #y = self.model.get_hidden_values(tilde_x)
        #z = self.model.get_reconstructed_input(y)
        
        #thing1 = ( 1.00 / ( 2450 * self.model.n_visible ) ) * T.sum( 0.5 *
        #                                (self.model.x - z) ** 2, axis = 1) + self.model.weight_reg * T.sum( self.model.W )
        #self.print_set( thing1, "sum_axis1" )
        #thing2 = ( 1.00 / ( 2450 * self.model.n_visible ) ) * T.sum( 0.5 *
        #                                (self.model.x - z) ** 2) + self.model.weight_reg * T.sum( self.model.W )
        
        #self.print_set( thing2, "sum" )
        
        
        self.print_set( self.model.W, "corruption:" + str( self.corruption_level ) + time.strftime( " %Y-%m-%d-%H:%M:%S") + " weights" )
        self.print_set( self.model.b, "corruption:" + str( self.corruption_level ) + time.strftime( " %Y-%m-%d-%H:%M:%S") + " bias" )
        
        #self.fid.write( til_printed )
        #self.fid.write( ' \n\n\n' )
        
        #self.fid.write( y_printed )
        #self.fid.write( ' \n\n\n' )
        
        #self.fid.write( z_printed )
        #self.fid.write( ' \n\n\n' )
        
        #self.fid.write( self.start_index )
        #self.fid.write( ' \n\n\n' )
        
        #self.fid.write( self.end_index )
        #self.fid.write( ' \n\n\n' )
        
            
    def run_train( self, batch_size, epochs ):
        #num_train_batches = math.ceil( float(len( self.train_set ) ) / float( batch_size ) )
        num_train_batches = math.ceil( len( self.train_set ) / batch_size )
        start_time = time.clock()
        train_size = len( self.train_set )
        print  batch_size, num_train_batches, train_size
        #for epoch in xrange( epochs ):
        epoch = 0
        while epoch < epochs:
            c = []
            for ind in xrange( int( num_train_batches ) ):
                #print ind
                start = ind * batch_size
                end = start + batch_size
                if end > train_size: end = train_size
                c.append( self.train( start, end ) )
            #numpy.save( time.strftime("%Y-%m-%d-%H:%M:%S") + str( epoch ) + 'cost', c )
            print 'Training epoch %d, cost ' % epoch, numpy.mean( c )
            epoch = epoch + 1
            if numpy.mean( c ) > self.last_cost:
                self.learning_rate = self.learning_rate / 2
            self.last_cost = numpy.mean( c )
            if numpy.mean( c ) <= self.stop_val: return
        #self.print_parts()
        print ( time.clock() - start_time )
        with open( "autoencoder_train.obj", 'wb' ) as output:
            pickle.dump( self.model, output )
        
            
    def run_test( self, batch_size, epochs ):
        #num_train_batches = math.ceil( float(len( self.train_set ) ) / float( batch_size ) )
        num_test_batches = math.ceil( len( self.test_set ) / batch_size )
        start_time = time.clock()
        test_size = len( self.test_set )
        print  batch_size, num_test_batches, test_size
        for epoch in xrange( epochs ):
            c = []
            for ind in xrange( int( num_test_batches ) ):
                start = ind * batch_size
                end = start + batch_size
                if end > test_size: end = test_size
                c.append( self.train( start, end ) )
            #numpy.save( time.strftime("%Y%m%d-%H%M%S") + str( epoch ) + 'cost', c )
            print 'Testing epoch %d, cost ' % epoch, numpy.mean( c )
        #self.print_parts()
        print ( time.clock() - start_time )    
        with open( "autoencoder_test.obj", 'wb' ) as output2:
            pickle.dump( self.model, output2 )
        
        
        
        
        
        
