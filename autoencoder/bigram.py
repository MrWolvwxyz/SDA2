word1 = "the"
word2 = "girl"
print word1 
print word2

F = open("priorProbs", "r")
lines = F.readlines()
F.close

"""create the dictionary for unigram"""
unigram = {}
for l in lines:
    l = l.split(' ')
    unigram[l[0]] = l[1].strip()

F = open("annotateBIG", "r")
lines = F.readlines()
F.close

"""create the dictionary for bigram"""    
bigram = {}
for l in lines:
    l = l.split(':')
    bigram[l[0]] = l[1].strip()    

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
for s in sortedresult:
    print s

