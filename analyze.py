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
import matplotlib
matplotlib.use('agg')
matplotlib.rcParams.update({"font.size":12})

All = []
AllAcc = []
corrs = []
trueRank = np.array([[2,1,0,4,3],[1,2,4,0,3]])
rankAcc = []
RankConf = []
cCoef = []
PD = []
planTime = []
AllConf = []
pDistsAll = []
ExpTime = []
predR = []
toSave = []
ptSits = []
def analyze(ii,part,trueRank):
    X = pd.read_csv(part)
    Runs = []
    RConf = []
    RunAcc = []
    RunRankConf = []
    cCoefR = []
    PDR = []
    rplanTime = []
    rpDist = []
    rPredR = []
    ExpTime = X.timeExpDuration[1]/60

    toSave = []
    ptSits = []
    # for runs
    for k in range(2):
        stimuli = json.loads(X.Stimuli[k])
        situation = np.array(stimuli[1])
        persontoSit = [str(int(s.split("/")[2])-1) for s in situation[:,1]]
        ptSit = list(map(lambda x: int(x),persontoSit))
        ptSits += [ptSit]
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
                found = False
                for kkk in range(5):
                   if kkk == selfRank[ki]:
                       continue
                   pDist[kk] += 1/(ki+1)
                   pRank = secondChoice[pRank]
                   if pRank == kk:
                       found = True
                       break
                if not found:
                    pDist[kk] = 100
        RunAcc +=[[np.array(firstChoice)==trueRank[k],np.array(secondChoice)==trueRank[k]]]            
        rPredR += [[np.array(firstChoice),np.array(secondChoice)]]
        rplanTime += [X.rankRT[k]]
        rpDist += [pDist]
        corrChoice = np.array(json.loads(X.correctChoice[k]))
        choice = np.array(json.loads(X.Choice[k]))
        if len(choice) < 40:
            continue
        BWgroup = (json.loads(X.BWgroup[k]))
        Soc = (json.loads(X.Query[k]))
        performance = (corrChoice == choice)
        Conf0 = np.array(json.loads(X.retrievalConf[k]),dtype=float)
        pDist = np.array(pDist)
        ptSit = np.array(ptSit)
        selfDist = np.array(list(map(lambda x: pDist[x==ptSit],json.loads(X.Pind[k])))).squeeze()
        # Cues shown at each trial
        Pind = np.array(list(map(lambda x: ptSit[x],json.loads(X.Pind[k])))).squeeze()
        # Participant distance (steps) to each cue
        rawDist = np.copy(np.array(list(map(lambda x: pDist[x==ptSit],json.loads(X.Pind[k])))).squeeze())
        selfDist = np.exp(-2**selfDist)#1/(selfDist+1)
        wiGaSoc = performance[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 0))[0]].sum()
        wiGaLoc = performance[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 1))[0]].sum()
        bwGaSoc = performance[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 0))[0]].sum()
        bwGaLoc = performance[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 1))[0]].sum()

        CwiGaSoc = Conf0[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 0))[0]].mean()
        CwiGaLoc = Conf0[np.where(np.logical_and(np.array(BWgroup) == 0,np.array(Soc) == 1))[0]].mean()
        CbwGaSoc = Conf0[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 0))[0]].mean()
        CbwGaLoc = Conf0[np.where(np.logical_and(np.array(BWgroup) == 1,np.array(Soc) == 1))[0]].mean()
        SocInt = np.array(Soc)
        BWgroupInt = np.array(BWgroup)
        toSave += [[performance,SocInt,BWgroupInt,Pind,Conf0,rawDist]]
        Soc = list(map(lambda x: "Social" if not x else "NonSocial",Soc))
        BWgroup = list(map(lambda x: "Between" if x else "Within",BWgroup))
        RT0 = np.array(json.loads(X.retrievalRT[k]))
        PDR += [[performance,Soc,BWgroup,RT0,np.repeat(ii,40),np.repeat(k,40),np.repeat((X.rankconf[k]),40),Conf0,selfDist]] 
        RT0 = np.delete(RT0,np.where(Conf0!=Conf0)[0])
        Conf0 = np.delete(Conf0,np.where(Conf0!=Conf0)[0])
        Runs += [[wiGaSoc,wiGaLoc,bwGaSoc,bwGaLoc]]
        RConf += [[CwiGaSoc,CwiGaLoc,CbwGaSoc,CbwGaLoc]]
    return PDR,rpDist,rplanTime,RunRankConf,RunAcc,rPredR,Runs,RConf,ExpTime,ptSits,toSave
