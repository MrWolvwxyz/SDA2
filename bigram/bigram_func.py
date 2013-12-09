import random

"""create the dictionary for unigram"""
F = open("priorProbs","r")
lines = F.readlines()
F.close

unigram = {}
for l in lines:
	l = l.split(' ')
	unigram[l[0]] = l[1].strip()

#print "unigram created"

"""create the dictionary for bigram"""
F = open("annotateBIG", "r")
lines = F.readlines()
F.close

#print "bigram created"

bigram = {}
for l in lines:
	l = l.split(':')
	bigram[l[0]] = l[1].strip()

def bigram_func(word1, word2):
	#print word1 
	#print word2

	choice1 = []
	choice2 = []
	for l in bigram:
    		if l.endswith(" "+word1):
			w = l.split(' ')
        		choice1.append(w[0])
    		if l.startswith(word2+" "):
			w = l.split(' ')
        		choice2.append(w[1])

	choice = set(choice1) & set(choice2)    

	prob1 = unigram[word1]

	result = {}
	for c in choice:
    		condition1 = c+" "+word1
    		prob2 = bigram[condition1]
    		condition2 = word2+" "+c
    		prob3 = bigram[condition2]
    		prob = float(prob1) + float(prob2) + float(prob3)
    		result[c] = prob
    
	sortedresult = sorted(result.iteritems(), key =lambda (k,v):(v,k), reverse = True)
       	#for r in sortedresult:
		#print r
	return sortedresult

F = open("input","r")
input = F.readlines()
F.close

F = open("output","w+")
#F.seek(0)
#F.truncate()

"""select the best k results"""
k = 10 

result = {}
for l in input:
	l = l.split('.')
	F.write(str(l[0])+'.'+'\n')
	word = l[0].split(' ')
	#print len(word)
	miss = random.randint(1,len(word)-2)
	F.write("the missing word is "+str(word[miss])+'. And the best '+str(k)+' results are: '+'\n')
	result  = bigram_func(word[miss-1], word[miss+1])
	if len(result) < k:
		#print "less than 10"
		for r in result:
			F.write(str(r[0])+'\n')
			#print "add one"
	if len(result) >= k:
		for r in result[:k]:
			F.write(str(r[0])+'\n')

F.close


