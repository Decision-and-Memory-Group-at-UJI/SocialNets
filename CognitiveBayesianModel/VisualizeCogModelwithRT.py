import jax.numpy as jnp
import jax.scipy.stats as jstats
from sklearn.metrics import roc_curve,roc_auc_score
import scipy.stats as stats
import jax
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({"font.size":12})
matplotlib.use("agg")
import pickle
import arviz as az

with open('Posterior_EpStrAltActCovDirRTBDP.pkl', 'rb') as f:
    data = pickle.load(f)
data = jax.tree_map(lambda x: x[:,::1],data)

invlogit = lambda x: 1/(1+jnp.exp(-x))
CoVul = lambda x,a,b: a + (b-a)*invlogit(x)
CoV = lambda x: jnp.exp(x)
simpnorm = lambda a,b,N: stats.norm.ppf(np.linspace(1e-3,1-1e-3,N))*b + a
simpcauchy = lambda a,b,N: stats.cauchy.ppf(np.linspace(1e-3,1-1e-3,N))*b + a
Res = np.concatenate([np.load("Perdistrep1Collect.npy"),np.load("Perdistrep2Collect.npy")[:,::-1]],0)
Ranks = np.concatenate([np.load("PerRankingrep1.npy"),np.load("PerRankingrep2.npy")[:,::-1]],0).transpose(0,2,1)
RT = Res[:,:,-2].astype(float)
Confidence = Res[:,:,-3].astype(float)
Persons = Res[...,-4,:]
Dists = Res[...,-1,:]
Social = Res[...,0,:]
RunsDist = [[[np.unique(Dists[k,j][Persons[k,j]==i]).squeeze() for i in range(5)] for j in range(2)] for k in range(Dists.shape[0])]
obs = Res[:,:,0]
Social = Res[:,:,1]
Episode = Res[:,:,2]
EpSoc = 2*Social + Episode
RConfs = [[[] for j in range(4)] for i in range(2)]
for i in range(Dists.shape[0]):
    for j in range(2):
        for k in range(4):
            if k < 2:
                RConfs[j][k].append(Confidence[i,j][Social[i,j]==k].mean())
            else:
                RConfs[j][k].append(Confidence[i,j][Episode[i,j]==k-2].mean())
RankConf = np.array(RConfs).transpose(2,0,1)/Confidence.mean(-1,keepdims=True)
ConfM = Confidence.mean(-1,keepdims=True)
RRTs = [[[] for j in range(4)] for i in range(2)]
for i in range(Dists.shape[0]):
    for j in range(2):
        for k in range(4):
            if k < 2:
                RRTs[j][k].append(RT[i,j][Social[i,j]==k].mean())
            else:
                RRTs[j][k].append(RT[i,j][Episode[i,j]==k-2].mean())
RankRT = np.array(RRTs).transpose(2,0,1)/RT.mean(-1,keepdims=True)
RRTs = [[[[] for k in range(2)] for j in range(2)] for i in range(2)]
for i in range(Dists.shape[0]):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                RRTs[j][k][l] += [RT[i,j][EpSoc[i,j]==k+2*l]]
RTsep = np.array(RRTs).transpose(3,0,1,2,4)[...,None,:]#/RT.mean(-1,keepdims=True)
RTM = RT.mean(-1,keepdims=True)
weight = CoV(data.position['weightS'])#*CoV(data.position['weightPS'][:,:,None,None])
wT = weight
tNDS = RTsep - (CoVul(data.position['tNDS'][...,None],0,1)*np.median(RT,-1,keepdims=True)[...,None])[...,None,None]
corRT = CoVul(tNDS*wT[...,None,None,:,None],-1,1)

def makeCov2(A,B):
    A01 = jnp.sqrt(A[0]*A[1])
    A02 = jnp.sqrt(A[0]*A[2])
    A12 = jnp.sqrt(A[1]*A[2])
    a = A[0]
    b = B[0]*A01
    c = B[1]*A02
    d = B[2]*A01
    e = A[1]
    f = B[3]*A12
    g = B[4]*A02
    h = B[5]*A12
    i = A[2]
    return jnp.array([[a,b,c],[d,e,f],[g,h,i]])
data.position['VarCritS'] = CoVul(data.position['VarCritS'],0,1)
corRT2 = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(makeCov2,in_axes=[None,-1]),in_axes=[None,-3]),in_axes=[None,-4])))))(data.position['VarCritS'][...,None].repeat(3,axis=-1),corRT)
print(az.summary({"corrRT":corRT.mean((2,3,-2))}))

