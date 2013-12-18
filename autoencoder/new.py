import theano
from theano import tensor as T
import numpy

x = T.matrix('input')
w = T.matrix('weights')
t = T.matrix('target')

y = T.dot(w, x)

error = ((t - y)**2).sum() + 0.005 * (w ** 2).sum()

gradient = T.grad(error, [w])

f = theano.function([x, w, t], error)
f_prime = theano.function([x, w, t], gradient)

learning_rate = 0.1
iterations = 10

input = numpy.load('train_new.npy')
input = numpy.transpose(input)
#print input.shape
input = numpy.array(input, numpy.float)
weight = numpy.random.random((200, 400))
target = numpy.load('target.npy')
target = numpy.transpose(target)
#print target.shape
target = numpy.array(target, numpy.float)

for i in range(iterations):
    error = f(input, weight,target)
    errorgrad = f_prime(input, weight, target)
    errorgrad = numpy.array(errorgrad).reshape(200,400)
    #print errorgrad.shape
    weight -= errorgrad * learning_rate
    print "training"
    print error

print "weight"
print weight