for ii,part in enumerate(list(sorted(glob.glob("data/*.csv")))):
    X = pd.read_csv(part)
    if len(json.loads(X.rankDec[0])['0']) != 2 or len(json.loads(X.rankDec[1])['0']) != 2:
        continue
    if type(X.correctChoice[0]) != str or type(X.correctChoice[1]) != str:
        continue
    PDR,rpDist,rPlanTime,RunRankConf,RunAcc,rPredR,Runs,RConf,ETime,ptSit,tSave = analyze(ii,part,trueRank)
    PD += [PDR]
    toSave += [tSave]
    ptSits += [ptSit]
    pDistsAll += [rpDist]
    planTime += [rPlanTime]
    RankConf += [RunRankConf]
    AllAcc += [RunAcc]
    predR += [rPredR]
    All += [Runs]
    AllConf += [RConf]    
    ExpTime += [ETime]
All = np.array(All)
AllCompAcc = np.array(AllAcc).sum(-2,keepdims=True).mean(-1)
AllFirst = np.array(AllAcc)[...,0,:].mean(-1)
AllSecond = np.array(AllAcc)[...,1,:].mean(-1)
np.save("distrep2Collect",[toSave[i] for i in range(len(All)) if AllCompAcc.mean(1)[i] > 0.2 and All.mean((1,2))[i]/10 > 0.6])
np.save("Rankingrep2",[[AllCompAcc.squeeze()[i],AllFirst[i],AllSecond[i]] for i in range(len(All)) if AllCompAcc.mean(1)[i] > 0.2 and All.mean((1,2))[i]/10 > 0.6])
np.save("Attr2Collect",[All[i]/10 for i in range(len(All)) if AllCompAcc.mean(1)[i] > 0.2 and All.mean((1,2))[i]/10 > 0.6])
np.save("Pind2Collect",[ptSits[i] for i in range(len(All)) if AllCompAcc.mean(1)[i] > 0.2 and All.mean((1,2))[i]/10 > 0.6])
All = All/10
import scipy.stats as stats

PDPA = [[pd.DataFrame({"performance":PD[i][j][0].astype(int),"Confidence":PD[i][j][-2],"SelfDist":PD[i][j][-1],"rankConf":PD[i][j][-3],"Social":PD[i][j][1],"Episode":PD[i][j][2],"RT":PD[i][j][3],"Participant":PD[i][j][4],"Run":PD[i][j][5],"Ranking":(AllCompAcc[i,j].squeeze().repeat(40)),"FRanking":(AllFirst[i,j].squeeze().repeat(40)),"SRanking":(AllSecond[i,j].squeeze().repeat(40)),"Time":(np.arange(40))/40}) for j in range(2)] for i in range(len(PD)) if AllCompAcc.mean((1))[i] > 0.2 and All.mean((1,2))[i] > 0.6]
print(len(PDPA))
print((np.argsort(np.mean(np.array(predR),0))))
print((np.argsort(np.mean(np.array(predR),0)) - trueRank)==0)
trueRank = np.array([[1,2,4,0,3],[2,1,0,4,3]])
#trueRank = np.array([[3, 1, 4, 0, 2],[2, 3, 0, 1, 4]])
PD = []# [PDR]
pDistsAll = []# [rpDist]
planTime = []# [rplanTime]
RankConf = []# [RunRankConf]
AllAcc = []# [RunAcc]
predR = []# [rPredR]
All = []# [Runs]
AllConf = []# [RConf]    
toSave = []
ptSits = []

for ii,part in enumerate(list(sorted(glob.glob("dataRe*/*.csv")))):
    ii = ii + len(list(glob.glob("dataRe*/*.csv")))
    X = pd.read_csv(part)
    if len(json.loads(X.rankDec[0])['0']) != 2 or len(json.loads(X.rankDec[1])['0']) != 2:
        continue
    if type(X.correctChoice[0]) != str or type(X.correctChoice[1]) != str:
        continue
    PDR,rpDist,rPlanTime,RunRankConf,RunAcc,rPredR,Runs,RConf,ETime,ptSit,tSave = analyze(ii,part,trueRank)
    ptSits += [ptSit]
    toSave += [tSave]
    PD += [PDR]
    pDistsAll += [rpDist]
    planTime += [rPlanTime]
    RankConf += [RunRankConf]
    AllAcc += [RunAcc]
    predR += [rPredR]
    All += [Runs]
    AllConf += [RConf]    
    ExpTime += [ETime]