az.plot_trace({"corrRT":corRT.mean((2,3,-2))[...,:2]})
plt.savefig("corrRTSocial_Trace")
plt.close('all')
az.plot_trace({"corrRT":corRT.mean((2,3,-2))[...,2:4]})
plt.savefig("corrRTNonSocial_Trace")
plt.close('all')
lowPostProbaz = az.convert_to_inference_data(np.array(jnp.nanmean(corRT2,(2,3,-3))[:,:,0,0,0]))
highPostProbaz = az.convert_to_inference_data(np.array(jnp.nanmean(corRT2,(2,3,-3))[:,:,1,0,1]))
higherPostProbaz = az.convert_to_inference_data(np.array(jnp.nanmean(corRT2,(2,3,-3))[:,:,2,0,2]))
fig,ax = plt.subplots(3,1,sharex=True)
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial',],shade=0.2,ax=ax)
plt.tight_layout()
plt.savefig("CorrwithRT")
plt.close('all')

axNoneSocialS = (data.position['axNonSocialS']*data.position['axNonSocialPS'][...,None])
axSocialS = (data.position['axSocialS']*data.position['axSocialPS'][...,None])
axActS = (data.position['axActS']*data.position['axActPS'][...,None])
olddirectionS = jnp.concatenate([axSocialS[...,None],axNoneSocialS[...,None],axActS[...,None]],-1)
directionS = jnp.exp(jnp.concatenate([axSocialS[...,None],axNoneSocialS[...,None],axActS[...,None]],-1))
directionS = (directionS/(directionS**2).sum(-1,keepdims=True))+1e-10
print(az.summary({"Direction":(jnp.log(directionS[...,0])-jnp.log(directionS[...,1]))}))#[...,0]/directionS[...,1])}))
az.plot_trace({"Direction":(jnp.log(directionS[...,0])-jnp.log(directionS[...,1]))})#[...,0]/directionS[...,1])})
plt.savefig("Direction_Trace")
plt.close('all')

def makeCov(A,B):
    a = A[0]
    b = B[0]*jnp.sqrt(A[0]*A[1])
    c = B[1]*jnp.sqrt(A[0]*A[2])
    d = b
    e = A[1]
    f = B[2]*jnp.sqrt(A[1]*A[2])
    g = c
    h = f
    i = A[2]
    return jnp.array([[a,b,c],[d,e,f],[g,h,i]])
def fastinv(M):
    a,b,c,d,e,f,g,h,i = M.ravel()
    A = (e*i - f*h)
    B = -(d*i - f*g)
    C = (d*h - e*g)
    D = -(b*i-c*h)
    E = a*i -c*g
    F = -(a*h - b*g)
    G = b*f - c*e
    H = -(a*f-c*d)
    I = a*e - b*d
    detM = a*A + b*B + c*C
    return jnp.array([[A,D,G],[B,E,H],[C,F,I]])/(detM)
def fastinv22(M):
    a,b,c,d = M.ravel()
    detM = a*d - b*c
    return jnp.array([[d,-b],[-c,a]])/(detM)
def det22(M):
    a,b,c,d = M.ravel()
    detM = a*d - b*c
    return detM 
def KL(A,B,BP):
    return .5*(jnp.log(det22(B)) - jnp.log(det22(A)) -2 +jnp.diag(BP.dot(A)).sum())
CovWIS = CoVul(data.position['CovWIS'],0,1)
CovBWS = CoVul(data.position['CovBWS'],0,1)
VarWIS = CoV(data.position['VarWIS'])
VarBWS = CoV(data.position['VarBWS'])

EWIS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: fastinv(makeCov(a,b)),in_axes=[-1,None],out_axes=-1)))))(VarWIS,CovWIS).mean(-1)
SNSWIS = EWIS[...,:2,:2]
SAWIS = EWIS[...,[0,0,2,2],[0,2,0,2]].reshape(*EWIS.shape[:-2],2,2)
NSAWIS = EWIS[...,[2,2,1,1],[2,1,2,1]].reshape(*EWIS.shape[:-2],2,2)
PSNSWIS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(fastinv22))))(SNSWIS)
PSAWIS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(fastinv22))))(SAWIS)
PNSAWIS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(fastinv22))))(NSAWIS)
KLSAWI = jax.vmap(jax.vmap(jax.vmap(jax.vmap(KL))))( NSAWIS,SNSWIS,PSNSWIS)
KLNSAWI = jax.vmap(jax.vmap(jax.vmap(jax.vmap(KL))))(SAWIS ,SNSWIS,PSNSWIS)

