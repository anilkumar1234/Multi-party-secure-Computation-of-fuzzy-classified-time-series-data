#Training Phase
dtr=raw_input("Enter your Training data:")#taking input training data set
f=open(dtr,'r')
mind={}
maxd={}
totald={}
meand={}
cnt={}
n=0
while True:#reading training patterns
	line = f.readline()
	if not line: 
		break
	X=line.split(",")
	k=X[0]	#class of given training pattern
	X=X[1:]#getting time series points
	n=len(X)#time series length
	if(k in cnt.keys()):#list of classes
		cnt[k]+=1
		for j in range(n):#iterating over fields
			tmp=float(X[j])
			mind[k][j]=min(tmp,mind[k][j])						
			maxd[k][j]=max(tmp,maxd[k][j])
			totald[k][j]=totald[k][j]+tmp
	else:
		cnt[k]=1
		mind[k]=map(float,X)
		maxd[k]=map(float,X)
		totald[k]=map(float,X)
		meand[k]=map(float,[1]*n)
		#print "At initial:",mind
for k in cnt.keys():
	for j in range(n):#calculating mean values
		meand[k][j]=(totald[k][j])/cnt[k]
f.close()
#ouput of phase 1
#print "\t\tMin Max Mean"
#for k in cnt.keys():
#	print "Class:",k,mind[k]," ",maxd[k]," ",meand[k]
#classification phase
dtst=raw_input("Enter your Test data:")#getting test data set
f=open(dtst,'r')

correct=0#initializing variables
#preparing for classification

# in classification phase ,at initial time
#for k in cnt.keys():
#	print "Mu:",mu
#	print "Score:",score
#	print "Mem:",mem
tlen=0
while True:#reading test patterns
	mu={}
	score={}
	mem={}
	line = f.readline()	
	if not line: 
		break
	tlen+=1
	Y=line.split(",")
	ac=Y[0]	
#	print "Actual class:",ac
	Y=Y[1:]
	n=len(Y)
	for k in cnt.keys():
		mu[k]=[0]*n
		score[k]=0
		mem[k]=0
	#print "Analyzing test pattern...",Y," of class ",ac
	for j in range(n):
		for k in cnt.keys():
			tmp=float(Y[j])
			if(tmp<meand[k][j]):#calculating membership of j'th dimension of class k
				mu[k][j]=1-((meand[k][j]-tmp)/(meand[k][j]-mind[k][j]))
			else:
				mu[k][j]=1-((tmp-meand[k][j])/(maxd[k][j]-meand[k][j]))
	#print "Mu values for test pattern:"
#	for k in cnt.keys():
#		print "Class ",k," :",mu[k]
	for k in cnt.keys():
		for i in range(n):
			score[k]+=mu[k][i]
	for k in cnt.keys():
		mem[k]=score[k]/(sum(score.values()))#calculating membership value of class k
	#print "Score values for given pattern:"
	#for k in mem.keys():
	#	print "Class ",k," :",score[k]
	tmp=max(mem.values())
	for k in mem.keys():
		#print k,mem[k]
		if(mem[k]==tmp):
			pc=k
#	if(pc==""):
#		print "Error"
	#print "Predicted class:",pc,ac
	if(pc==ac):
#		print "Predicted class and Actual class are same"
		correct+=1
#	else:
#		print "Predicted class and Actual class are not same"
#	print
#	print
#	print
f.close()
print "No.of Correctly Predicted Examples:",correct," Accuracy:",((correct*1.0)/tlen)*100,tlen
