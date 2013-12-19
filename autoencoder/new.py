import theano
from theano import tensor as T
import numpy

x = T.matrix('x')
w = T.matrix('w')
t = T.matrix('t')
 
y = T.dot(w, x)

error = ((t - y)**2).sum()# + 0.005 * (w ** 2).sum()

gradient = T.grad(error, [w])

f = theano.function([w, x, t], error)
f_prime = theano.function([w, x, t], gradient)

learning_rate = float(3.4e-14)
iterations = 10000

input = numpy.load('5_train.npy')
target = input[ : ][ 800 : 1000 ]
input = input[ : ][  : 800 ]
input = numpy.transpose(input)
target = numpy.transpose(target)
#print input.shape
input = numpy.array(input, numpy.float)
weight = numpy.random.random((200, 800))

#print target.shape
target = numpy.array(target, numpy.float)

for i in range(iterations):
    error = f(weight, input, target)
    errorgrad = f_prime(weight, input, target)
    errorgrad = numpy.array(errorgrad).reshape(200,800)
    #print errorgrad.shape
    weight -= errorgrad[ 0 ] * learning_rate
    print "training %i" % i
    print error
    #print '\n\n'
    #print "weight"
    #print weight
    #print '\n'