EBWS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: fastinv(makeCov(a,b)),in_axes=[-1,None],out_axes=-1)))))(VarBWS,CovBWS).mean(-1)
SNSBWS = EBWS[...,:2,:2]
SABWS = EBWS[...,[0,0,2,2],[0,2,0,2]].reshape(*EBWS.shape[:-2],2,2)
NSABWS = EBWS[...,[2,2,1,1],[2,1,2,1]].reshape(*EBWS.shape[:-2],2,2)
PSNSBWS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(fastinv22))))(SNSBWS)
PSABWS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(fastinv22))))(SABWS)
PNSABWS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(fastinv22))))(NSABWS)
KLSABW = jax.vmap(jax.vmap(jax.vmap(jax.vmap(KL))))( NSABWS,SNSBWS,PSNSBWS)
KLNSABW = jax.vmap(jax.vmap(jax.vmap(jax.vmap(KL))))(SABWS ,SNSBWS,PSNSBWS)
lowPostProbaz = az.convert_to_inference_data( np.nanmean(np.array(jnp.concatenate((KLSAWI [...,None],KLSABW[...,None]),-1)),(2,3,)))
highPostProbaz = az.convert_to_inference_data(np.nanmean(np.array(jnp.concatenate((KLNSAWI[...,None],KLNSABW[...,None]),-1)),(2,3)))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.savefig("KLBW_Trace")
plt.close('all')


PPred = data.position['posteriorPredictive']
data.position['PosteriorProb'] = data.position['PosteriorProb'][...,:2,:,:]
PosteriorProb = data.position['PosteriorProb']
data.position['postMuP'] = data.position['postMu'].mean((2,3,))
data.position['Symmetry'] = data.position['NpostVar']/data.position['SpostVar'][...,None,:]
data.position['Symmetry'] = data.position['Symmetry'][...,1,:].mean(-1).reshape(8,data.logdensity.shape[1],ConfM.shape[0],3,2)
data.position['Separation'] = -(data.position['SpostMu'][...,None,:]-data.position['NpostMu'])/data.position['SpostVar'][...,None,:]
data.position['Separation'] = data.position['Separation'].mean(-1).reshape(8,data.logdensity.shape[1],ConfM.shape[0],3,4)
data.position['CovWIS'] = CoVul(data.position['CovWIS'],0,1)*2-1
data.position['CovBWS'] = CoVul(data.position['CovBWS'],0,1)*2-1
interWI = jnp.concatenate((data.position['VarWIS'],data.position['CovWIS'][...,None]),-1)
interBW = jnp.concatenate((data.position['VarBWS'],data.position['CovBWS'][...,None]),-1)

transformCov = lambda x: (x)
lowPostProbaz = az.convert_to_inference_data( np.array(-((jnp.median(transformCov(data.position['CovWIS'][...,0,:]),(2,3,))))))
highPostProbaz = az.convert_to_inference_data(np.array(-((jnp.median(transformCov(data.position['CovBWS'][...,0,:]),(2,3,))))))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Within','Between'],shade=0.2)
plt.tight_layout()
plt.savefig("Corr_Trace.png")
Covs = jnp.concatenate((data.position['CovWIS'][...,1:,None],data.position['CovBWS'][...,1:,None]),-1)
lowPostProbaz = az.convert_to_inference_data( np.array(-((jnp.median(transformCov(Covs[...,0,:]),(2,3,))))))
highPostProbaz = az.convert_to_inference_data(np.array(-((jnp.median(transformCov(Covs[...,1,:]),(2,3,))))))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.tight_layout()
plt.savefig("CorrAct_Trace.png")

data.position['postVarP'] = data.position['postVar'].mean((2,3,))
data.position['muS'] = jnp.ones_like(data.position['postMu'])#data.position['muS'][...,None].repeat(2,axis=-1)
data.position['muPM'] = jnp.ones_like(data.position['postMuP'])#[...,None,None].mean((2,3,-1,-2))
data.position['sigS'] = 2*jnp.ones_like(data.position['postVar'])#data.position['sigS'][...,None].repeat(2,axis=-1)
data.position['sigPM'] = 2*jnp.ones_like(data.position['postVarP'])#[...,None,None].mean((2,3,-1,-2))
data.position['diffMu'] = data.position['postMuP'] - data.position['muPM']
data.position['diffVar'] = data.position['postVarP']/data.position['sigPM']
data.position['PriorProb'] = jstats.norm.cdf(0,loc=data.position['muS'][...],scale=data.position['sigS'][...])
data.position['PriorCDF'] = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: jstats.norm.cdf((jnp.arange(-3,3,0.5)-a)/b))))))(data.position['muS'].mean((-1,-2)),data.position['sigS'].mean((-1,-2)))
data.position['PosteriorCDF'] = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: jstats.norm.cdf((jnp.arange(-3,3,0.5)- a)/b))))))(data.position['postMu'].mean((-1,-2)),data.position['postVar'].mean((-1,-2)))
data.position['HitRate'] = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: jstats.norm.cdf((jnp.arange(-3,3,0.5)-a)/b)))))))(data.position['SpostMu'],data.position['SpostVar'])
data.position['FalseAlarmRate'] = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: jstats.norm.cdf((jnp.arange(-3,3,0.5)- a)/b))))))))(data.position['NpostMu'],data.position['NpostVar'])
data.position['Symmetry'] = data.position['NpostVar']/data.position['SpostVar'][...,None,:]
data.position['Separation'] = -(data.position['SpostMu'][...,None,:]-data.position['NpostMu'])/data.position['SpostVar'][...,None,:]
data.position['PHitRate'] = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: jstats.norm.cdf((jnp.arange(-3,3,0.5)- a)/b))))))))(data.position['postMu'],data.position['postVar']/np.sqrt(2))
data.position['PFalseAlarmRate'] = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: jstats.norm.cdf((jnp.arange(-3,3,0.5)- a)/b))))))))(jnp.zeros_like(data.position['postMu']),data.position['postVar']/np.sqrt(2))
plt.close('all')
lROC = [["Social","NonSocial"],["WI","BW"]]
fig,ax = plt.subplots(1,1)
color = ['blue', 'orange', 'red', 'green']
marker = ['x', '*', 'o', '^', '8']
FAll = data.position['FalseAlarmRate'].mean((0,1,2,3))
HAll = data.position['HitRate'].mean((0,1,2,3))
for i in range(2):
    for j in range(2):
        for k in range(5):
            if k == 0:
                ax.plot(FAll[i,j,k],HAll[i,k],marker=marker[k],color=color[i+2*j],label="{0} and {1}".format(lROC[0][i],lROC[1][j]))
            else:
                ax.plot(FAll[i,j,k],HAll[i,k],marker=marker[k],color=color[i+2*j])
