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

with open('Posterior_FullJoint.pkl', 'rb') as f:
    data = pickle.load(f)
print(data.logdensity.shape)
data = jax.tree_map(lambda x: x[:,::1],data)

# Load data
Res = np.concatenate([np.load("distrep1Collect.npy"),np.load("distrep2Collect.npy")[:,::-1]],0)
Pind = np.concatenate([np.load("Pind1Collect.npy"),np.load("Pind2Collect.npy")[:,::-1]],0)
Ranks = np.concatenate([np.load("Rankingrep1.npy"),np.load("Rankingrep2.npy")[:,::-1]],0).transpose(0,2,1)
Cues = Res[...,-3,:]
Dists = Res[...,-1,:]
Social = Res[...,0,:]

# Get steps from participant to each cue
RunsDist = [[[np.unique(Dists[k,j][Persons[k,j]==i]).squeeze() for i in range(5)] for j in range(2)] for k in range(115)]

obs = Res[:,:,0]
Social = Res[:,:,1]
Episode = Res[:,:,2]

EpSoc = 2*Social + Episode
PPred = data.position['posteriorPredictive']

# Posteriori Within person Social memory recall ability
WIS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==0,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)
# Posterior Between person Social memory recall ability
BWS = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==1,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)
# Posterior Within person NonSocial memory recall ability
WIN = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==2,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)
# Posterior Between person NonSocial memory recall ability
BWN = jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: jnp.where(B==3,A,0).max())),in_axes=[0,None]),in_axes=[0,None])(PPred,EpSoc)

print("Getting Summary")
invlogit = lambda x: 1/(1+jnp.exp(-x))
CoVul = lambda x,a,b: a + (b-a)*invlogit(x)
# 95% Confidence interval calculation for the logistic parameter given each sampled population mean and std
data.position['p95selfEpSocPM'] = data.position['selfEpSocPM'] + 1.96*data.position['selfEpSocPS']
data.position['p5selfEpSocPM'] = data.position['selfEpSocPM'] - 1.96*data.position['selfEpSocPS']
# Transform population mean with logistic function to its Bernoulli probability form
data.position['selfEpSocPM'] = CoVul(data.position['selfEpSocPM'],0,1)
# Get marginal probabilities for BW/WI and Social/NonSocial memory interactions
data.position['EpSocPM'] = data.position['selfEpSocPM'].mean((2,-1))
# for activity cue and Social memory interaction
data.position['selfSocPM'] = data.position['selfEpSocPM'].mean(-2)
# for activity cue and BW/WI episode stimuli interaction
data.position['selfEpPM'] = data.position['selfEpSocPM'].mean(-3)
# for activity cue main effect
data.position['selfPM'] = data.position['selfEpSocPM'].mean((-2,-3))
# for BW/WI episode stimuli main effect
data.position['EpPM'] = data.position['selfEpSocPM'].mean((2,-1,-3))
# For Social/NonSocial memory main effect
data.position['SocPM'] = data.position['selfEpSocPM'].mean((2,-1,-2))

# The same but for the 95% confidence intervals
data.position['p95selfEpSocPM'] = CoVul(data.position['p95selfEpSocPM'],0,1)
data.position['p95EpSocPM'] = data.position['p95selfEpSocPM'].mean((2,-1))
data.position['p95selfSocPM'] = data.position['p95selfEpSocPM'].mean(-2)
data.position['p95selfEpPM'] = data.position['p95selfEpSocPM'].mean(-3)
data.position['p95selfPM'] = data.position['p95selfEpSocPM'].mean((-2,-3))
data.position['p95EpPM'] = data.position['p95selfEpSocPM'].mean((2,-1,-3))
data.position['p95SocPM'] = data.position['p95selfEpSocPM'].mean((2,-1,-2))

data.position['p5selfEpSocPM'] = CoVul(data.position['p5selfEpSocPM'],0,1)
data.position['p5EpSocPM'] = data.position['p5selfEpSocPM'].mean((2,-1))
data.position['p5selfSocPM'] = data.position['p5selfEpSocPM'].mean(-2)
data.position['p5selfEpPM'] = data.position['p5selfEpSocPM'].mean(-3)
data.position['p5selfPM'] = data.position['p5selfEpSocPM'].mean((-2,-3))
data.position['p5EpPM'] = data.position['p5selfEpSocPM'].mean((2,-1,-3))
data.position['p5SocPM'] = data.position['p5selfEpSocPM'].mean((2,-1,-2))

# Get subject level logistic parameter
data.position['selfS'] = data.position['selfEpSocS'].mean((-2,-3))

# Print summaries and plot MCMC traces
print(az.summary(data.position,var_names=["EpSocPM"]))
ax = az.plot_trace(data.position,var_names=["EpSocPM"])
plt.tight_layout()
plt.savefig("EpSocial_Trace.png")

print(az.summary(data.position,var_names=["selfSocPM"]))
ax = az.plot_trace(data.position,var_names=["selfSocPM"])
plt.tight_layout()
plt.savefig("selfSocial_Trace.png")

print(az.summary(data.position,var_names=["selfEpPM"]))
ax = az.plot_trace(data.position,var_names=["selfEpPM"])
plt.tight_layout()
plt.savefig("selfEpisode_Trace.png")

print(az.summary(data.position,var_names=["SocPM"]))
ax = az.plot_trace(data.position,var_names=["SocPM"])
plt.tight_layout()
plt.savefig("Social_Trace.png")

print(az.summary(data.position,var_names=["EpPM"]))
ax = az.plot_trace(data.position,var_names=["EpPM"])
plt.tight_layout()
plt.savefig("Episode_Trace.png")

