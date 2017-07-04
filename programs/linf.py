import math
def maxnorm(a,b):
	d=[]
	for i in range(0,len(a)):
		d.append(abs(a[i]-b[i]))
		
	return max(d)	
			
#1NN Classifier
dtr=raw_input("Enter your Training data:")#taking input training data set
f=open(dtr,'r')
val=[]
while True:#reading training patterns
	line = f.readline()
	if not line: 
		break
	X=line.split(",")		
	val.append(X)
f.close()

dtst=raw_input("Enter your Test data:")#taking input training data set
f=open(dtst,'r')
correct=0
tlen=0
while True:#reading training patterns
	line = f.readline()
	res=[]
	if not line: 
		break
	tlen+=1
	X=line.split(",")
	pcl=X[0]	#class of given training pattern
	X=map(float,X[1:])#getting time series points
	for i in val:
		acl=i[0]
		trtp=map(float,i[1:])
		ecval=maxnorm(X,trtp)
		#print "Training Pattern:",trtp,"\tTest Pattern:",X," Euclid Distance :",ecval
		if(len(res)!=0 and ecval<res[1]):
			#print "Yes"
			res=[acl,ecval]
		elif(len(res)==0):
			res=[acl,ecval]		
#	print "Predicted class : ",res[0]," Min Euclid Distance : ",res[1]," actual class :: ",pcl
	if(res[0]==pcl):
		correct+=1		
f.close()
print "No of correctly predicted examples:",correct," Accuracy:",((correct*1.0)/tlen)*100