ax.plot([0,1],label="50/50",color='black')
plt.legend()
plt.savefig("PosteriorROC")
plt.close('all')
fig,ax = plt.subplots(1,1)
for i in range(2):
    for j in range(2):
        for k in range(5):
            if k == 0:
                ax.plot(FAll[i,j,k],HAll[i,k]-FAll[i,j,k],color=color[i+2*j],label="{0} and {1}".format(lROC[0][i],lROC[1][j]))
            else:
                ax.plot(FAll[i,j,k],HAll[i,k]-FAll[i,j,k],color=color[i+2*j])
            sc = ax.scatter(FAll[i,j,k],HAll[i,k]-FAll[i,j,k],marker=marker[k],c=jnp.arange(-3,3,0.5),cmap='hot')        

plt.legend()
cbar = plt.colorbar(sc)
cbar.set_label("Bias")
plt.xlabel("False Alarm")
plt.ylabel("Hit Rate - Diagonal")
plt.savefig("PosteriorROCImp")
plt.close('all')
fig,ax = plt.subplots(1,1)
LRP = data.position['HitRate'][...,:,None,:,:]
LRN = (data.position['FalseAlarmRate'][...,:,:]+1e-2)
BF = jnp.log(LRP/LRN).mean((0,1,2,3,-2))
BayesFactor = BF
for i in range(2):
    for j in range(2):
        plt.plot(FAll.mean((-2))[i,j],HAll.mean((-2))[i]-FAll.mean((-2))[i,j],label="{0} and {1}".format(lROC[0][i],lROC[1][j]))
        sc = ax.scatter(FAll.mean((-2))[i,j,1:],HAll.mean((-2))[i,1:]-FAll.mean((-2))[i,j,1:],c=BayesFactor[i][j,1:],cmap='hot')
plt.legend()
cbar = plt.colorbar(sc)
cbar.set_label("Bias")
plt.xlabel("False Alarm")
plt.ylabel("Hit Rate - Diagonal")
plt.savefig("PosteriorROCBF")
plt.close('all')
FAlarm = data.position['FalseAlarmRate'].mean((0,1,2,3,-2))
HitR = data.position['HitRate'].mean((0,1,2,3,-2))
fig,ax = plt.subplots(1,1)
for i in range(2):
    for j in range(2):
        ax.plot(FAlarm[i,j],HitR[i],label="{0} and {1}".format(lROC[0][i],lROC[1][j]))
        sc = ax.scatter(FAlarm[i,j],HitR[i],c=jnp.arange(-3,3,0.5),cmap='hot')
ax.plot([0,1],label="50/50")
cbar = plt.colorbar(sc)
cbar.set_label("Bias")
plt.xlabel("False Alarm")
plt.ylabel("Hit Rate")
plt.savefig("ROCContour")
plt.close('all')
FAlarm = data.position['PFalseAlarmRate'].mean((0,1,2,3,-2))
HitR = data.position['PHitRate'].mean((0,1,2,3,-2))
fig,ax = plt.subplots(1,1)
for i in range(2):
    for j in range(2):
        ax.plot(FAlarm[i,j],HitR[i,j],label="{0} and {1}".format(lROC[0][i],lROC[1][j]))
        sc = ax.scatter(FAlarm[i,j],HitR[i,j],c=jnp.arange(-3,3,0.5),cmap='hot')        
