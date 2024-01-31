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

with open('Posterior_EpStrBDP.pkl', 'rb') as f:
    data = pickle.load(f)
print(data.logdensity.shape)
data = jax.tree_map(lambda x: x[:,:],data)

Res = np.concatenate([np.load("distrep1Collect.npy"),np.load("distrep2Collect.npy")[:,::-1]],0)
# Memory Retrieval Confidence
Confidence = Res[:,:,-3].astype(float)
Persons = Res[...,-4,:]
Dists = Res[...,-1,:]
Social = Res[...,0,:]
# Get the participant distance from each activity cue
RunsDist = [[[np.unique(Dists[k,j][Persons[k,j]==i]).squeeze() for i in range(5)] for j in range(2)] for k in range(115)]
obs = Res[:,:,0]
Social = Res[:,:,1]
Episode = Res[:,:,2]
EpSoc = 2*Social + Episode
# Ranking performance
Ranks = np.concatenate([np.load("Rankingrep1.npy"),np.load("Rankingrep2.npy")[:,::-1]],0).transpose(0,2,1)
RConfs = [[[] for j in range(2)] for i in range(2)]
# Get confidence for each participant for each run for either social or nonsocial memory retrieval
for i in range(115):
    for j in range(2):
        for k in range(2):
            RConfs[j][k].append(Confidence[i,j][Social[i,j]==k].mean())
RankConf = np.array(RConfs).transpose(2,0,1)

# Posterior Predictive of hierarchical inference
PPred = data.position['posteriorPredictive']
PosteriorProb = data.position['PosteriorProb']

# Marginalizing out participants and runs
data.position['postMuP'] = data.position['postMu'].mean((2,3,))
# Correlating confidence with variance parameters
confcorr = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: jnp.corrcoef(a.ravel(),b.ravel())[0,1],in_axes=[None,-1]),in_axes=[-1,None]),in_axes=[0,None]),in_axes=[0,None])
rankconfsig = confcorr((data.position['sigS']),RankConf)
rankconfpostsig = confcorr(data.position['postVar'],RankConf)
rankconfmu = confcorr(data.position['postMu'],RankConf)
# Explained variance
rankconfssig = confcorr((data.position['sigS']),RankConf)**2
rankconfspostsig = confcorr(data.position['postVar'],RankConf)**2
rankconfsmu = confcorr(data.position['postMu'],RankConf)**2

