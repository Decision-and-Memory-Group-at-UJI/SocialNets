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
planTime = []
AllConf = []
ExpTime = []
for ii,part in enumerate(sorted(glob.glob("data/*.csv"))):
    X = pd.read_csv(part)
    Runs = []
    RConf = []
    RunAcc = []
    RunRankConf = []
    cCoefR = []
    PDR = []
    rplanTime = []

    if len(json.loads(X.rankDec[0])['0']) != 2 or len(json.loads(X.rankDec[1])['0']) != 2:
        print(X.participant[1],X.rankDec)
        continue
    if type(X.correctChoice[0]) != str or type(X.correctChoice[1]) != str:
        print(X.participant[1],X.correctChoice)
        continue
    ExpTime += [X.timeExpDuration[1]/60]
    # for runs
    for k in range(2):
        if 'Stimuli' in X:
            stimuli = json.loads(X.Stimuli[k])
            situation = np.array(stimuli[1])
            persontoSit = [str(int(s.split("/")[2])-1) for s in situation[:,1]]
            ptSit = list(map(lambda x: int(x),persontoSit))
            ranking = json.loads(X.rankDec[k])
            RunRankConf += [(X.rankconf[k])]
            firstChoice = [ranking[str(i)]['0'] for i in persontoSit]
            secondChoice = [ranking[str(i)]['1'] for i in persontoSit]
            selfRank = np.array(json.loads(X.selfRanks[1])[k])
            pDist = [0 for kk in range(5)]
            for ki in range(1):
                for kk in range(5):
                    pRank = selfRank[ki]
                    if kk == pRank:
                        continue
                    for kkk in range(5):
                       if kkk == selfRank[ki]:
                           continue
                       pDist[kk] += 1/(ki+1)
                       pRank = secondChoice[pRank]
                       if pRank == kk:
                           break