ax.plot([0,1],label="50/50")
plt.legend()
cbar = plt.colorbar(sc)
cbar.set_label("Bias")
plt.xlabel("False Alarm")
plt.ylabel("Hit Rate")
plt.savefig("ROCContour2AFC")
plt.close('all')
plt.close('all')
fig,ax = plt.subplots(1,1)
for i in range(2):
    for j in range(2):
        plt.plot(FAlarm[i,j],HitR[i,j]-FAlarm[i,j],label="{0} and {1}".format(lROC[0][i],lROC[1][j]))
        sc = ax.scatter(FAlarm[i,j],HitR[i,j]-FAlarm[i,j],c=jnp.arange(-3,3,0.5),cmap='hot')
plt.legend()
cbar = plt.colorbar(sc)
cbar.set_label("Bias")
plt.xlabel("False Alarm")
plt.ylabel("Hit Rate - Diagonal")
plt.savefig("PosteriorROC2AFCImp")
plt.close('all')
LRP = data.position['PHitRate']
LRN = (data.position['PFalseAlarmRate']+1e-2)
BayesFactor = jnp.log(LRP/LRN).mean((0,1,2,3,-2))
fig,ax = plt.subplots(1,1)
for i in range(2):
    for j in range(2):
        plt.plot(FAlarm[i,j],HitR[i,j]-FAlarm[i,j],label="{0} and {1}".format(lROC[0][i],lROC[1][j]))
        sc = ax.scatter(FAlarm[i,j,1:],HitR[i,j,1:]-FAlarm[i,j,1:],c=BayesFactor[i,j,1:],cmap='hot')
plt.legend()
cbar = plt.colorbar(sc)
cbar.set_label("Bias")
plt.xlabel("False Alarm")
plt.ylabel("Hit Rate - Diagonal")
plt.savefig("PosteriorROC2AFCBF")
plt.close('all')
az.summary({"Noise":data.position['NpostMu'].mean((2,3)),"Signal":data.position['SpostMu'].mean((2,3))})
az.plot_trace({"Noise":data.position['NpostMu'].mean((2,3)),"Signal":data.position['SpostMu'].mean((2,3))})
plt.savefig("Trace_MuSDT")
az.summary({"Noise":data.position['NpostVar'].mean((2,3)),"Signal":data.position['SpostVar'].mean((2,3))})
az.plot_trace({"Noise":data.position['NpostVar'].mean((2,3)),"Signal":data.position['SpostVar'].mean((2,3))})
plt.savefig("Trace_VarSDT")
plt.close('all')
X = jnp.zeros((*data.position['FalseAlarmRate'].shape[:-1],13))
X = X.at[...,1:].set(data.position['FalseAlarmRate'])
AUC = (data.position['HitRate'][...,:,None,:,:]*jnp.diff(X[...,:,:],axis=-1)).sum(-1)
az.plot_trace({"AUC":AUC.mean((2,3))})
plt.savefig("Trace_AUC")
plt.close('all')
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['Symmetry'].mean((2,3))[...,0,1,:].mean(-1)))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['Symmetry'].mean((2,3))[...,1,1,:].mean(-1)))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.savefig("CompSvNSSymmetry_Density")
plt.close('all')
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['Separation'].mean((2,3))[...,0,1,:].mean(-1)))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['Separation'].mean((2,3))[...,1,1,:].mean(-1)))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.savefig("CompSvNSSeparation_Density")
plt.close('all')
lowPostProbaz = az.convert_to_inference_data( np.array(AUC.mean((2,3))[...,0,:,:].mean(-1)))
highPostProbaz = az.convert_to_inference_data(np.array(AUC.mean((2,3))[...,1,:,:].mean(-1)))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.savefig("CompSvNSAUC_Density")
X = jnp.zeros((*data.position['PFalseAlarmRate'].shape[:-1],13))
X = X.at[...,1:].set(data.position['PFalseAlarmRate'])
AUC = (data.position['PHitRate']*jnp.diff(X,axis=-1)).sum(-1)
az.plot_trace({"AUC":AUC.mean((2,3))})
plt.savefig("Trace2AFC_AUC")
lowPostProbaz = az.convert_to_inference_data( np.array(AUC.mean((2,3))[...,0,:,:]))
highPostProbaz = az.convert_to_inference_data(np.array(AUC.mean((2,3))[...,1,:,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.savefig("CompSvNS2AFCAUC_Density")

fig,ax = plt.subplots(2,1,sharey=True)
ax[0].plot(jnp.arange(-3,3,0.5),jnp.exp(jnp.log(data.position['PriorCDF'].mean((0,1,2,3))[0])-jnp.log(data.position['PriorCDF'].mean((0,1,2,3))[1])))
ax[0].grid()
ax[0].set_ylabel("log(Prior)")
ax[1].plot(jnp.arange(-3,3,0.5),jnp.exp(jnp.log(data.position['PosteriorCDF'].mean((0,1,2,3))[0])-jnp.log(data.position['PosteriorCDF'].mean((0,1,2,3))[1])))
ax[1].grid()
ax[1].set_ylabel("log(Posterior)")
fig.supxlabel("Signal Strength")
plt.tight_layout()
plt.savefig("CompPriorvPosteriorCDF")
data.position['logImpcriterionS'] = jnp.log(data.position['PosteriorProb']+1e-10)-jnp.log(data.position['PriorProb'][...,:2,:,:]+1e-10)
data.position['ImpEpSocS'] = data.position['logImpcriterionS'].mean((2,3,-1))
data.position['highImpEpSocS'] = data.position['logImpcriterionS'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-1))
data.position['lowImpEpSocS'] = data.position['logImpcriterionS'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-1))

WIS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==0,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)
BWS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==1,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)
WIN = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==2,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)
BWN = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==3,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)

