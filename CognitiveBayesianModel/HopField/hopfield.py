import numpy as np
from joblib import Parallel,delayed
import time
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
invlogistic = lambda a,b: 1/(1+np.exp(-a*b))

def updateRule(patterns,W):
    W += (patterns.T.dot(patterns))
    np.fill_diagonal(W,0)
    return W

def makePattern(person,triplet):
    temp = np.zeros((1+6)*5)
    temp[person*7] = 1
    for i in range(1+triplet*3,1+triplet*3+3):
        temp[person*7+i] = 1
    return temp

def makeRecall(person,triplet,item,bw):
    temp = np.zeros((1+6)*5)
    p = person*7
    selectp = p
    if item == 0:
        clue = 1.1
    else:
        clue = 1
    # Set activity
    temp[p+1+3*triplet] = 1
    # Set Item. If item == 0 (social), heightened activity
    temp[p+1+3*triplet + 1 + item] = clue
    # Select which foil triplet
    selectt = triplet^1
    if not bw:
        temp[p+1+3*(selectt) + 1 + item] = clue
    else:
       # Select foil person
       selectp = np.arange(5)[np.arange(5)!= person][np.random.randint(4)]*7
       selectt = (triplet^(np.random.randint(2)))
       temp[selectp + 1 + 3*(selectt) + 1 + item] = clue
#    temp[-1-item] = 1
#    temp[-1-item^1] = -1
#    temp[-3] = 1
    return temp,selectp//7,selectt
    
def checkRecall(Z,person,triplet,item,selectp,selectt):
    p= person*7
    foilp = selectp*7
    true = Z[p+1+3*triplet + 1 + item]
    foil = Z[foilp+1+3*selectt + 1 + item]
    if item == 0:
        scale = 10
    if item == 1:
        scale = 8.5
    ret = np.clip((invlogistic(true - foil,scale)),a_min=0.5,a_max=0.95)
    return ret

def patternComplete(X,Y,W,its):
    oldY = Y
    for i in range(its):
        Y = (Y.dot(W) + X)
        if ((oldY - Y)**2).sum() < 1e-20:
            break
        oldY = Y
    return Y,i

def run(R):
    patterns = [[makePattern(p,t) for p in range(5)] for t in range(2)]
    patternr = np.array(patterns).reshape(-1,1,(1+6)*5)
    patternsr = np.concatenate([patternr[np.random.permutation(10)] for i in range(2)],0)
    carry = np.zeros((1,(1+6)*5))
    W = np.zeros(((1+6)*5,(1+6)*5))
    for p in patternsr:
        p = np.logical_or(p,carry)
        W = updateRule(p,W)
        carry = np.copy(p)
        carry[carry == 1] = np.random.binomial(1,0.2,size=np.sum(carry).astype(int))
    W /= 20
    X,selectp,selectt = zip(*[makeRecall(p,t,i,b) for p in range(5) for t in range(2) for i in range(2) for b in range(2)])
    item = [2*b+i for p in range(5) for t in range(2) for i in range(2) for b in range(2)]
    truep,truet,truei,trueb = zip(*[[p,t,i,b] for p in range(5) for t in range(2) for i in range(2) for b in range(2)])
    X = np.array(X)
    Y = np.zeros_like(X)
    Z = []
    nIts = [[],[],[],[]]
    D = [[],[],[],[]]
    for x,y,i,sp,st,tp,tt,ti in zip(X,Y,item,selectp,selectt,truep,truet,truei):
        z,its = patternComplete(x,y,W,100)
        d = checkRecall(z,tp,tt,ti,sp,st) 
        D[i] += [d]
        nIts[i] += [np.log(its)]
        Z += [z]
    #print(np.mean(nIts,-1),np.std(nIts,-1))
    Z = np.array(Z)
    plt.close('all')
    fig,ax = plt.subplots(1,3)
    ax[0].imshow(X)
    ax[1].imshow(Z)
    ax[2].imshow(W)
    plt.savefig("Recall_"+str(R))
    return Z,W,patterns,X,selectp,selectt,item,nIts,D
L = []
for i in range(100):
    L += [run(i)]
Z,W,patterns,X,p,t,item,nIts,D = zip(*L)#run()

np.save("Iterations",nIts)
np.save("Recall",D)
np.save("Items",item)
np.save("rBinomial",np.random.binomial(1,D))
#Res = (Parallel(n_jobs=40)(delayed(run) for k in range(40)))
PnIts = np.array(nIts).mean(-1)
PD = np.array(D).mean(-1)
import scipy.stats as stats
print(stats.ttest_rel(PnIts[:,0],PnIts[:,1]))
print(stats.ttest_rel(PnIts[:,2],PnIts[:,3]))
print(stats.ttest_rel(PD[:,0],PD[:,1]))
print(stats.ttest_rel(PD[:,2],PD[:,3]))
