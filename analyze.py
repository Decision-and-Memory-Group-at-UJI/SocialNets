import numpy as np
import pandas as pd
import json
import glob
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

        Soc = list(map(lambda x: "Social" if x else "NonSocial",Soc))
        BWgroup = list(map(lambda x: "Between" if x else "Within",BWgroup))
        PDR += [[performance,Soc,BWgroup,np.repeat(ii,40),np.repeat(k,40)]]
        RT0 = np.array(json.loads(X.retrievalRT[k]))
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
import matplotlib.pyplot as plt
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
import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.formula.api as smf
PDP = [[pd.DataFrame({"performance":PD[i][j][0].astype(int),"Social":PD[i][j][1],"Episode":PD[i][j][2],"Participant":PD[i][j][3],"Run":PD[i][j][4],"Ranking":AllCompAcc[i,j].squeeze().repeat(40)}) for j in range(2)] for i in range(6)]
PDPCat = pd.concat([PDP[i][j] for i in range(6) for j in range(2)])
PDPCat["RunPart"] = PDPCat["Participant"].astype(str)+PDPCat["Run"].astype(str)
fit = smf.mixedlm('performance ~ Social+Episode +Ranking + Episode:Social +Social:Ranking + Episode:Ranking + Episode:Social:Ranking',data=PDPCat,groups=PDPCat['RunPart']).fit(reml=False)
plt.figure(figsize=[10,8])
plt.plot(fit.params.values, fit.params.keys(),"*")
for key,up,low in zip(fit.params.keys(), fit.conf_int(0.05)[0], fit.conf_int(0.05)[1]):
    plt.plot([low,up],[key,key])
plt.xlabel("Coeff Value")
plt.tight_layout()
plt.savefig("LMEFit")
fit.summary().tables[1].to_csv("SummaryMEff.csv")
print(fit.summary(alpha=0.05))