#            print(firstChoice,secondChoice,ptSit[secondChoice[selfRank[ki]]],selfRank[ki])
            RunAcc +=[[np.array(firstChoice)==trueRank[k],np.array(secondChoice)==trueRank[k]]]            
            rplanTime += [X.rankRT[k]]
            #print(X.participant[1],(X.rankconf[k]),X.rankRT[k])
        else:
            continue
            
        corrChoice = np.array(json.loads(X.correctChoice[k]))
        choice = np.array(json.loads(X.Choice[k]))
        if len(choice) < 40:
            continue
        BWgroup = (json.loads(X.BWgroup[k]))
        Soc = (json.loads(X.Query[k]))
        performance = (corrChoice == choice)
        Conf0 = np.array(json.loads(X.retrievalConf[k]),dtype=float)
        selfDist = np.array(list(map(lambda x: pDist[x],json.loads(X.Pind[k]))))
        selfDist = np.exp(-selfDist)#1/(selfDist+1)
        wiGaSoc = performance[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 0))[0]].mean()
        wiGaLoc = performance[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 1))[0]].mean()
        bwGaSoc = performance[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 0))[0]].mean()
        bwGaLoc = performance[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 1))[0]].mean()
        CwiGaSoc = Conf0[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 0))[0]].mean()
        CwiGaLoc = Conf0[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 1))[0]].mean()
        CbwGaSoc = Conf0[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 0))[0]].mean()
        CbwGaLoc = Conf0[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 1))[0]].mean()

        Soc = list(map(lambda x: "Social" if not x else "NonSocial",Soc))
        BWgroup = list(map(lambda x: "Between" if x else "Within",BWgroup))
        RT0 = np.array(json.loads(X.retrievalRT[k]))
        PDR += [[performance,Soc,BWgroup,RT0,np.repeat(ii,40),np.repeat(k,40),np.repeat((X.rankconf[k]),40),Conf0,selfDist]] 
        RT0 = np.delete(RT0,np.where(Conf0!=Conf0)[0])
        Conf0 = np.delete(Conf0,np.where(Conf0!=Conf0)[0])
        corrs += [[RT0[:len(Conf0)],Conf0,performance[:len(Conf0)]]]
        cCoefR += [np.corrcoef(corrs[-1][0],corrs[-1][1])[0,1]]
        Runs += [[wiGaSoc,wiGaLoc,bwGaSoc,bwGaLoc]]
        RConf += [[CwiGaSoc,CwiGaLoc,CbwGaSoc,CbwGaLoc]]
    PD += [PDR]
    planTime += [rplanTime]
    cCoef += [cCoefR]
    RankConf += [RunRankConf]
    AllAcc += [RunAcc]
    All += [Runs]
    AllConf += [RConf]
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
PDP = [[pd.DataFrame({"performance":PD[i][j][0].astype(int),"Confidence":PD[i][j][-2],"SelfDist":PD[i][j][-1],"rankConf":PD[i][j][-3],"Social":PD[i][j][1],"Episode":PD[i][j][2],"RT":PD[i][j][3],"Participant":PD[i][j][4],"Run":PD[i][j][5],"Ranking":(AllCompAcc[i,j].squeeze().repeat(40)),"FRanking":(AllFirst[i,j].squeeze().repeat(40)),"SRanking":(AllSecond[i,j].squeeze().repeat(40)),"Time":(np.arange(40))/40}) for j in range(2)] for i in range(len(PD)) if (AllCompAcc).squeeze().mean(1)[i] > 0.25 and All.mean((1,2))[i] > 0.6]
PDPCat = pd.concat([PDP[i][j] for i in range(len(PDP)) for j in range(2)],ignore_index=True)
PDPCatCat = pd.concat([PDPCat,PDPCat],ignore_index=True)
tempz = PDPCatCat["performance"].values
tempz[len(PDPCat):] = PDPCat["Confidence"].values
PDPCatCat["PerfConf"] = tempz
tempz = np.zeros(len(PDPCatCat))
tempz[len(PDPCat):] = 1
PDPCatCat["PoC"] = tempz
PDPCat["RunPart"] = PDPCat["Participant"].astype(str)+PDPCat["Run"].astype(str)
PDPCat['Time'] -= PDPCat['Time'].mean()
PDPCat['RankingCont'] = PDPCat['FRanking'] - PDPCat['SRanking']
PDPCat['WRank'] = PDPCat['FRanking'] + 0.5*PDPCat['SRanking']
transform = lambda x: x
invtransform = lambda x: x
PDPCat['Ranking'] = transform(PDPCat['Ranking'])
PDPRm = PDPCat['Ranking'].mean()
PDPCat['Ranking'] -= PDPCat['Ranking'].mean()
PDPRm = PDPCat['WRank'].mean()
PDPCat['WRank'] -= PDPCat['WRank'].mean()
PDPCat['RRanking'] = stats.rankdata(PDPCat['Ranking'])
PDPCat['RRanking'] -= PDPCat['RRanking'].mean()
PDPCat['rankConf'] -= PDPCat['rankConf'].mean()
fPDPRm = PDPCat['FRanking'].mean()
sPDPRm = PDPCat['SRanking'].mean()
PDPCat['FRanking'] -= PDPCat['FRanking'].mean()
PDPCat['SRanking'] -= PDPCat['SRanking'].mean()
PDPCat['RankingCont'] -= PDPCat['RankingCont'].mean()

PDPCatCat["RunPart"] = PDPCatCat["Participant"].astype(str)+PDPCatCat["Run"].astype(str)
PDPCatCat['Time'] -= PDPCatCat['Time'].mean()
PDPSm = PDPCat['SelfDist'].mean()
PDPCat['SelfDist'] -= PDPCat['SelfDist'].mean()
PDPCatCat['RankingCont'] = PDPCatCat['FRanking'] - PDPCatCat['SRanking']
PDPCatCat['Ranking'] -= PDPCatCat['Ranking'].mean()
PDPCatCat['FRanking'] -= PDPCatCat['FRanking'].mean()
PDPCatCat['SRanking'] -= PDPCatCat['SRanking'].mean()
PDPCatCat['RankingCont'] -= PDPCatCat['RankingCont'].mean()

