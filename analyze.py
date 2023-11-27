import numpy as np
from sklearn.metrics import roc_curve,roc_auc_score
from pymer4.models import Lmer
from pymer4.stats import lrt
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json
import glob
import statsmodels.genmod.bayes_mixed_glm as smgb
import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.formula.api as smf

All = []
AllAcc = []
corrs = []
trueRank = np.array([[1,2,4,0,3],[2,1,0,4,3]])
rankAcc = []
RankConf = []
cCoef = []
PD = []
for ii,part in enumerate(sorted(glob.glob("data/*.csv"))):
    X = pd.read_csv(part)
    Runs = []
    RunAcc = []
    RunRankConf = []
    cCoefR = []
    PDR = []
    # for runs
    for k in range(2):
        if 'Stimuli' in X:
            stimuli = json.loads(X.Stimuli[k])
            situation = np.array(stimuli[1])
            persontoSit = [str(int(s.split("/")[2])-1) for s in situation[:,1]]
            ranking = json.loads(X.rankDec[k])
            RunRankConf += [(X.rankconf[k])]
            firstChoice = [ranking[str(i)]['0'] for i in persontoSit]
            secondChoice = [ranking[str(i)]['1'] for i in persontoSit]
            RunAcc +=[[np.array(firstChoice)==trueRank[k],np.array(secondChoice)==trueRank[k]]]            
            print(X.participant[k],(X.rankconf[k]),X.rankRT[k])
        else:
            continue
            
        corrChoice = np.array(json.loads(X.correctChoice[k]))
        choice = np.array(json.loads(X.Choice[k]))
        if len(choice) < 40:
            continue
        BWgroup = (json.loads(X.BWgroup[k]))
        Soc = (json.loads(X.Query[k]))
        performance = (corrChoice == choice)
        wiGaSoc = performance[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 0))[0]].mean()
        wiGaLoc = performance[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 1))[0]].mean()
        bwGaSoc = performance[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 0))[0]].mean()
        bwGaLoc = performance[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 1))[0]].mean()

        Soc = list(map(lambda x: "Social" if not x else "NonSocial",Soc))
        BWgroup = list(map(lambda x: "Between" if x else "Within",BWgroup))
        RT0 = np.array(json.loads(X.retrievalRT[k]))
        PDR += [[performance,Soc,BWgroup,RT0,np.repeat(ii,40),np.repeat(k,40)]]
        Conf0 = np.array(json.loads(X.retrievalConf[k]),dtype=float)
        RT0 = np.delete(RT0,np.where(Conf0!=Conf0)[0])
        Conf0 = np.delete(Conf0,np.where(Conf0!=Conf0)[0])
        corrs += [[RT0[:len(Conf0)],Conf0,performance[:len(Conf0)]]]
        print("Corr Run {0:d}".format(k),np.corrcoef(corrs[-1][0],corrs[-1][1])[0,1])
        cCoefR += [np.corrcoef(corrs[-1][0],corrs[-1][1])[0,1]]
        Runs += [[wiGaSoc,wiGaLoc,bwGaSoc,bwGaLoc]]
    PD += [PDR]
    cCoef += [cCoefR]
    RankConf += [RunRankConf]
    AllAcc += [RunAcc]
    All += [Runs]
RankRet = []
toPlot = []
All = np.array(All)
AllCompAcc = np.array(AllAcc).sum(-2,keepdims=True).mean(-1)
AllFirst = np.array(AllAcc)[...,0,:].mean(-1)
AllSecond = np.array(AllAcc)[...,1,:].mean(-1)
import scipy.stats as stats
RNum = [1,2]
ANOVA = ["WI_S","WI_NS", "BW_S", "BW_NS"]
C = np.concatenate(corrs,-1)
M = np.polyfit(C[0],C[1],1)[0]
for i in range(4):
    Runs = []
    RPlot = []
    for j in range(2):
        Ranks = []
        for k in range(1):
            Ranks += [np.corrcoef(AllCompAcc[:,j,k],All[:,j,i])[0,1]]
            RPlot += [[AllCompAcc[:,j,k],All[:,j,i]]]
            print(stats.pearsonr(AllCompAcc[:,j,k],All[:,j,i]),ANOVA[i],RNum[j],k+1)
        Runs += [Ranks]
    toPlot += [RPlot]
    RankRet += [Runs]
RankRet = np.array(RankRet).squeeze()
toPlot = np.array(toPlot).squeeze()
plt.ion()
fig,ax = plt.subplots(2,2,figsize=(8,8))
a = ax.ravel()
labs = ["W/I Social", "W/I NonSocial", "B/W Social", "B/W NonSocial"]
for i in range(len(a)):
    a[i].set_title(labs[i])
    a[i].scatter(toPlot[i,0,0],toPlot[i,0,1])
    a[i].scatter(toPlot[i,1,0],toPlot[i,1,1])
    l = a[i].legend(["{0:.3f}, {1:.3f}".format(*stats.pearsonr(toPlot[i,0,0],toPlot[i,0,1])), "{0:.3f}, {1:.3f}".format(*stats.pearsonr(toPlot[i,1,0],toPlot[i,1,1]))])