All = np.array(All)
AllCompAcc = np.array(AllAcc).sum(-2,keepdims=True).mean(-1)
AllFirst = np.array(AllAcc)[...,0,:].mean(-1)
AllSecond = np.array(AllAcc)[...,1,:].mean(-1)
np.save("distrep1Collect",[toSave[i] for i in range(len(All)) if AllCompAcc.mean(1)[i] > 0.2 and All.mean((1,2))[i]/10 > 0.6])
np.save("Rankingrep1",[[AllCompAcc.squeeze()[i],AllFirst[i],AllSecond[i]] for i in range(len(All)) if AllCompAcc.mean(1)[i] > 0.2 and All.mean((1,2))[i]/10 > 0.6])
np.save("Pind1Collect",[ptSits[i] for i in range(len(All)) if AllCompAcc.mean(1)[i] > 0.2 and All.mean((1,2))[i]/10 > 0.6])
np.save("Attr1Collect",[All[i]/10 for i in range(len(All)) if AllCompAcc.mean(1)[i] > 0.2 and All.mean((1,2))[i]/10 > 0.6])
All = All/10
print((np.argsort(np.mean(np.array(predR),0))))
print((np.argsort(np.mean(np.array(predR),0)) - trueRank)==0)

import scipy.stats as stats

PDPB = [[pd.DataFrame({"performance":PD[i][j][0].astype(int),"Confidence":PD[i][j][-2],"SelfDist":PD[i][j][-1],"rankConf":PD[i][j][-3],"Social":PD[i][j][1],"Episode":PD[i][j][2],"RT":PD[i][j][3],"Participant":PD[i][j][4],"Run":PD[i][j][5],"Ranking":(AllCompAcc[i,j].squeeze().repeat(40)),"FRanking":(AllFirst[i,j].squeeze().repeat(40)),"SRanking":(AllSecond[i,j].squeeze().repeat(40)),"Time":(np.arange(40))/40}) for j in range(2)] for i in range(len(PD)) if AllCompAcc.mean((1))[i] > 0.2 and  All.mean((1,2))[i] > 0.6]

print(len(PDPB))
Rfits = []
Cfits = []
Pfits = []
RModels = []
CModels = []
pModels = []
PDPCatA = pd.concat([PDPA[i][j] for i in np.random.permutation(len(PDPA))[:] for j in range(2)],ignore_index=True)
PDPCatB = pd.concat([PDPB[i][j] for i in np.random.permutation(len(PDPB))[:] for j in range(2)],ignore_index=True)

PDPCat = pd.concat([PDPCatA,PDPCatB],ignore_index=True)

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