print("Getting Summary")

data.position['criterionPM'] = data.position['Separation'].mean((2,3))
data.position['selfPM'] = data.position['Separation'].mean((2,-2,-3))
data.position['EpPM'] =   data.position['Separation'].mean((2,3,-1))
data.position['selfS'] = data.position['Separation'].mean((-2,-3))
data.position['criterionS'] = data.position['Separation']
EpSocS = data.position['Separation'].mean(-1)


data.position['PosteriorEpSocPM'] = data.position['PosteriorProb'].mean((2,3,-1))
data.position['PosteriorselfSocPM'] = data.position['PosteriorProb'].mean((2,3,-2))
data.position['PosteriorselfEpPM'] = data.position['PosteriorProb'].mean((2,3,-3))
data.position['PosteriorselfPM'] = data.position['PosteriorProb'].mean((2,3,-2,-3))
data.position['PosteriorEpPM'] = data.position['PosteriorProb'].mean((2,3,-1,-3))
data.position['PosteriorSocPM'] = data.position['PosteriorProb'].mean((2,3,-1,-2))


data.position['PriorEpSocPM'] = data.position['PriorProb'].mean((2,3,-1))
data.position['PriorselfSocPM'] = data.position['PriorProb'].mean((2,3,-2))
data.position['PriorselfEpPM'] = data.position['PriorProb'].mean((2,3,-3))
data.position['PriorselfPM'] = data.position['PriorProb'].mean((2,3,-2,-3))
data.position['PriorEpPM'] = data.position['PriorProb'].mean((2,3,-1,-3))
data.position['PriorSocPM'] = data.position['PriorProb'].mean((2,3,-1,-2))