# Plotting kernel densities of role uncertainty correlation with confidence
fig,ax = plt.subplots(2,1)
lowPostProbaz = az.convert_to_inference_data( np.array(rankconfsig[...,0,:]))
highPostProbaz = az.convert_to_inference_data( np.array(rankconfsig[...,1,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2,ax=ax)
plt.tight_layout()
plt.savefig("CompRankConfRoleUncertaintyCorr")
plt.close('all')
labs = ["Social","NonSocial"]
labsO = ["W/I","B/W"]
PosteriorProbEpSoc = (PosteriorProb[...,0,:,:]-PosteriorProb[...,1,:,:]).mean((2,3,-1))

figa,axa = plt.subplots(1,2,sharex=True)
fig2,ax2 = plt.subplots(1,2,sharex=True)
for i in range(2):
    idata = az.from_dict(posterior={"Hit Rate":PosteriorProbEpSoc[...,i],"Assignment Uncertainty":rankconfssig[...,0,i]-rankconfssig[...,1,i]}, prior={"Hit Rate":np.random.normal(0, 0.05, 20000),"Assignment Uncertainty":np.random.normal(0, 0.01, 20000)})
    az.plot_bf(idata,var_name="Assignment Uncertainty",ax=axa[i])
    az.plot_bf(idata,var_name="Hit Rate",ax=ax2[i])
    axa[i].set_xlabel("{0} Confidence".format(labs[i]))
    ax2[i].set_xlabel("{0}".format(labsO[i]))
figa.supxlabel(r"$R^{2}_{\hat\sigma_{Role|Social},Confidence} - R^{2}_{\hat\sigma_{Role|NonSocial},Confidence}$")
fig2.supxlabel(r"Hit Rate")

fig2.tight_layout()
figa.tight_layout()
figa.savefig("BayesFactorsAss".format(labs[i]),bbox_inches='tight')
fig2.savefig("BayesFactorsPerformance".format(labs[i]),bbox_inches='tight')
plt.close('all')



print("OddsSig: {0:.4f}, {1:.4f}".format(*((rankconfssig[...,0,:] > rankconfssig[...,1,:]).sum((0,1))/(rankconfssig[...,0,:] < rankconfssig[...,1,:]).sum((0,1)))))
print("OddsSig: {0:.4f}, {1:.4f}".format(*(1/((rankconfssig[...,0,:] > rankconfssig[...,1,:]).sum((0,1))/(rankconfssig[...,0,:] < rankconfssig[...,1,:]).sum((0,1))))))

# Low vs high performance filter on role assignment for posterior memory recall parms
data.position['highpostMuP'] = data.position['postMu'][:,:,Ranks[...,1]>=0.4].mean((2))
data.position['lowpostMuP'] = data.position['postMu'][:,:,Ranks[...,1]<0.4].mean((2))
data.position['postVarP'] = data.position['postVar'].mean((2,3,))
data.position['highpostVarP'] = data.position['postVar'][:,:,Ranks[...,1]>=0.4].mean((2))
data.position['lowpostVarP'] = data.position['postVar'][:,:,Ranks[...,1]<0.4].mean((2))

# Prior d' on memory recall
data.position['muS'] = jnp.ones_like(data.position['postMu'])
data.position['muPM'] = jnp.ones_like(data.position['postMuP'])
data.position['highmuPM'] = data.position['muS'][:,:,Ranks[...,1]>=0.4].mean((2))
data.position['lowmuPM'] = data.position['muS'][:,:,Ranks[...,1]<0.4].mean((2))
# Role uncertainty parameter
data.position['RankSigS'] = jnp.copy(data.position['sigS'])
# prior encoding variance on memory recall
data.position['sigPM'] = data.position['sigS'].mean((2,3))
data.position['sigS'] = jnp.ones_like(data.position['postVar'])
data.position['sigPM'] = jnp.ones_like(data.position['postVarP'])
data.position['highsigPM'] = data.position['sigS'][:,:,Ranks[...,1]>=0.4].mean((2))
data.position['lowsigPM'] = data.position['sigS'][:,:,Ranks[...,1]<0.4].mean((2))
# Difference between posterior and prior d'
data.position['diffMu'] = data.position['postMuP'] - data.position['muPM']
# Ratio between posterior and prior encoding variance
data.position['diffVar'] = data.position['postVarP']/data.position['sigPM']
# Prior probability of given signals (dependent on activity cue, and W/I or B/W discrimination)
data.position['PriorProb'] = jstats.norm.cdf(data.position['criterionS'][...,None,:,:],loc=data.position['muS'][...,None,None],scale=data.position['sigS'][...,None,None])
# Plotting prior and posterior CDFs w.r.t. signal strength
data.position['PriorCDF'] = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: jstats.norm.cdf((jnp.arange(0,3,0.1)-a)/b))))))(data.position['muS'],data.position['sigS'])
data.position['PosteriorCDF'] = jax.vmap(jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda a,b: jstats.norm.cdf((jnp.arange(0,3,0.1)- a)/b))))))(data.position['postMu'],data.position['postVar'])
plt.close('all')
# plotting prior and posterior CDFs
fig,ax = plt.subplots(2,1,sharey=True)
ax[0].plot(jnp.arange(0,3,0.1),jnp.exp(jnp.log(data.position['PriorCDF'].mean((0,1,2,3))[0])-jnp.log(data.position['PriorCDF'].mean((0,1,2,3))[1])))
ax[0].grid()
ax[0].set_ylabel("log(Prior)")
ax[1].plot(jnp.arange(0,3,0.1),jnp.exp(jnp.log(data.position['PosteriorCDF'].mean((0,1,2,3))[0])-jnp.log(data.position['PosteriorCDF'].mean((0,1,2,3))[1])))
ax[1].grid()
ax[1].set_ylabel("log(Posterior)")
fig.supxlabel("Signal Strength")
plt.tight_layout()
plt.savefig("CompPriorvPosteriorCDF")
# Log ratio of memory recall improvement 
data.position['logImpcriterionS'] = jnp.log(data.position['PosteriorProb']+1e-10)-jnp.log(data.position['PriorProb']+1e-10)
data.position['ImpEpSocS'] = data.position['logImpcriterionS'].mean((2,3,-1))
data.position['highImpEpSocS'] = data.position['logImpcriterionS'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-1))
data.position['lowImpEpSocS'] = data.position['logImpcriterionS'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-1))

# Get posterior memory recall hit rate for W/I or B/W and Social or NonSocial memory
WIS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==0,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)
BWS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==1,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)
WIN = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==2,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)
BWN = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==3,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)

print("Getting Summary")
invlogit = lambda x: 1/(1+jnp.exp(-x))
CoVul = lambda x,a,b: a + (b-a)*invlogit(x)
CoV = lambda x: jnp.exp(x)

