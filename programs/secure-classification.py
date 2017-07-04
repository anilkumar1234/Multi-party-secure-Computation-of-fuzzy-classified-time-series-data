import random
import sys
import time
start_time = time.clock()
#Training Phase
def train(dtr): 
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
                k=X[0]  #class of given training pattern
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
        #print len(meand['1']),len(meand['2'])
        return [mind,maxd,meand,cnt]

def classify(line,cnt,mind,maxd,meand,user):
        mu={}
        score={}
        Y=line.split(",")
        ac=Y[0]
        Y=Y[1:]
        n=len(Y)
        for k in cnt.keys():
                mu[k]=[0]*n
                score[k]=0
        for j in range(n):
                for k in cnt.keys():
                        tmp=float(Y[j])
                        #if(user=="B"):
                        #       print k,j,n
                        if(tmp<meand[k][j]):
                                mu[k][j]=1-((meand[k][j]-tmp)/(meand[k][j]-mind[k][j]))
                        else:
                                mu[k][j]=1-((tmp-meand[k][j])/(maxd[k][j]-meand[k][j]))
        for k in cnt.keys():
                for i in range(n):
                        score[k]+=mu[k][i]        
        return [score,ac]
def getScore(user):
        trn=raw_input("Enter User "+user+" train data:")
        tst=raw_input("Enter User "+user+" test data:")
        acs=[]
        tr=train(trn)
        mind=tr[0]
        maxd=tr[1]
        meand=tr[2]
        print user,len(meand['1']),len(meand['2'])
        cnt=tr[3]
        f=open(tst,'r')
        scores=[]
        while True:
                line = f.readline()
                if not line:
                        break
                tmp=classify(line,cnt,mind,maxd,meand,user)
                acs.append(tmp[1])
                scores.append(tmp[0])
        f.close()
        return [scores,acs,cnt]
class UserA():
                def init(self,n,alpha,beta,p):
                        self.n=n
                        self.p=p
                        self.alpha=alpha
                        self.beta=beta
                        self.x=0
                        m=[]
                        for i in range(2*n):
                                m.append([0]*2)
                        self.m=m
                def computeMi(self):
                        #M=input("Enter M:")
                        j=0
                        self.x=int(random.randrange(1,self.n-1))
                        for i in range((-self.n)+1,self.n+1):
                                self.m[j]=[0]*2
                                j+=1
                        j=0
                        for i in range((-self.n)+1,self.n+1):
                                self.m[j][0]=(self.M+i)-self.x
                                self.m[j][1]=int(random.randrange(2,10))
                                j+=1
                        return self.encryptMi()
                def encryptMi(self):
                        encrypt=[0]*len(self.m)
                        for i in range(len(self.m)):
                                encrypt[i]=[0]*2
                        for j in range(len(self.m)):
                                encrypt[j][0]=pow(self.alpha,self.m[j][1])
                                encrypt[j][1]=self.m[j][0]*pow(self.beta,self.m[j][1])
                        return encrypt
                def partialDecrypt(self,reEncrypted):
                        partialDecrypted=[0]*(2*self.n)
                        for i in range(2*n):
                                partialDecrypted[i]=[0]*2
                        for i in range(len(self.m)):                    
                                partialDecrypted[i][0]=reEncrypted[0]*pow(self.alpha,-(self.m[i][1]))
                                partialDecrypted[i][1]=reEncrypted[1]*pow(self.beta,-(self.m[i][1]))
                        return partialDecrypted
                def setM(self,M):
                        self.M=M
                def addX(self,partialSum):
                        return (partialSum+self.x)      
class UserB():
                def init(self,n,p):
                        self.n=n
                        self.p=p
                        self.alpha=int(random.randrange(2,10))
                        self.s=int(random.randrange(2,10))
                        self.beta=pow(self.alpha,self.s)
                def setN(self,N):
                        self.N=N
                def reEncrypt(self,encrypt):
                        #N=input("Enter N:")
                        reEncrypted=[0]*2
                        reEncrypted[0]=(encrypt[(self.n-1)+self.N][0])*pow(self.alpha,self.s)
                        reEncrypted[1]=(encrypt[(self.n-1)+self.N][1])*pow(self.beta,self.s)
                        return reEncrypted
                def fullyDecrypted(self,partiallyDecrypted):
                        t=partiallyDecrypted[(self.n-1)+self.N][1]
                        r=partiallyDecrypted[(self.n-1)+self.N][0]
                        mN=t*(r**-self.s)
                        return mN       

tmpa=getScore('A')
ascores=tmpa[0]
acs=tmpa[1]
cnt=tmpa[2]
tmpb=getScore('B')
bscores=tmpb[0]
precision=2
mul=pow(10,precision)
correct=0
n=79991
ubObj=UserB()
p=22801763489   
ubObj.init(n,p)
alpha=ubObj.alpha
beta=ubObj.beta
uaObj=UserA()   
uaObj.init(n,alpha,beta,p)
def secureSum(uaObj,ubObj,M,N):
        uaObj.setM(M)
        ubObj.setN(N)
        encrypt=uaObj.computeMi()
        #print "User B - Re-Encryption"
        reEncrypted=ubObj.reEncrypt(encrypt)
        #print "User A - Partial-Decryption"
        partiallyDecrypted=uaObj.partialDecrypt(reEncrypted)
        #print "User B - Full Decryption"
        partialSum=ubObj.fullyDecrypted(partiallyDecrypted)
        #print "User A - After Adding random number"
        result=uaObj.addX(partialSum)
        return result
def progressbar(perc, prefix="Progress:",size=100):
        #l=len(prefix)+(2*perc)+(size-perc)+4
        sys.stdout.write("\r%s[%s%s] %i/%i\r" % (prefix, "#"*perc, "."*(size-perc),perc,100))
        sys.stdout.flush()
        sys.stdout.write("\n")
        sys.stdout.flush()
rt=0
count=0
for i in range(len(ascores)):
        mem={}  
        for k in cnt.keys():
                mem[k]=0
        score={}
        y=len(ascores)*len(cnt.keys())
        for k in cnt.keys():
                #print rt
                score[k]=secureSum(uaObj,ubObj,int(ascores[i][k]*mul),int(bscores[i][k]*mul))/mul
                #score[k]=ascores[i][k]+bscores[i][k]
                rt+=1
                perc=rt%(y/100)
                if(perc==0):
                        count+=1
                        progressbar(count, "Progress: ")                        
        for k in cnt.keys():
                mem[k]=score[k]/(sum(score.values()))
        ac=acs[i]
        tmp=max(mem.values())
        for k in mem.keys():
                if(mem[k]==tmp):
                        pc=k
        if(pc==ac):
                correct+=1
tlen=len(ascores)
print "No.of Correctly Predicted Examples:",correct," Accuracy:",((correct*1.0)/tlen)*100,tlen  
print("--- %s seconds ---" % (time.clock() - start_time))