lowPostProbaz = az.convert_to_inference_data( np.array(data.position['PosteriorEpSocPM'][...,0]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['PosteriorEpSocPM'][...,1]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['W/I','B/W'],shade=0.2)
plt.savefig("CompWIBW_Density")
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['PosteriorEpSocPM'][...,0,:]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['PosteriorEpSocPM'][...,1,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.savefig("CompSvNS_Density")
plt.close('all')
fig,ax = plt.subplots(2,3,sharex=True)
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['PriorEpSocPM'][...,:]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['PosteriorEpSocPM'][...,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Prior','Posterior'],shade=0.2,ax=ax)
plt.tight_layout()
plt.savefig("CompPriorvPosterior_Density")
plt.close('all')
lowPostProbaz = az.convert_to_inference_data( np.array(1/data.position['sigPM'][...,:]))
highPostProbaz = az.convert_to_inference_data(np.array(1/data.position['postVarP'][...,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Prior','Posterior'],shade=0.2)
plt.tight_layout()
plt.savefig("CompSensitivityPriorvPosterior_Density")
plt.close('all')
PriorlowPostProbaz = az.convert_to_inference_data( np.array(1/data.position['lowsigPM'][...,:]))
PostlowPostProbaz = az.convert_to_inference_data(np.array(1/data.position['lowpostVarP'][...,:]))
PriorhighPostProbaz = az.convert_to_inference_data( np.array(1/data.position['highsigPM'][...,:]))
PosthighPostProbaz = az.convert_to_inference_data(np.array(1/data.position['highpostVarP'][...,:]))
axes = az.plot_density([PostlowPostProbaz,PosthighPostProbaz,PriorlowPostProbaz,PriorhighPostProbaz],data_labels=['Low Posterior','High Posterior','Low Prior','High Prior'],shade=0.2)
plt.tight_layout()
plt.savefig("lowCompSensitivityPriorvPosterior_Density",bbox_inches='tight')

plt.close('all')
fig,ax = plt.subplots(2,5,sharex=True,figsize=(12,10))
LowhighPostProbaz = az.convert_to_inference_data(np.array(data.position['diffVar'][...,0,:,:]))
HighhighPostProbaz = az.convert_to_inference_data(np.array(data.position['diffVar'][...,1,:,:]))
axes = az.plot_density([LowhighPostProbaz,HighhighPostProbaz],data_labels=['Social','NonSocial'],shade=0.2,ax=ax)
ax[0,0].legend(bbox_to_anchor=(.65, 0.9),ncols=1)
plt.tight_layout()
plt.savefig("CompdiffVarPriorvPosterior_Density")
plt.close('all')
fig,ax = plt.subplots(2,5,sharex=True,figsize=(12,10))
LowhighPostProbaz = az.convert_to_inference_data(np.array(data.position['diffMu'][...,0,:,:]))
HighhighPostProbaz = az.convert_to_inference_data(np.array(data.position['diffMu'][...,1,:,:]))
axes = az.plot_density([LowhighPostProbaz,HighhighPostProbaz],data_labels=['Social','NonSocial'],shade=0.2,ax=ax)
ax[0,0].legend(bbox_to_anchor=(.65, 0.9),ncols=1)
plt.tight_layout()
plt.savefig("CompdiffMuPriorvPosterior_Density")
plt.close('all')

print(az.summary(data.position,var_names=["criterionPM"]))
ax = az.plot_trace(data.position,var_names=["criterionPM"])
plt.tight_layout()
plt.savefig("EpSocial_Trace.png")

print(az.summary(data.position,var_names=["EpPM"]))
ax = az.plot_trace(data.position,var_names=["EpPM"])
plt.tight_layout()
plt.savefig("Episode_Trace.png")

print(az.summary(data.position,var_names=["selfPM"]))
ax = az.plot_trace(data.position,var_names=["selfPM"])
plt.tight_layout()
plt.savefig("Self_Trace.png")

print(az.summary(data.position,var_names=["PosteriorEpSocPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorEpSocPM"])
plt.tight_layout()
plt.savefig("PosteriorEpSocial_Trace.png")

print(az.summary(data.position,var_names=["PosteriorselfSocPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorselfSocPM"])
plt.tight_layout()
plt.savefig("PosteriorselfSocial_Trace.png")

print(az.summary(data.position,var_names=["PosteriorselfEpPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorselfEpPM"])
plt.tight_layout()
plt.savefig("PosteriorselfEpisode_Trace.png")

print(az.summary(data.position,var_names=["PosteriorSocPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorSocPM"])
plt.tight_layout()
plt.savefig("PosteriorSocial_Trace.png")

print(az.summary(data.position,var_names=["PosteriorEpPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorEpPM"])
plt.tight_layout()
plt.savefig("PosteriorEpisode_Trace.png")

print(az.summary(data.position,var_names=["PosteriorselfPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorselfPM"])
plt.tight_layout()
plt.savefig("PosteriorSelf_Trace.png")

def ttest(A,B):
 mA = jnp.where(A==1,B,0).sum()/(A==1).sum()
 mB = jnp.where(A==0,B,0).sum()/(A==0).sum()
 S = (jnp.where(A==1,(B-mA)**2,0).sum() + jnp.where(A==0,(B-mB)**2,0).sum())/(A.size-2)
 return (mA - mB)/jnp.sqrt(S/(A==1).sum() +S/(A==0).sum())

def ttest1Samp(A):
    return A.mean()/(A.std()/jnp.sqrt(A.size-1))
GLods = []
GLodCIs = []
LLods = []
Dists = []
RankDists = []
Ts = []
for i in range(5):
    plt.close('all')
    Dists += [jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: (jstats.rankdata(-A,'max')[i]==jstats.rankdata(B,'max')[i]).astype(int))),in_axes=[0,None]),in_axes=[0,None])(data.position['selfS'],jnp.exp(-jnp.array(RunsDist)))] 
    WISRankCorr = (jax.vmap(jax.vmap(ttest))(Dists[i],-EpSocS[...,0,0]))
    WINRankCorr = (jax.vmap(jax.vmap(ttest))(Dists[i],-EpSocS[...,1,0]))
    BWSRankCorr = (jax.vmap(jax.vmap(ttest))(Dists[i],-EpSocS[...,0,1]))
    BWNRankCorr = (jax.vmap(jax.vmap(ttest))(Dists[i],-EpSocS[...,1,1]))
    WISRCorr = (jax.vmap(jax.vmap(lambda A,B: jnp.corrcoef(A.ravel(),B.ravel())[0,1], in_axes=[0,None]),in_axes=[0,None])(EpSocS[...,0,0],Ranks[...,1]))
    WINRCorr = (jax.vmap(jax.vmap(lambda A,B: jnp.corrcoef(A.ravel(),B.ravel())[0,1], in_axes=[0,None]),in_axes=[0,None])(EpSocS[...,1,0],Ranks[...,1]))
    BWSRCorr = (jax.vmap(jax.vmap(lambda A,B: jnp.corrcoef(A.ravel(),B.ravel())[0,1], in_axes=[0,None]),in_axes=[0,None])(EpSocS[...,0,1],Ranks[...,1]))
    BWNRCorr = (jax.vmap(jax.vmap(lambda A,B: jnp.corrcoef(A.ravel(),B.ravel())[0,1], in_axes=[0,None]),in_axes=[0,None])(EpSocS[...,1,1],Ranks[...,1]))
    Ts += [jnp.array([WISRankCorr,WINRankCorr,BWSRankCorr,BWNRankCorr]).transpose(1,2,0)]
    print(az.summary({"{0:d}_TTest".format(5-i):jnp.array([WISRankCorr,WINRankCorr,BWSRankCorr,BWNRankCorr]).transpose(1,2,0)}))
    az.plot_trace({"TTest":jnp.array([WISRankCorr,WINRankCorr,BWSRankCorr,BWNRankCorr]).transpose(1,2,0)})
    plt.savefig("{0:d}_TTest_Trace.png".format(5-i))
    plt.close('all')
    az.plot_trace({"RankCorr":jnp.array([WISRCorr,BWSRCorr,WINRCorr,BWNRCorr]).transpose(1,2,0)})
    plt.savefig("{0:d}_RankCorr_Trace.png".format(5-i))
    GWISOdd = (WISRankCorr>0).sum(-1)/(WISRankCorr<0).sum(-1)
    GWISCI = 1.96*np.sqrt(1/(WISRankCorr>0).sum(-1) + 1/(WISRankCorr<0).sum(-1) + 2*1/WISRankCorr.shape[-1])
    GWINOdd = (WINRankCorr>0).sum(-1)/(WINRankCorr<0).sum(-1)
    GWINCI = 1.96*np.sqrt(1/(WINRankCorr>0).sum(-1) + 1/(WINRankCorr<0).sum(-1) + 2*1/WINRankCorr.shape[-1])
    GBWSOdd = (BWSRankCorr>0).sum(-1)/(BWSRankCorr<0).sum(-1)
    GBWSCI = 1.96*np.sqrt(1/(BWSRankCorr>0).sum(-1) + 1/(BWSRankCorr<0).sum(-1) + 2*1/BWSRankCorr.shape[-1])
    GBWNOdd = (BWNRankCorr>0).sum(-1)/(BWNRankCorr<0).sum(-1)
    GBWNCI = 1.96*np.sqrt(1/(BWNRankCorr>0).sum(-1) + 1/(BWNRankCorr<0).sum(-1) + 2*1/BWNRankCorr.shape[-1])
    LWISOdd = 1/((WISRankCorr>0).sum()/(WISRankCorr<0).sum())
    LWINOdd = 1/((WINRankCorr>0).sum()/(WINRankCorr<0).sum())
    LBWSOdd = 1/((BWSRankCorr>0).sum()/(BWSRankCorr<0).sum())
    LBWNOdd = 1/((BWNRankCorr>0).sum()/(BWNRankCorr<0).sum())
    GLods += [[1/GWISOdd.mean(),1/GWINOdd.mean(),1/GBWSOdd.mean(),1/GBWNOdd.mean()]] 
    GLodCIs += [[GWISOdd.std(),GWINOdd.std(),GBWSOdd.std(),GBWNOdd.std()]] 
    LLods += [[LWISOdd,LWINOdd,LBWSOdd,LBWNOdd]] 
GLodCIs = np.array(GLodCIs)

Ts = jnp.array(Ts).transpose(1,2,3,0)
plt.close('all')
low = az.convert_to_inference_data(np.array( Ts[...,1,::-1]))
high = az.convert_to_inference_data(np.array(Ts[...,0,::-1]))
fig, ax = plt.subplots(5,1,sharex=True)
az.plot_density([high,low],shade=0.2,data_labels=['Social','NonSocial'],ax=ax)
ax[-1].set_xlim((-5.5,5.5))
plt.tight_layout()
plt.savefig("WITTests")
plt.close('all')
low = az.convert_to_inference_data(np.array( Ts[...,3,::-1]))
high = az.convert_to_inference_data(np.array(Ts[...,2,::-1]))
fig, ax = plt.subplots(5,1,sharex=True)
az.plot_density([high,low],shade=0.2,data_labels=['Social','NonSocial'],ax=ax)
ax[-1].set_xlim((-5.5,5.5))
plt.tight_layout()
plt.savefig("BWTTests")