print(az.summary(data.position,var_names=["selfPM"]))
ax = az.plot_trace(data.position,var_names=["selfPM"])
plt.tight_layout()
plt.savefig("Self_Trace.png")

print(az.summary(data.position,var_names=["p95EpSocPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p95EpSocPM"])
plt.tight_layout()
plt.savefig("EpSocial95p_Trace.png")

print(az.summary(data.position,var_names=["p95selfSocPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p95selfSocPM"])
plt.tight_layout()
plt.savefig("selfSocial95p_Trace.png")

print(az.summary(data.position,var_names=["p95selfEpPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p95selfEpPM"])
plt.tight_layout()
plt.savefig("selfEpisode95p_Trace.png")

print(az.summary(data.position,var_names=["p95SocPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p95SocPM"])
plt.tight_layout()
plt.savefig("Social95p_Trace.png")

print(az.summary(data.position,var_names=["p95EpPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p95EpPM"])
plt.tight_layout()
plt.savefig("Episode95p_Trace.png")

print(az.summary(data.position,var_names=["p95selfPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p95selfPM"])
plt.tight_layout()
plt.savefig("Self95p_Trace.png")

print(az.summary(data.position,var_names=["p5EpSocPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p5EpSocPM"])
plt.tight_layout()
plt.savefig("EpSocial5p_Trace.png")

print(az.summary(data.position,var_names=["p5selfSocPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p5selfSocPM"])
plt.tight_layout()
plt.savefig("selfSocial5p_Trace.png")

print(az.summary(data.position,var_names=["p5selfEpPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p5selfEpPM"])
plt.tight_layout()
plt.savefig("selfEpisode5p_Trace.png")

print(az.summary(data.position,var_names=["p5SocPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p5SocPM"])
plt.tight_layout()
plt.savefig("Social5p_Trace.png")

print(az.summary(data.position,var_names=["p5EpPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p5EpPM"])
plt.tight_layout()
plt.savefig("Episode5p_Trace.png")

print(az.summary(data.position,var_names=["p5selfPM"]))
ax = az.plot_trace(data.position,combined=True,var_names=["p5selfPM"])
plt.tight_layout()
plt.savefig("Self5p_Trace.png")


# Independent sample TTest... though log Odds for the hypothesis testing doesn't need this, just the means Lol
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
for i in range(5):
    plt.close('all')
    # Get samples for cues probabilities that do and do not occupy i steps from the participant
    Dists += [jax.vmap(jax.vmap(jax.vmap(jax.vmap(lambda A,B: (jstats.rankdata(A,'max')[i]==jstats.rankdata(B,'max')[i]).astype(int))),in_axes=[0,None,None]),in_axes=[0,None,None])(data.position['selfS'],jnp.exp(-jnp.array(RunsDist)))] 

    # ttest between cues that are (5-i) steps from participants and that are not i steps from the participant for each social memory and episode memory type attribute
    WISRankCorr = (jax.vmap(jax.vmap(ttest))(Dists[i],WIS))
    WINRankCorr = (jax.vmap(jax.vmap(ttest))(Dists[i],WIN))
    BWSRankCorr = (jax.vmap(jax.vmap(ttest))(Dists[i],BWS))
    BWNRankCorr = (jax.vmap(jax.vmap(ttest))(Dists[i],BWN))

    # Print TTest summary for this step
    print(az.summary({"{0:d}_TTest".format(5-i):jnp.array([WISRankCorr,WINRankCorr,BWSRankCorr,BWNRankCorr]).transpose(1,2,0)}))
    az.plot_trace({"TTest":jnp.array([WISRankCorr,WINRankCorr,BWSRankCorr,BWNRankCorr]).transpose(1,2,0)})
    plt.savefig("{0:d}_TTest_Trace.png".format(5-i))
    GWISOdd = (WISRankCorr>0).sum(-1)/(WISRankCorr<0).sum(-1)
    GWISCI = 1.96*np.sqrt(1/(WISRankCorr>0).sum(-1) + 1/(WISRankCorr<0).sum(-1) + 2*1/WISRankCorr.size)

    # Get LogOdds for the attribuets
    GWINOdd = (WINRankCorr>0).sum(-1)/(WINRankCorr<0).sum(-1)
    GWINCI = 1.96*np.sqrt(1/(WINRankCorr>0).sum(-1) + 1/(WINRankCorr<0).sum(-1) + 2*1/WINRankCorr.size)

    GBWSOdd = (BWSRankCorr>0).sum(-1)/(BWSRankCorr<0).sum(-1)
    GBWSCI = 1.96*np.sqrt(1/(BWSRankCorr>0).sum(-1) + 1/(BWSRankCorr<0).sum(-1) + 2*1/BWSRankCorr.size)

    GBWNOdd = (BWNRankCorr>0).sum(-1)/(BWNRankCorr<0).sum(-1)
    GBWNCI = 1.96*np.sqrt(1/(BWNRankCorr>0).sum(-1) + 1/(BWNRankCorr<0).sum(-1) + 2*1/BWNRankCorr.size)

    GLods += [[GWISOdd.mean(),GWINOdd.mean(),GBWSOdd.mean(),GBWNOdd.mean()]] 
    GLodCIs += [[GWISOdd.std(),GWINOdd.std(),GBWSOdd.std(),GBWNOdd.std()]] 
# Visualize log odds
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
plt.title("Log Odds that Performance Improves")
plt.ylabel("Log Odds")
plt.legend(["W/I Social", "W/I NonSocial", "B/W Social", "B/W NonSocial"],loc='center left', bbox_to_anchor=(1., .5))
plt.savefig("GreaterOdds",bbox_inches='tight')