fig.supxlabel("Ranking Performance")
fig.supylabel("Recall Performance")
plt.tight_layout()
plt.savefig("WICorrBWCorr")
plt.figure()
print(toPlot.shape)
print(stats.pearsonr(np.concatenate([t[0,0] for t in toPlot],-1),np.concatenate([t[0,1] for t in toPlot],-1)))
print(stats.pearsonr(np.concatenate([t[1,0] for t in toPlot],-1),np.concatenate([t[1,1] for t in toPlot],-1)))
plt.scatter(np.concatenate([t[0,0] for t in toPlot],-1),np.concatenate([t[0,1] for t in toPlot],-1))
plt.scatter(np.concatenate([t[1,0] for t in toPlot],-1),np.concatenate([t[1,1] for t in toPlot],-1))
plt.figure()
plt.scatter(C[0],C[1])
plt.plot(C[0],M*C[0] +C[1].mean())
plt.ylabel("Confidence")
plt.xlabel("Response Time")
plt.title("Correlation {0:.3f}, p value {1:.3f}".format(*stats.pearsonr(C[0],C[1])))
plt.savefig("RTimeConf")
plt.figure()
plt.boxplot([C[1][C[2]==1],C[1][C[2]!=1]])
plt.xticks([1,2],['Correct','Incorrect'])
plt.title("T test {0:.3f}, p value {1:.3f}".format(*stats.ttest_ind(C[1][C[2]==1],C[1][C[2]!=1])))
plt.ylabel("Confidence")
plt.savefig("PerfConf")
PDP = [[pd.DataFrame({"performance":PD[i][j][0].astype(int),"Social":PD[i][j][1],"Episode":PD[i][j][2],"RT":PD[i][j][3],"Participant":PD[i][j][4],"Run":PD[i][j][5],"Ranking":(AllCompAcc[i,j].squeeze().repeat(40)),"Time":(np.arange(40))/40}) for j in range(2)] for i in range(6)]
PDPCat = pd.concat([PDP[i][j] for i in range(6) for j in range(2)],ignore_index=True)
PDPCat["RunPart"] = PDPCat["Participant"].astype(str)+PDPCat["Run"].astype(str)
PDPCat['Time'] -= PDPCat['Time'].mean()
PDPCat['Ranking'] -= PDPCat['Ranking'].mean()
model = Lmer('performance~ (1|Participant:Run) + Episode+Social+Episode:Social+Ranking+ Ranking:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
model2 = Lmer('performance~ (1|Participant:Run)+ Episode+Social+Episode:Social+Ranking+ Ranking:(Episode+Social+Episode:Social) + Time + Time:(Episode+Social+Episode:Social+Ranking+ Ranking:(Episode+Social+Episode:Social))',data=PDPCat,family='binomial')
fit = model.fit()
fit2 = model2.fit()
print(lrt([model,model2]))
plt.close('all')
plt.figure(figsize=[10,8])
plt.plot(fit['Estimate'].values, fit['Estimate'].keys(),"*")
for key,up,low in zip(fit['Estimate'].keys(), fit["2.5_ci"].values, fit["97.5_ci"].values):
    plt.plot([low,up],[key,key])
plt.axvline(0,color='red')
R2 = np.var(model.fits)/(np.var(model.fits)+model.ranef_var['Var'].values + np.var(model.residuals.var()))
R22 = np.var(model2.fits)/(np.var(model2.fits)+model2.ranef_var['Var'].values + np.var(model2.residuals.var()))
print("R2: ",R2)
plt.xlabel("Coeff Value")
plt.tight_layout()
plt.savefig("LMEFit")
print(fit)
model.data['EpisodeSocial'] = list(map(lambda a,b: a+":"+b,model.data['Episode'],model.data['Social']))
model.data['Ranking'] += AllCompAcc.mean()
g = sns.lmplot(x='Ranking',y='fits',hue='EpisodeSocial',data=model.data)#,col='Participant',col_wrap=3,capsize=.2, errorbar="se",kind="point", height=6, aspect=.75)
plt.savefig("LMEAnovaPlot")
plt.figure()
from scipy.interpolate import make_interp_spline

for e in ["Within","Between"]:
 for s in ["Social", "NonSocial"]:
  fpr,tpr,_=roc_curve(model.data.performance[np.logical_and(model.data.Episode==e,model.data.Social==s)], model.data.fits[ np.logical_and(model.data.Episode==e,model.data.Social==s)])
  dpr = pd.DataFrame({"fpr":fpr,"tpr":tpr}).groupby("fpr").mean().reset_index() 
  plt.plot(fpr,tpr,label="{0}:{1}, AUC:{2:0.3f}".format(e,s,roc_auc_score(model.data.performance[np.logical_and(model.data.Episode==e,model.data.Social==s)], model.data.fits[ np.logical_and(model.data.Episode==e,model.data.Social==s)])))
plt.plot([0,1],[0,1],label="Random")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.tight_layout()
plt.savefig("LMEAUC")