modelN = Lmer('performance~   (1|Participant:Run)+ Episode+Social+Episode:Social',data=PDPCat,family='binomial')
model = Lmer('performance~   (1|Participant:Run)+ Episode+Social+Episode:Social+ Ranking+  Ranking:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
modelS = Lmer('performance~   (1|Participant:Run)+ Episode+Social+Episode:Social+ SelfDist+  SelfDist:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
model3 = Lmer('performance~   (1|Participant:Run)+ Episode+Social+Episode:Social+ WRank+  WRank:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
modelf = Lmer('performance~  (1|Participant:Run)+ Episode+Social+Episode:Social+FRanking+ FRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
models = Lmer('performance~  (1|Participant:Run)+ Episode+Social+Episode:Social+SRanking+ SRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
modelfs = Lmer('performance~ (1|Participant:Run)+ Episode+Social+Episode:Social+FRanking+ FRanking:(Episode+Social+Episode:Social)+SRanking+ SRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
model2 = Lmer('performance~ (1|Participant:Run) + Episode+Social+Episode:Social+RankingCont+ RankingCont:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
Cmodel = Lmer('Confidence~ (1|Participant:Run) + Episode+Social+Episode:Social+Ranking+ Ranking:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
CmodelS = Lmer('Confidence~ (1|Participant:Run) + Episode+Social+Episode:Social+SelfDist+ SelfDist:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
Cmodelf = Lmer('Confidence~ (1|Participant:Run) + Episode+Social+Episode:Social+FRanking+ FRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
Cmodels = Lmer('Confidence~ (1|Participant:Run) + Episode+Social+Episode:Social+SRanking+ SRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
Cmodelfs = Lmer('Confidence~ (1|Participant:Run) + Episode+Social+Episode:Social+FRanking+ FRanking:(Episode+Social+Episode:Social)+SRanking+ SRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
Cmodel2 = Lmer('Confidence~ (1|Participant:Run) + Episode+Social+Episode:Social+RankingCont+ RankingCont:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
#CCmodel = Lmer('PerfConf~ (1|Participant:Run:PoC) + Episode+Social+Episode:Social+Ranking+ Ranking:(Episode+Social+Episode:Social)',data=PDPCatCat,family='gaussian')
#CCmodelf = Lmer('PerfConf~ (1|Participant:Run:PoC) + Episode+Social+Episode:Social+FRanking+ FRanking:(Episode+Social+Episode:Social)',data=PDPCatCat,family='gaussian')
#CCmodels = Lmer('PerfConf~ (1|Participant:Run:PoC) + Episode+Social+Episode:Social+SRanking+ SRanking:(Episode+Social+Episode:Social)',data=PDPCatCat,family='gaussian')
#CCmodelfs = Lmer('PerfConf~ (1|Participant:Run:PoC) + Episode+Social+Episode:Social+FRanking+ FRanking:(Episode+Social+Episode:Social)+SRanking+ SRanking:(Episode+Social+Episode:Social)',data=PDPCatCat,family='gaussian')
#CCmodel2 = Lmer('PerfConf~ (1|Participant:Run:PoC) + Episode+Social+Episode:Social+RankingCont+ RankingCont:(Episode+Social+Episode:Social)',data=PDPCatCat,family='gaussian')

fit = model.fit()
fitN = modelN.fit()
fitS = modelS.fit()
fitf = modelf.fit()
fits = models.fit()
fitfs = modelfs.fit()
fit2 = model2.fit()
fit3 = model3.fit()
Cfit = Cmodel.fit()
CfitS = CmodelS.fit()
Cfitf = Cmodelf.fit()
Cfits = Cmodels.fit()
Cfitfs = Cmodelfs.fit()
Cfit2 = Cmodel2.fit()
#CCfit = CCmodel.fit()
#CCfitf = CCmodelf.fit()
#CCfits = CCmodels.fit()
#CCfitfs = CCmodelfs.fit()
#CCfit2 = CCmodel2.fit()

print(lrt([modelN,model,modelf,models,modelfs,model2,model3,modelS]))
print(lrt([Cmodel,Cmodelf,Cmodels,Cmodelfs,Cmodel2,CmodelS]))
#print(lrt([CCmodel,CCmodelf,CCmodels,CCmodelfs,CCmodel2]))

plt.close('all')
plt.figure(figsize=[10,8])
plt.plot(fit['Estimate'].values, fit['Estimate'].keys(),"*")
for key,up,low in zip(fit['Estimate'].keys(), fit["2.5_ci"].values, fit["97.5_ci"].values):
    plt.plot([low,up],[key,key])
plt.axvline(0,color='red')
plt.xlabel("Coeff Value")
plt.tight_layout()
plt.savefig("LMEFit")
plt.figure(figsize=[10,8])
plt.plot(fitS['Estimate'].values, fitS['Estimate'].keys(),"*")
for key,up,low in zip(fitS['Estimate'].keys(), fitS["2.5_ci"].values, fitS["97.5_ci"].values):
    plt.plot([low,up],[key,key])
plt.axvline(0,color='red')
plt.xlabel("Coeff Value")
plt.tight_layout()
plt.savefig("LMEFitDist")
plt.figure(figsize=[10,8])
plt.plot(Cfit['Estimate'].values, Cfit['Estimate'].keys(),"*")
for key,up,low in zip(Cfit['Estimate'].keys(), Cfit["2.5_ci"].values, Cfit["97.5_ci"].values):
    plt.plot([low,up],[key,key])
plt.axvline(0,color='red')
plt.xlabel("Coeff Value")
plt.tight_layout()
plt.savefig("CLMEFit")

print(fit)
print(Cfit)
print(fitS)
model.data['EpisodeSocial'] = list(map(lambda a,b: a+":"+b,model.data['Episode'],model.data['Social']))
Cmodel.data['EpisodeSocial'] = list(map(lambda a,b: a+":"+b,Cmodel.data['Episode'],Cmodel.data['Social']))
modelS.data['EpisodeSocial'] = list(map(lambda a,b: a+":"+b,modelS.data['Episode'],modelS.data['Social']))
model.data['Ranking'] = invtransform(model.data['Ranking']+PDPRm)
modelS.data['SelfDist'] = invtransform(modelS.data['SelfDist']+PDPSm)
model.data['logfits'] = np.log(model.data['fits'])
modelS.data['logfits'] = np.log(modelS.data['fits'])

g = sns.lmplot(x='Ranking',y='fits',hue='EpisodeSocial',data=model.data,hue_order=sorted(model.data['EpisodeSocial'].unique()))#,col='Participant',col_wrap=3,capsize=.2, errorbar="se",kind="point", height=6, aspect=.75)
plt.savefig("LMEAnovaPlot")
g = sns.lmplot(x='SelfDist',y='fits',hue='EpisodeSocial',data=modelS.data,hue_order=sorted(model.data['EpisodeSocial'].unique()))#,col='Participant',col_wrap=3,capsize=.2, errorbar="se",kind="point", height=6, aspect=.75)
plt.savefig("LMEDistAnovaPlot")
Cmodel.data['Ranking'] += AllCompAcc.mean()
g = sns.lmplot(x='Ranking',y='fits',hue='EpisodeSocial',data=Cmodel.data,hue_order=sorted(model.data['EpisodeSocial'].unique()))#,col='Participant',col_wrap=3,capsize=.2, errorbar="se",kind="point", height=6, aspect=.75)
plt.savefig("CLMEAnovaPlot")

from scipy.interpolate import make_interp_spline

plt.figure()
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

plt.figure()
for e in ["Within","Between"]:
 for s in ["Social", "NonSocial"]:
  fpr,tpr,_=roc_curve(modelS.data.performance[np.logical_and(modelS.data.Episode==e,modelS.data.Social==s)], modelS.data.fits[ np.logical_and(modelS.data.Episode==e,modelS.data.Social==s)])
  dpr = pd.DataFrame({"fpr":fpr,"tpr":tpr}).groupby("fpr").mean().reset_index() 
  plt.plot(fpr,tpr,label="{0}:{1}, AUC:{2:0.3f}".format(e,s,roc_auc_score(modelS.data.performance[np.logical_and(modelS.data.Episode==e,modelS.data.Social==s)], modelS.data.fits[ np.logical_and(modelS.data.Episode==e,modelS.data.Social==s)])))
plt.plot([0,1],[0,1],label="Random")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.tight_layout()
plt.savefig("LMEDistAUC")