# Get biases
data.position['selfPM'] = ((1/data.position['postVar'][...,:,None,None])*(2*data.position['postMu'][...,:,None,None] - data.position['criterionS'][...,None,:,:])).mean((2,-2))
data.position['EpPM'] =   ((1/data.position['postVar'][...,:,None,None])*(2*data.position['postMu'][...,:,None,None] - data.position['criterionS'][...,None,:,:])).mean((2,3,-1))
data.position['selfS'] = ((1/data.position['postVar'][...,:,None,None])*(2*data.position['postMu'][...,:,None,None] - data.position['criterionS'][...,None,:,:])).mean((-2,-3))
data.position['criterionS'] = (data.position['criterionS'])
EpSocS = ((1/data.position['postVar'][...,:,None,None])*(2*data.position['postMu'][...,:,None,None] - data.position['criterionS'][...,None,:,:])).mean((-1))


# Get marginal posterior probs
data.position['PosteriorEpSocPM'] = data.position['PosteriorProb'].mean((2,3,-1))
data.position['PosteriorselfSocPM'] = data.position['PosteriorProb'].mean((2,3,-2))
data.position['PosteriorselfEpPM'] = data.position['PosteriorProb'].mean((2,3,-3))
data.position['PosteriorselfPM'] = data.position['PosteriorProb'].mean((2,3,-2,-3))
data.position['PosteriorEpPM'] = data.position['PosteriorProb'].mean((2,3,-1,-3))
data.position['PosteriorSocPM'] = data.position['PosteriorProb'].mean((2,3,-1,-2))