model = Lmer('performance~   ((1+Time)|Participant:Run)+ Episode+Social+Episode:Social',data=PDPCat,family='binomial')
modelS = Lmer('performance~   ((1+Time)|Participant:Run)+ Episode+Social+Episode:Social+ SelfDist+  SelfDist:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
modelfS = Lmer('performance ~ ((1+Time)|Participant:Run)+ Episode+Social+Episode:Social+ SelfDist+FRanking+ SelfDist:(Episode+Social+Episode:Social) + FRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
modelf = Lmer('performance~  ((1+Time)|Participant:Run)+ Episode+Social+Episode:Social+FRanking+ FRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='binomial')
Cmodel = Lmer('Confidence ~   ((1+Time)|Participant:Run)+ Episode+Social+Episode:Social',data=PDPCat,family='gaussian')
CmodelS = Lmer('Confidence~ ((1+Time)|Participant:Run) + Episode+Social+Episode:Social+SelfDist+ SelfDist:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
Cmodelf = Lmer('Confidence~ ((1+Time)|Participant:Run) + Episode+Social+Episode:Social+FRanking+ FRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
CmodelfS = Lmer('Confidence~   ((1+Time)|Participant:Run)+ Episode+Social+Episode:Social+ SelfDist+FRanking+ SelfDist:(Episode+Social+Episode:Social) + FRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
Rmodel = Lmer('RT ~   ((1+Time)|Participant:Run)+ Episode+Social+Episode:Social',data=PDPCat,family='gaussian')
RmodelS = Lmer('RT~ ((1+Time)|Participant:Run) + Episode+Social+Episode:Social+SelfDist+ SelfDist:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
Rmodelf = Lmer('RT~ ((1+Time)|Participant:Run) + Episode+Social+Episode:Social+FRanking+ FRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')
RmodelfS = Lmer('RT~   ((1+Time)|Participant:Run)+ Episode+Social+Episode:Social+ SelfDist+FRanking+ SelfDist:(Episode+Social+Episode:Social) + FRanking:(Episode+Social+Episode:Social)',data=PDPCat,family='gaussian')

fitfS = modelfS.fit()
CfitfS = CmodelfS.fit()
RfitfS = RmodelfS.fit()
Rfits += [RfitfS]
Pfits += [fitfS]
Cfits += [CfitfS]
pModels += [modelfS]
RModels += [RmodelfS]
CModels += [CmodelfS]

print(lrt([model,modelf,modelS]))
print(lrt([Cmodel,Cmodelf,CmodelS]))
print(lrt([Rmodel,Rmodelf,RmodelS]))

print(fit)
print(fitf)
print(Cfit)
print(Cfitf)
print(fitS)
CmodelfS.data['EpisodeSocial'] = list(map(lambda a,b: a+":"+b,CmodelfS.data['Episode'],CmodelfS.data['Social']))
modelfS.data['EpisodeSocial'] = list(map(lambda a,b: a+":"+b,modelfS.data['Episode'],modelfS.data['Social']))
modelfS.data['FRanking'] = invtransform(modelfS.data['FRanking']+fPDPRm)
modelfS.data['SelfDist'] = invtransform(modelfS.data['SelfDist']+PDPSm)
CmodelfS.data['FRanking'] = invtransform(CmodelfS.data['FRanking']+fPDPRm)
CmodelfS.data['SelfDist'] = invtransform(CmodelfS.data['SelfDist']+PDPSm)
RmodelfS.data['FRanking'] = invtransform(RmodelfS.data['FRanking']+fPDPRm)
RmodelfS.data['SelfDist'] = invtransform(RmodelfS.data['SelfDist']+PDPSm)

g = sns.lmplot(x='FRanking',y='fits',hue='EpisodeSocial',data=modelfS.data,hue_order=sorted(modelfS.data['EpisodeSocial'].unique()))
plt.savefig("FullRepLMEAnovaPlot")
g = sns.lmplot(x='SelfDist',y='fits',hue='EpisodeSocial',data=modelfS.data,hue_order=sorted(modelfS.data['EpisodeSocial'].unique()))
plt.savefig("FullRepLMEDistAnovaPlot")
g = sns.lmplot(x='FRanking',y='fits',hue='EpisodeSocial',data=CmodelfS.data,hue_order=sorted(modelf.data['EpisodeSocial'].unique()))
plt.savefig("FullRepCLMEAnovaPlot")

g = sns.lmplot(x='SelfDist',y='fits',hue='EpisodeSocial',data=CmodelfS.data,hue_order=sorted(modelfS.data['EpisodeSocial'].unique()))
plt.savefig("FullRepCLMEDistAnovaPlot")
plt.close('all')

sns.barplot(x='Social',y='fits',data=CmodelfS.data,ci=99.9,order=sorted(np.unique(CmodelfS.data.Social.values)))
plt.savefig("FullRepSocialConf")
plt.close('all')

sns.lmplot(x='SelfDist',y='fits',data=CmodelfS.data,hue='Social',ci=99.9,hue_order=sorted(np.unique(CmodelfS.data.Social.values)))
plt.savefig("FullRepSocialDistInteractionConf")
plt.close('all')

sns.lmplot(x='FRanking',y='fits',data=CmodelfS.data,hue='Social',ci=99.9,hue_order=sorted(np.unique(CmodelfS.data.Social.values)))
plt.savefig("FullRepSocialRankInteractionConf")
plt.close('all')

sns.barplot(x='Episode',y='fits',data=CmodelfS.data,hue='Social',ci=99.9,hue_order=sorted(np.unique(CmodelfS.data.Social.values)),order=sorted(np.unique(CmodelfS.data.Episode.values)))
plt.savefig("FullRepSocialEpisodeInteractionConf")
plt.close('all')

sns.barplot(x='Episode',y='fits',data=CmodelfS.data,ci=99.9,order=sorted(np.unique(CmodelfS.data.Episode.values)))
plt.savefig("FullRepEpisodeConf")
plt.close('all')

sns.lmplot(x='SelfDist',y='fits',data=CmodelfS.data,hue='Episode',ci=99.9,hue_order=sorted(np.unique(CmodelfS.data.Episode.values)))
plt.savefig("FullRepEpisodeDistInteractionConf")
plt.close('all')

sns.lmplot(x='FRanking',y='fits',data=CmodelfS.data,hue='Episode',ci=99.9,hue_order=sorted(np.unique(CmodelfS.data.Episode.values)))
plt.savefig("FullRepEpisodeRankInteractionConf")
plt.close('all')

sns.barplot(x='Social',y='fits',data=modelfS.data,ci=99.9,order=sorted(np.unique(modelfS.data.Social.values)))
plt.savefig("FullRepSocialPerf")
plt.close('all')

sns.lmplot(x='SelfDist',y='fits',data=modelfS.data,hue='Social',ci=99.9,hue_order=sorted(np.unique(modelfS.data.Social.values)))
plt.savefig("FullRepSocialDistInteractionPerf")
plt.close('all')

sns.lmplot(x='FRanking',y='fits',data=modelfS.data,hue='Social',ci=99.9,hue_order=sorted(np.unique(modelfS.data.Social.values)))
plt.savefig("FullRepSocialRankInteractionPerf")
plt.close('all')

sns.barplot(x='Episode',y='fits',data=modelfS.data,hue='Social',ci=99.9,hue_order=sorted(np.unique(modelfS.data.Social.values)),order=sorted(np.unique(modelfS.data.Episode.values)))
plt.savefig("FullRepSocialEpisodeInteractionPerf")
plt.close('all')

sns.barplot(x='Episode',y='fits',data=modelfS.data,ci=99.9,order=sorted(np.unique(modelfS.data.Episode.values)))
plt.savefig("FullRepEpisodePerf")
plt.close('all')

sns.lmplot(x='SelfDist',y='fits',data=modelfS.data,hue='Episode',ci=99.9,hue_order=sorted(np.unique(modelfS.data.Episode.values)))
plt.savefig("FullRepEpisodeDistInteractionPerf")
plt.close('all')

sns.lmplot(x='FRanking',y='fits',data=modelfS.data,hue='Episode',ci=99.9,hue_order=sorted(np.unique(modelfS.data.Episode.values)))
plt.savefig("FullRepEpisodeRankInteractionPerf")
plt.close('all')

sns.barplot(x='Social',y='fits',data=RmodelfS.data,ci=99.9,order=sorted(np.unique(RmodelfS.data.Social.values)))
plt.savefig("FullRepSocialRT")
plt.close('all')

sns.lmplot(x='SelfDist',y='fits',data=RmodelfS.data,hue='Social',ci=99.9,hue_order=sorted(np.unique(RmodelfS.data.Social.values)))
plt.savefig("FullRepSocialDistInteractionRT")
plt.close('all')

sns.lmplot(x='FRanking',y='fits',data=RmodelfS.data,hue='Social',ci=99.9,hue_order=sorted(np.unique(RmodelfS.data.Social.values)))
plt.savefig("FullRepSocialRankInteractionRT")
plt.close('all')

sns.barplot(x='Episode',y='fits',data=RmodelfS.data,hue='Social',ci=99.9,hue_order=sorted(np.unique(RmodelfS.data.Social.values)),order=sorted(np.unique(RmodelfS.data.Episode.values)))
plt.savefig("FullRepSocialEpisodeInteractionRT")
plt.close('all')

sns.barplot(x='Episode',y='fits',data=RmodelfS.data,ci=99.9,order=sorted(np.unique(RmodelfS.data.Episode.values)))
plt.savefig("FullRepEpisodeRT")
plt.close('all')

sns.lmplot(x='SelfDist',y='fits',data=RmodelfS.data,hue='Episode',ci=99.9,hue_order=sorted(np.unique(RmodelfS.data.Episode.values)))
plt.savefig("FullRepEpisodeDistInteractionRT")
plt.close('all')

sns.lmplot(x='FRanking',y='fits',data=RmodelfS.data,hue='Episode',ci=99.9,hue_order=sorted(np.unique(RmodelfS.data.Episode.values)))
plt.savefig("FullRepEpisodeRankInteractionRT")
plt.close('all')


plt.figure()
for e in ["Within","Between"]:
 for s in ["Social", "NonSocial"]:
  fpr,tpr,_=roc_curve(modelf.data.performance[np.logical_and(modelf.data.Episode==e,modelf.data.Social==s)], modelf.data.fits[ np.logical_and(modelf.data.Episode==e,modelf.data.Social==s)])
  dpr = pd.DataFrame({"fpr":fpr,"tpr":tpr}).groupby("fpr").mean().reset_index() 
  plt.plot(fpr,tpr,label="{0}:{1}, AUC:{2:0.3f}".format(e,s,roc_auc_score(modelf.data.performance[np.logical_and(modelf.data.Episode==e,modelf.data.Social==s)], modelf.data.fits[ np.logical_and(modelf.data.Episode==e,modelf.data.Social==s)])))
plt.plot([0,1],[0,1],label="Random")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.tight_layout()
plt.savefig("FullRepLMEAUC")

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
plt.savefig("FullRepLMEDistAUC")