# High vs low performing participants on role assignment
data.position['highPosteriorEpSocPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-1))
data.position['highPosteriorselfSocPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-2))
data.position['highPosteriorselfEpPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-3))
data.position['highPosteriorselfPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-2,-3))
data.position['highPosteriorEpPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-1,-3))
data.position['highPosteriorSocPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-1,-2))

data.position['lowPosteriorEpSocPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-1))
data.position['lowPosteriorselfSocPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-2))
data.position['lowPosteriorselfEpPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-3))
data.position['lowPosteriorselfPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-2,-3))
data.position['lowPosteriorEpPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-1,-3))
data.position['lowPosteriorSocPM'] = data.position['PosteriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-1,-2))


# Get  marginal prior probs
data.position['PriorEpSocPM'] = data.position['PriorProb'].mean((2,3,-1))
data.position['PriorselfSocPM'] = data.position['PriorProb'].mean((2,3,-2))
data.position['PriorselfEpPM'] = data.position['PriorProb'].mean((2,3,-3))
data.position['PriorselfPM'] = data.position['PriorProb'].mean((2,3,-2,-3))
data.position['PriorEpPM'] = data.position['PriorProb'].mean((2,3,-1,-3))
data.position['PriorSocPM'] = data.position['PriorProb'].mean((2,3,-1,-2))


# For high and low performing participants on role assignment
data.position['highPriorEpSocPM'] = data.position['PriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-1))
data.position['highPriorselfSocPM'] = data.position['PriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-2))
data.position['highPriorselfEpPM'] = data.position['PriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-3))
data.position['highPriorselfPM'] = data.position['PriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-2,-3))
data.position['highPriorEpPM'] = data.position['PriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-1,-3))
data.position['highPriorSocPM'] = data.position['PriorProb'][:,:,Ranks[...,1]>=0.4,:,:].mean((2,-1,-2))

data.position['lowPriorEpSocPM'] = data.position['PriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-1))
data.position['lowPriorselfSocPM'] = data.position['PriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-2))
data.position['lowPriorselfEpPM'] = data.position['PriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-3))
data.position['lowPriorselfPM'] = data.position['PriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-2,-3))
data.position['lowPriorEpPM'] = data.position['PriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-1,-3))
data.position['lowPriorSocPM'] = data.position['PriorProb'][:,:,Ranks[...,1]<0.4,:,:].mean((2,-1,-2))


# Compare low v high performing participant posterior memory recall
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['lowPosteriorEpSocPM']))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['highPosteriorEpSocPM']))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['low','high'],shade=0.2)
plt.savefig("CompLowHigh_Density")
# Compare W/I vs B/W posterior memory recall
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['PosteriorEpSocPM'][...,0]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['PosteriorEpSocPM'][...,1]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['W/I','B/W'],shade=0.2)
plt.savefig("CompWIBW_Density")
# Compare Social v NonSocial memory recall
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['PosteriorEpSocPM'][...,0,:]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['PosteriorEpSocPM'][...,1,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.savefig("CompSvNS_Density")
# high v low performing participant Social v Nonsocial memory recall
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['highPosteriorEpSocPM'][...,0,:]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['highPosteriorEpSocPM'][...,1,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.savefig("highCompSvNS_Density")
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['lowPosteriorEpSocPM'][...,0,:]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['lowPosteriorEpSocPM'][...,1,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Social','NonSocial'],shade=0.2)
plt.savefig("lowCompSvNS_Density")
plt.close('all')
import matplotlib.pyplot as plt
plt.close('all')
# Prior v Posterior Memory recall
fig,ax = plt.subplots(2,2,sharex=True)
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['PriorEpSocPM'][...,:]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['PosteriorEpSocPM'][...,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Prior','Posterior'],shade=0.2,ax=ax)
plt.tight_layout()
plt.savefig("CompPriorvPosterior_Density")
plt.close('all')
fig,ax = plt.subplots(2,2,sharex=True)
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['highPriorEpSocPM'][...,:]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['highPosteriorEpSocPM'][...,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Prior','Posterior'],shade=0.2,ax=ax)
plt.tight_layout()
plt.savefig("highCompPriorvPosterior_Density")
plt.close('all')
fig,ax = plt.subplots(2,2,sharex=True)
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['lowPriorEpSocPM'][...,:]))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['lowPosteriorEpSocPM'][...,:]))
axes = az.plot_density([lowPostProbaz,highPostProbaz],data_labels=['Prior','Posterior'],shade=0.2)
plt.tight_layout()
plt.savefig("lowCompPriorvPosterior_Density")
plt.close('all')

# Plot Prior d', Posterior d', and Signal biases together for B/W, W/I and Social, Nonsocial memory recall
mVal = az.convert_to_inference_data(np.array(data.position['criterionS'].mean((2,3,-1))[...,None,:].repeat(2,axis=-2)))
highmVal = az.convert_to_inference_data(np.array(data.position['criterionS'][:,:,Ranks[...,1]>=0.4].mean((2,-1))[...,None,:].repeat(2,axis=-2)))
lowmVal = az.convert_to_inference_data(np.array(data.position['criterionS'][:,:,Ranks[...,1]>=0.4].mean((2,-1))[...,None,:].repeat(2,axis=-2)))
plt.close('all')
fig,ax = plt.subplots(2,2,sharex=True,figsize=(8,6))
lowPostProbaz = az.convert_to_inference_data( np.array(data.position['muPM'][...,None].repeat(2,axis=-1)))
highPostProbaz = az.convert_to_inference_data(np.array(data.position['postMuP'][...,None].repeat(2,axis=-1)))
axes = az.plot_density([lowPostProbaz,highPostProbaz,mVal],data_labels=['Prior','Posterior',"Signal Strength"],shade=0.2,ax=ax)
plt.tight_layout()
ax[0,0].legend(bbox_to_anchor=(0.6, 0.7))
plt.savefig("CompMuPriorvPosterior_Density")
plt.close('all')
fig,ax = plt.subplots(2,2,sharex=True,figsize=(8,6))
axes = az.plot_density([lowPostProbaz,highPostProbaz,highmVal],data_labels=['Prior','Posterior',"Signal Strength"],shade=0.2,ax=ax)
plt.tight_layout()
ax[0,0].legend(bbox_to_anchor=(0.6, 0.7))
plt.savefig("highCompMuPriorvPosterior_Density")
plt.close('all')
fig,ax = plt.subplots(2,2,sharex=True,figsize=(8,6))
LowlowPostProbaz = az.convert_to_inference_data( np.array(data.position['lowmuPM'][...,:,None].repeat(2,axis=-1)))
LowhighPostProbaz = az.convert_to_inference_data(np.array(data.position['lowpostMuP'][...,:,None]).repeat(2,axis=-1))
HighlowPostProbaz = az.convert_to_inference_data( np.array(data.position['highmuPM'][...,:,None].repeat(2,axis=-1)))
HighhighPostProbaz = az.convert_to_inference_data(np.array(data.position['highpostMuP'][...,:,None]).repeat(2,axis=-1))
axes = az.plot_density([LowlowPostProbaz,LowhighPostProbaz,lowmVal,HighlowPostProbaz,HighhighPostProbaz,highmVal],data_labels=['Low Prior','Low Posterior',"Low Signal Strength",'High Prior','High Posterior',"High Signal Strength"],shade=0.2,ax=ax)
ax[0,0].legend(bbox_to_anchor=(.65, 0.9),ncols=2)
ax[0,0].get_legend().remove()
plt.tight_layout()
plt.savefig("lowCompMuPriorvPosterior_Density")
plt.close('all')
fig,ax = plt.subplots(1,1,sharex=True)
# Plot ratio between Posterior and prior encoding variance for social and nonsocial memory recall
LowhighPostProbaz = az.convert_to_inference_data(np.array(data.position['diffVar'][...,0]))
HighhighPostProbaz = az.convert_to_inference_data(np.array(data.position['diffVar'][...,1]))
axes = az.plot_density([LowhighPostProbaz,HighhighPostProbaz],data_labels=['Social','NonSocial'],shade=0.2,ax=ax)
ax.legend(bbox_to_anchor=(.65, 0.9),ncols=1)
plt.tight_layout()
plt.savefig("CompdiffVarPriorvPosterior_Density")
plt.close('all')
fig,ax = plt.subplots(1,1,sharex=True)
# Plot difference between posterior and prior d' for social and nonsocial
LowhighPostProbaz = az.convert_to_inference_data(np.array(data.position['diffMu'][...,0]))
HighhighPostProbaz = az.convert_to_inference_data(np.array(data.position['diffMu'][...,1]))
axes = az.plot_density([LowhighPostProbaz,HighhighPostProbaz],data_labels=['Social','NonSocial'],shade=0.2,ax=ax)
ax.legend(bbox_to_anchor=(.65, 0.9),ncols=1)
plt.tight_layout()
plt.savefig("CompdiffMuPriorvPosterior_Density")
plt.close('all')

# Plot bias for interactions between B/W, W/I and activity cue biases
print(az.summary(data.position,var_names=["criterionPM"]))
ax = az.plot_trace(data.position,var_names=["criterionPM"])
plt.tight_layout()
plt.savefig("EpSocial_Trace.png")

# Plot marginal bias for B/W and W/I
print(az.summary(data.position,var_names=["EpPM"]))
ax = az.plot_trace(data.position,var_names=["EpPM"])
plt.tight_layout()
plt.savefig("Episode_Trace.png")

# Plot marginal bias for activity cues
print(az.summary(data.position,var_names=["selfPM"]))
ax = az.plot_trace(data.position,var_names=["selfPM"])
plt.tight_layout()
plt.savefig("Self_Trace.png")

# Plot posterior memory recall hit rate marginalizing out acitvity cue
print(az.summary(data.position,var_names=["PosteriorEpSocPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorEpSocPM"])
plt.tight_layout()
plt.savefig("PosteriorEpSocial_Trace.png")

# Plot posterior memory recall hit rate marginalizing out B/W and W/I interactions 
print(az.summary(data.position,var_names=["PosteriorselfSocPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorselfSocPM"])
plt.tight_layout()
plt.savefig("PosteriorselfSocial_Trace.png")

# Plot posterior memory recall hit rate marginalizing out Social and NonSocial interactions 
print(az.summary(data.position,var_names=["PosteriorselfEpPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorselfEpPM"])
plt.tight_layout()
plt.savefig("PosteriorselfEpisode_Trace.png")

# Plot marginal posterior memory recall hit rate for Social v Nonsocial 
print(az.summary(data.position,var_names=["PosteriorSocPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorSocPM"])
plt.tight_layout()
plt.savefig("PosteriorSocial_Trace.png")

# Plot marginal posterior memory recall hit rate for W/I v B/W 
print(az.summary(data.position,var_names=["PosteriorEpPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorEpPM"])
plt.tight_layout()
plt.savefig("PosteriorEpisode_Trace.png")

# Plot marginal posterior memory recall hit rate for activity cue 
print(az.summary(data.position,var_names=["PosteriorselfPM"]))
ax = az.plot_trace(data.position,var_names=["PosteriorselfPM"])
plt.tight_layout()
plt.savefig("PosteriorSelf_Trace.png")

# All the above, but for high performing participants
print(az.summary(data.position,var_names=["highPosteriorEpSocPM"]))
ax = az.plot_trace(data.position,var_names=["highPosteriorEpSocPM"])
plt.tight_layout()
plt.savefig("highPosteriorEpSocial_Trace.png")

print(az.summary(data.position,var_names=["highPosteriorselfSocPM"]))
ax = az.plot_trace(data.position,var_names=["highPosteriorselfSocPM"])
plt.tight_layout()
plt.savefig("highPosteriorselfSocial_Trace.png")

print(az.summary(data.position,var_names=["highPosteriorselfEpPM"]))
ax = az.plot_trace(data.position,var_names=["highPosteriorselfEpPM"])
plt.tight_layout()
plt.savefig("highPosteriorselfEpisode_Trace.png")

print(az.summary(data.position,var_names=["highPosteriorSocPM"]))
ax = az.plot_trace(data.position,var_names=["highPosteriorSocPM"])
plt.tight_layout()
plt.savefig("highPosteriorSocial_Trace.png")

print(az.summary(data.position,var_names=["highPosteriorEpPM"]))
ax = az.plot_trace(data.position,var_names=["highPosteriorEpPM"])
plt.tight_layout()
plt.savefig("highPosteriorEpisode_Trace.png")

print(az.summary(data.position,var_names=["highPosteriorselfPM"]))
ax = az.plot_trace(data.position,var_names=["highPosteriorselfPM"])
plt.tight_layout()
plt.savefig("highPosteriorSelf_Trace.png")

# All the above, but for low performing participants
print(az.summary(data.position,var_names=["lowPosteriorEpSocPM"]))
ax = az.plot_trace(data.position,var_names=["lowPosteriorEpSocPM"])
plt.tight_layout()
plt.savefig("lowPosteriorEpSocial_Trace.png")

print(az.summary(data.position,var_names=["lowPosteriorselfSocPM"]))
ax = az.plot_trace(data.position,var_names=["lowPosteriorselfSocPM"])
plt.tight_layout()
plt.savefig("lowPosteriorselfSocial_Trace.png")

print(az.summary(data.position,var_names=["lowPosteriorselfEpPM"]))
ax = az.plot_trace(data.position,var_names=["lowPosteriorselfEpPM"])
plt.tight_layout()
plt.savefig("lowPosteriorselfEpisode_Trace.png")

print(az.summary(data.position,var_names=["lowPosteriorSocPM"]))
ax = az.plot_trace(data.position,var_names=["lowPosteriorSocPM"])
plt.tight_layout()
plt.savefig("lowPosteriorSocial_Trace.png")

print(az.summary(data.position,var_names=["lowPosteriorEpPM"]))
ax = az.plot_trace(data.position,var_names=["lowPosteriorEpPM"])
plt.tight_layout()
plt.savefig("lowPosteriorEpisode_Trace.png")

print(az.summary(data.position,var_names=["lowPosteriorselfPM"]))
ax = az.plot_trace(data.position,var_names=["lowPosteriorselfPM"])
plt.tight_layout()
plt.savefig("lowPosteriorSelf_Trace.png")


# All the above, but for prior memory recall hit rate 
print(az.summary(data.position,var_names=["PriorEpSocPM"]))
ax = az.plot_trace(data.position,var_names=["PriorEpSocPM"])
plt.tight_layout()
plt.savefig("PriorEpSocial_Trace.png")

print(az.summary(data.position,var_names=["PriorselfSocPM"]))
ax = az.plot_trace(data.position,var_names=["PriorselfSocPM"])
plt.tight_layout()
plt.savefig("PriorselfSocial_Trace.png")

print(az.summary(data.position,var_names=["PriorselfEpPM"]))
ax = az.plot_trace(data.position,var_names=["PriorselfEpPM"])
plt.tight_layout()
plt.savefig("PriorselfEpisode_Trace.png")

print(az.summary(data.position,var_names=["PriorSocPM"]))
ax = az.plot_trace(data.position,var_names=["PriorSocPM"])
plt.tight_layout()
plt.savefig("PriorSocial_Trace.png")

print(az.summary(data.position,var_names=["PriorEpPM"]))
ax = az.plot_trace(data.position,var_names=["PriorEpPM"])
plt.tight_layout()
plt.savefig("PriorEpisode_Trace.png")

print(az.summary(data.position,var_names=["PriorselfPM"]))
ax = az.plot_trace(data.position,var_names=["PriorselfPM"])
plt.tight_layout()
plt.savefig("PriorSelf_Trace.png")

print(az.summary(data.position,var_names=["highPriorEpSocPM"]))
ax = az.plot_trace(data.position,var_names=["highPriorEpSocPM"])
plt.tight_layout()
plt.savefig("highPriorEpSocial_Trace.png")

print(az.summary(data.position,var_names=["highPriorselfSocPM"]))
ax = az.plot_trace(data.position,var_names=["highPriorselfSocPM"])
plt.tight_layout()
plt.savefig("highPriorselfSocial_Trace.png")

print(az.summary(data.position,var_names=["highPriorselfEpPM"]))
ax = az.plot_trace(data.position,var_names=["highPriorselfEpPM"])
plt.tight_layout()
plt.savefig("highPriorselfEpisode_Trace.png")

print(az.summary(data.position,var_names=["highPriorSocPM"]))
ax = az.plot_trace(data.position,var_names=["highPriorSocPM"])
plt.tight_layout()
plt.savefig("highPriorSocial_Trace.png")

print(az.summary(data.position,var_names=["highPriorEpPM"]))
ax = az.plot_trace(data.position,var_names=["highPriorEpPM"])
plt.tight_layout()
plt.savefig("highPriorEpisode_Trace.png")

print(az.summary(data.position,var_names=["highPriorselfPM"]))
ax = az.plot_trace(data.position,var_names=["highPriorselfPM"])
plt.tight_layout()
plt.savefig("highPriorSelf_Trace.png")

print(az.summary(data.position,var_names=["lowPriorEpSocPM"]))
ax = az.plot_trace(data.position,var_names=["lowPriorEpSocPM"])
plt.tight_layout()
plt.savefig("lowPriorEpSocial_Trace.png")

print(az.summary(data.position,var_names=["lowPriorselfSocPM"]))
ax = az.plot_trace(data.position,var_names=["lowPriorselfSocPM"])
plt.tight_layout()
plt.savefig("lowPriorselfSocial_Trace.png")

print(az.summary(data.position,var_names=["lowPriorselfEpPM"]))
ax = az.plot_trace(data.position,var_names=["lowPriorselfEpPM"])
plt.tight_layout()
plt.savefig("lowPriorselfEpisode_Trace.png")

print(az.summary(data.position,var_names=["lowPriorSocPM"]))
ax = az.plot_trace(data.position,var_names=["lowPriorSocPM"])
plt.tight_layout()
plt.savefig("lowPriorSocial_Trace.png")

print(az.summary(data.position,var_names=["lowPriorEpPM"]))
ax = az.plot_trace(data.position,var_names=["lowPriorEpPM"])
plt.tight_layout()
plt.savefig("lowPriorEpisode_Trace.png")

print(az.summary(data.position,var_names=["lowPriorselfPM"]))
ax = az.plot_trace(data.position,var_names=["lowPriorselfPM"])
plt.tight_layout()
plt.savefig("lowPriorSelf_Trace.png")

print(az.summary(data.position,var_names=["ImpEpSocS"]))
ax = az.plot_trace(data.position,var_names=["ImpEpSocS"])
plt.tight_layout()
plt.savefig("ImprovEpSocial_Trace.png")

print(az.summary(data.position,var_names=["highImpEpSocS"]))
ax = az.plot_trace(data.position,var_names=["highImpEpSocS"])
plt.tight_layout()
plt.savefig("HighImprovEpSocial_Trace.png")

print(az.summary(data.position,var_names=["lowImpEpSocS"]))
ax = az.plot_trace(data.position,var_names=["lowImpEpSocS"])
plt.tight_layout()
plt.savefig("LowImprovEpSocial_Trace.png")

# difference in d' between posterior and prior 
print(az.summary(data.position,var_names=["diffMu"]))
ax = az.plot_trace(data.position,var_names=["diffMu"])
plt.tight_layout()
plt.savefig("diffMuEpSocial_Trace.png")

# ratio of encoding variance  between posterior and prior 
print(az.summary(data.position,var_names=["diffVar"]))
ax = az.plot_trace(data.position,var_names=["diffVar"])
plt.tight_layout()
plt.savefig("diffVarEpSocial_Trace.png")

# posterior d' 
print(az.summary(data.position,var_names=["postMuP"]))
ax = az.plot_trace(data.position,var_names=["postMuP"])
plt.tight_layout()
plt.savefig("postMuPEpSocial_Trace.png")

# prior d'  (degenerate)
print(az.summary(data.position,var_names=["muPM"]))
ax = az.plot_trace(data.position,var_names=["muPM"])
plt.tight_layout()
plt.savefig("muPMEpSocial_Trace.png")

# posterior encoding variance 
print(az.summary(data.position,var_names=["postVarP"]))
ax = az.plot_trace(data.position,var_names=["postVarP"])
plt.tight_layout()
plt.savefig("postVarPEpSocial_Trace.png")

# prior encoding variance  (degenerate)
print(az.summary(data.position,var_names=["sigPM"]))
ax = az.plot_trace(data.position,var_names=["sigPM"])
plt.tight_layout()
plt.savefig("sigPMEpSocial_Trace.png")

# Unpaired t-test
def ttest(A,B):
 mA = jnp.where(A==1,B,0).sum()/(A==1).sum()
 mB = jnp.where(A==0,B,0).sum()/(A==0).sum()
 S = (jnp.where(A==1,(B-mA)**2,0).sum() + jnp.where(A==0,(B-mA)**2,0).sum())/(A.size-2)
 return (mA - mB)/jnp.sqrt(S/(A==1).sum() +S/(A==0).sum())

def ttest1Samp(A):
    return A.mean()/(A.std()/jnp.sqrt(A.size-1))
GLods = []
GLodCIs = []
LLods = []
Dists = []
RankDists = []
for i in range(5):
    plt.close('all')
    # Get whether the participant's biases for an activity cue shared the same rank as the familiarity we measure from ranking behavior
    Dists += [jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: (jstats.rankdata(A,'max')[i]==jstats.rankdata(B,'max')[i]).astype(int))),in_axes=[0,None]),in_axes=[0,None])(data.position['selfS'],jnp.exp(-jnp.array(RunsDist)))] 
    # T-test to test whether there's a difference of performance between when it accorded with participant's bias or not
    WISRankTTest = (jax.vmap(jax.vmap(ttest))(Dists[i],EpSocS[...,0,0]))
    WINRankTTest = (jax.vmap(jax.vmap(ttest))(Dists[i],EpSocS[...,1,0]))
    BWSRankTTest = (jax.vmap(jax.vmap(ttest))(Dists[i],EpSocS[...,0,1]))
    BWNRankTTest = (jax.vmap(jax.vmap(ttest))(Dists[i],EpSocS[...,1,1]))
    print(az.summary({"{0:d}_TTest".format(5-i):jnp.array([WISRankTTest,WINRankTTest,BWSRankTTest,BWNRankTTest]).transpose(1,2,0)}))
    az.plot_trace({"TTest":jnp.array([WISRankTTest,WINRankTTest,BWSRankTTest,BWNRankTTest]).transpose(1,2,0)})
    plt.savefig("{0:d}_TTest_Trace.png".format(5-i))
    plt.close('all')
    # Get odds ratio between whether it bias accordance improved or worsened performace
    GWISOdd = (WISRankTTest>0).sum(-1)/(WISRankTTest<0).sum(-1)
    # This is a 95% conf interval for odds
    GWISCI = 1.96*np.sqrt(1/(WISRankTTest>0).sum(-1) + 1/(WISRankTTest<0).sum(-1) + 2*1/WISRankTTest.shape[-1])
    GWINOdd = (WINRankTTest>0).sum(-1)/(WINRankTTest<0).sum(-1)
    GWINCI = 1.96*np.sqrt(1/(WINRankTTest>0).sum(-1) + 1/(WINRankTTest<0).sum(-1) + 2*1/WINRankTTest.shape[-1])
    GBWSOdd = (BWSRankTTest>0).sum(-1)/(BWSRankTTest<0).sum(-1)
    GBWSCI = 1.96*np.sqrt(1/(BWSRankTTest>0).sum(-1) + 1/(BWSRankTTest<0).sum(-1) + 2*1/BWSRankTTest.shape[-1])
    GBWNOdd = (BWNRankTTest>0).sum(-1)/(BWNRankTTest<0).sum(-1)
    GBWNCI = 1.96*np.sqrt(1/(BWNRankTTest>0).sum(-1) + 1/(BWNRankTTest<0).sum(-1) + 2*1/BWNRankTTest.shape[-1])
    GLods += [[1/GWISOdd.mean(),1/GWINOdd.mean(),1/GBWSOdd.mean(),1/GBWNOdd.mean()]] 
    GLodCIs += [[GWISOdd.std(),GWINOdd.std(),GBWSOdd.std(),GBWNOdd.std()]] 
# Plot all the odds
GLodCIs = np.array(GLodCIs)
plt.close('all')
plt.plot(np.log(np.array(GLods))[::-1],'-*')
colors=['r','b','g','orange']
for i in range(4):
    plt.fill_between(jnp.arange(5),np.log(np.array(GLods))[::-1,i]-(np.array(GLodCIs))[::-1,i],np.log(np.array(GLods))[::-1,i]+(np.array(GLodCIs))[::-1,i],alpha=0.7)
plt.xlabel("Steps From Self")
plt.xticks([0,1,2,3,4],([0,1,2,3,4]))
plt.axhline(np.log(10**0.5),color='black')
plt.axhline(-np.log(10**0.5),color='black')
plt.axhline(0,color='black')
plt.title("Log Odds Biased Yes (+) or No (-) Response")
plt.ylabel("Log Odds")
plt.legend(["W/I Social", "W/I NonSocial", "B/W Social", "B/W NonSocial"],loc='center left', bbox_to_anchor=(1., .5))
plt.savefig("GreaterOdds",bbox_inches='tight')


