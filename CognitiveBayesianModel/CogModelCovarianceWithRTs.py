import numpy as np
import pickle
import blackjax
import jax
import jax.numpy as jnp
import jax.scipy.stats as jstats
import os


def PosteriorFit(ChoiceRes,Rank):
    correct = ChoiceRes[:,:,0].astype(int)
    Social = ChoiceRes[:,:,1].astype(int)
    Episode = ChoiceRes[:,:,2].astype(int)
    Person = ChoiceRes[:,:,3].astype(int)
    Confidence = ChoiceRes[:,:,-3].astype(float)
    EpSoc = Social + 2*Episode
    RT = Res[:,:,-2].astype(float)    
    RRTs = [[[] for j in range(4)] for i in range(2)]
    for i in range(Confidence.shape[0]):
        for j in range(2):
            for k in range(4):
                if k < 2:
                    RRTs[j][k].append(RT[i,j][Social[i,j]==k].mean())
                else:
                    RRTs[j][k].append(RT[i,j][Episode[i,j]==k-2].mean())
    RankRT = np.array(RRTs).transpose(2,0,1)/RT.mean(-1,keepdims=True)
    RTM = RT.mean(-1,keepdims=True)

    RConf = [[[] for j in range(4)] for i in range(2)]
    for i in range(Confidence.shape[0]):
        for j in range(2):
            for k in range(4):
                if k < 2:
                    RConf[j][k].append(Confidence[i,j][Social[i,j]==k].mean())
                else:
                    RConf[j][k].append(Confidence[i,j][Episode[i,j]==k-2].mean())

    softplus = lambda x: jnp.log(1+jnp.exp(x))
    invlogit = lambda x: 1/(1+jnp.exp(-x))
    CoVoo = lambda x: invlogit(x)
    logdCoVoo = lambda x: invlogit(x)*(1-invlogit(x))
    CoV = lambda x: jnp.exp(x) # CoV
    logdCoV = lambda x: x # The absolute log derivative of CoV
    CoVul = lambda x,a,b: a + (b-a)*invlogit(x)
    logdCoVul = lambda x,a,b: (b-a)*invlogit(x)*(1-invlogit(x))
    finindices = jnp.array([0,4,8])

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
        return jnp.array([[A,D,G],[B,E,H],[C,F,I]])/detM

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

    def fastinv22(M):
        a,b,c,d = M.ravel()
        detM = a*d - b*c
        return jnp.array([[d,-b],[-c,a]])/detM

    def det22(M):
        a,b,c,d = M.ravel()
        detM = a*d - b*c
        return detM

    def KL(A,B,BP):
        return .5*(jnp.log(det22(B)) - jnp.log(det22(A)) -2 +jnp.diag(BP@A).sum())

    noisepostmuup = (jax.vmap(jax.vmap(jax.vmap(lambda a,b,c: fastinv(a+b)@c,in_axes=[None,-1,None],out_axes=-1))))
    noisepostvarup = (jax.vmap(jax.vmap(jax.vmap(lambda a,b: a+b,in_axes=[None,-1],out_axes=-1))))
    numpostmu = (jax.vmap(jax.vmap(jax.vmap(lambda a,b,c: a+b*c,in_axes=[None,None,-1],out_axes=-1))))
    sigpostmuup = (jax.vmap(jax.vmap(jax.vmap(lambda a,b,c: fastinv(a+b)@c,in_axes=[None,-1,-1],out_axes=-1))))
    sigpostvarup = (jax.vmap(jax.vmap(jax.vmap(lambda a,b: a+b,in_axes=[None,-1],out_axes=-1))))
    finaldiag = (jax.vmap(jax.vmap(jax.vmap(lambda a: fastinv(a).ravel()[finindices,None],in_axes=-1,out_axes=-1))))
    fastdot = (jax.vmap(jax.vmap(jnp.dot)))
    covdotRank = (jax.vmap(jax.vmap(lambda a,b: a@b)))
    firstpostmuup = (jax.vmap(jax.vmap(lambda a,b: fastinv(a)@b)))
    blnumup = (jax.vmap(jax.vmap(lambda a,b: a+b)))
    blmuup = (jax.vmap(jax.vmap(lambda a,b,c: fastinv(a+b)@c)))
    blvarup = (jax.vmap(jax.vmap(lambda a,b: a+b)))
    itemselect = (jax.vmap(jax.vmap(jax.vmap(lambda SS,A,B,C: SS[A,B,C],in_axes=[None,0,0,0]))))
    npitemselect = (jax.vmap(jax.vmap(jax.vmap(lambda SS,A,B: SS[A,B],in_axes=[None,0,0]))))
    RTmed = jnp.median(RT[...,None],-2,keepdims=True)
    def Model( 
            weightPS,weightS,
            tNDPS,tNDS,
            axSocialPS,axSocialS,
            axNonSocialPS,axNonSocialS,
            axActPS,axActS,
            sigBLPS,sigBLS,
            VarWIPM,VarWIS,
            VarBWPM,VarBWS,
            CovWIPS,CovWIS,
            CovBWPS,CovBWS,
            VarCritPS,VarCritS,
            mucritPS,mucritS,
            critPS,critS,
            ):
        logP = []

        oldcritPS = logdCoV(critPS)
        critPS = CoV(critPS)
        logcritPS = (oldcritPS + jstats.gamma.logpdf(critPS,3,scale=5)).sum()
        logP += [logcritPS]

        logcritS = (jstats.norm.logpdf(critS)).sum()
        critS = critS*critPS
        logP += [logcritS]

        oldmucritPS = logdCoV(mucritPS)
        mucritPS = CoV(mucritPS)
        logmucritPS = (oldmucritPS + jstats.gamma.logpdf(mucritPS,3,scale=5)).sum()
        logP += [logmucritPS]

        logmucritS = (jstats.norm.logpdf(mucritS)).sum()
        mucritS = mucritS*mucritPS
        logP += [logmucritS]

        oldVarCritPS = logdCoV(VarCritPS)
        VarCritPS = CoV(VarCritPS)
        logVarCritPS = (oldVarCritPS + jstats.gamma.logpdf(VarCritPS,3,scale=5)).sum()
        logP += [logVarCritPS]
        VarCritPM = VarCritPS[...,0]
        VarCritPS = VarCritPS[...,1]

        origVarCritS = VarCritS
        oldVarCritS = jnp.log(abs(logdCoVul(VarCritS,0,1)))
        VarCritS = CoVul(VarCritS,0,1)
        logVarCritS = (oldVarCritS + jstats.beta.logpdf(VarCritS,VarCritPM,VarCritPS)).sum()
        VarCritS = -VarCritS
        logP += [logVarCritS]

        oldweightPS = logdCoV(weightPS)
        weightPS = CoV(weightPS)
        logweightPS = (oldweightPS + jstats.gamma.logpdf(weightPS,3,scale=5)).sum()
        logP += [logweightPS]

        oldweightS =logdCoV(weightS)
        weightS = CoV(weightS)
        logweightS = (oldweightS + jstats.gamma.logpdf(weightS,3,scale=weightPS)).sum()
        logP += [logweightS]

        oldtNDPS = logdCoV(tNDPS)
        tNDPS = CoV(tNDPS)
        logtNDPS = (oldtNDPS + jstats.gamma.logpdf(tNDPS,3,scale=5)).sum()
        logP += [logtNDPS]
        tNDPM = tNDPS[...,0]
        tNDPS = tNDPS[...,1]

        origtNDS = tNDS
        oldtNDS = jnp.log(abs(logdCoVul(tNDS,0,1)))
        tNDS = CoVul(tNDS,0,1)
        logtNDS = (oldtNDS + jstats.beta.logpdf(tNDS,tNDPM,tNDPS)).sum()
        logP += [logtNDS]

        tT = jax.vmap(jax.vmap(jax.vmap(lambda a,b: a[b],in_axes=[None,-1])))(tNDS,Social)#npitemselect(tNDS,Social,Episode)
        wT = weightS
        TD = RT[...,None] - tT*RTmed

        oldaxSocialPS = logdCoV(axSocialPS)
        axSocialPS = CoV(axSocialPS)
        logaxSocialPS = (oldaxSocialPS + jstats.gamma.logpdf(axSocialPS,1,scale=5)).sum()
        logP += [logaxSocialPS]

        oldaxSocialS =logdCoV(axSocialS)
        axSocialS = CoV(axSocialS)
        logaxSocialS = (oldaxSocialS + jstats.gamma.logpdf(axSocialS,1,scale=axSocialPS)).sum()
        logP += [logaxSocialS]

        oldaxNonSocialPS = logdCoV(axNonSocialPS)
        axNonSocialPS = CoV(axNonSocialPS)
        logaxNonSocialPS = (oldaxNonSocialPS + jstats.gamma.logpdf(axNonSocialPS,1,scale=5)).sum()
        logP += [logaxNonSocialPS]

        oldaxNonSocialS =logdCoV(axNonSocialS)
        axNonSocialS = CoV(axNonSocialS)
        logaxNonSocialS = (oldaxNonSocialS + jstats.gamma.logpdf(axNonSocialS,1,scale=axNonSocialPS)).sum()
        logP += [logaxNonSocialS]

        oldaxActPS = logdCoV(axActPS)
        axActPS = CoV(axActPS)
        logaxActPS = (oldaxActPS + jstats.gamma.logpdf(axActPS,1,scale=5)).sum()
        logP += [logaxActPS]

        oldaxActS =logdCoV(axActS)
        axActS = CoV(axActS)
        logaxActS = (oldaxActS + jstats.gamma.logpdf(axActS,1,scale=axActPS)).sum()
        logP += [logaxActS]

        directionS = jnp.concatenate([axSocialS,axNonSocialS,axActS],-1)[...,None]
        directionS = directionS/(directionS.sum(-2,keepdims=True))

        # WI Corr
        oldCovWIPS = logdCoV(CovWIPS)
        CovWIPS = CoV(CovWIPS)
        logCovWIPS = (oldCovWIPS + jstats.gamma.logpdf(CovWIPS,1,scale=5)).sum()
        logP += [logCovWIPS]
        CovWIPM = CovWIPS[...,0]
        CovWIPS = CovWIPS[...,1]

        origCovWIS = CovWIS
        oldCovWIS = jnp.log(abs(logdCoVul(CovWIS,0,1)))
        CovWIS = CoVul(CovWIS,0,1)
        logCovWIS = (oldCovWIS + jstats.beta.logpdf(CovWIS,CovWIPM,CovWIPS)).sum()
        CovWIS = CovWIS*2-1
        logP += [logCovWIS]

        # BW Corr
        oldCovBWPS = logdCoV(CovBWPS)
        CovBWPS = CoV(CovBWPS)
        logCovBWPS = (oldCovBWPS + jstats.gamma.logpdf(CovBWPS,1,scale=5)).sum()
        logP += [logCovBWPS]
        CovBWPM = CovBWPS[...,0]
        CovBWPS = CovBWPS[...,1]

        origCovBWS = CovBWS
        oldCovBWS = jnp.log(abs(logdCoVul(CovBWS,0,1)))
        CovBWS = CoVul(CovBWS,0,1)
        logCovBWS = (oldCovBWS+jstats.beta.logpdf(CovBWS,CovBWPM,CovBWPS)).sum()
        CovBWS = CovBWS*2-1
        logP += [logCovBWS]

        # Var WI
        oldVarWIPM = logdCoV(VarWIPM)
        VarWIPM = CoV(VarWIPM)
        logVarWIPM = (oldVarWIPM + jstats.gamma.logpdf(VarWIPM,1,scale=5)).sum()
        logP += [logVarWIPM]

        oldVarWIS =logdCoV(VarWIS)
        VarWIS = CoV(VarWIS)
        logVarWIS = (oldVarWIS + jstats.gamma.logpdf(VarWIS,1,scale=VarWIPM)).sum()
        logP += [logVarWIS]

        # Var BW
        oldVarBWPM = logdCoV(VarBWPM)
        VarBWPM = CoV(VarBWPM)
        logVarBWPM = (oldVarBWPM + jstats.gamma.logpdf(VarBWPM,1,scale=5)).sum()
        logP += [logVarBWPM]

        oldVarBWS =logdCoV(VarBWS)
        VarBWS = CoV(VarBWS)
        logVarBWS = (oldVarBWS + jstats.gamma.logpdf(VarBWS,1,scale=VarBWPM)).sum()
        logP += [logVarBWS]

        # BL Dist
        oldsigBLPS = logdCoV(sigBLPS)
        sigBLPS = CoV(sigBLPS)
        logsigBLPS = (oldsigBLPS + jstats.gamma.logpdf(sigBLPS,1,scale=5)).sum()
        logP += [logsigBLPS]

        oldsigBLS =logdCoV(sigBLS)
        sigBLS = CoV(sigBLS)
        logsigBLS = (oldsigBLS + jstats.gamma.logpdf(sigBLS,1,scale=sigBLPS)).sum()
        logP += [logsigBLS]
        sigBLSW = sigBLS[...,0]
        sigBLSB = sigBLS[...,1]

        sigSN =  jax.vmap(jax.vmap(jax.vmap(makeCov,in_axes=[-1,None],out_axes=-1)))(VarWIS,CovWIS)
        sigESN = jax.vmap(jax.vmap(jax.vmap(makeCov,in_axes=[-1,None],out_axes=-1)))(VarBWS,CovBWS)

        EWIS = jax.vmap(jax.vmap(fastinv))(sigSN.mean(-1))
        SNSWIS = EWIS[...,:2,:2]
        SAWIS = EWIS[...,[0,0,2,2],[0,2,0,2]].reshape(*EWIS.shape[:-2],2,2)
        NSAWIS = EWIS[...,[2,2,1,1],[2,1,2,1]].reshape(*EWIS.shape[:-2],2,2)
        PSNSWIS = jax.vmap(jax.vmap(fastinv22))(SNSWIS)
        PSAWIS =  jax.vmap(jax.vmap(fastinv22))(SAWIS)
        PNSAWIS = jax.vmap(jax.vmap(fastinv22))(NSAWIS)

        EBWS = jax.vmap(jax.vmap(fastinv))(sigESN.mean(-1))
        SNSBWS = EBWS[...,:2,:2]
        SABWS = EBWS[...,[0,0,2,2],[0,2,0,2]].reshape(*EBWS.shape[:-2],2,2)
        NSABWS = EBWS[...,[2,2,1,1],[2,1,2,1]].reshape(*EBWS.shape[:-2],2,2)
        PSNSBWS = jax.vmap(jax.vmap(fastinv22))(SNSBWS)
        PSABWS =  jax.vmap(jax.vmap(fastinv22))(SABWS)
        PNSABWS = jax.vmap(jax.vmap(fastinv22))(NSABWS)

        KLSAWI =  jnp.log(jax.vmap(jax.vmap(KL))(NSAWIS,SNSWIS,PSNSWIS))
        KLNSAWI = jnp.log(jax.vmap(jax.vmap(KL))(SAWIS ,SNSWIS,PSNSWIS))
        KLSABW =  jnp.log(jax.vmap(jax.vmap(KL))(NSABWS,SNSBWS,PSNSBWS))
        KLNSABW = jnp.log(jax.vmap(jax.vmap(KL))(SABWS ,SNSBWS,PSNSBWS))

        logKL = jstats.norm.logpdf((KLSAWI - KLNSAWI).mean((0,1)),0,4) + jstats.norm.logpdf((KLSABW - KLNSABW).mean((0,1)),0,4)
        logP += [logKL.sum()]
        Ranks = Rank[...,[1],None]*directionS

        SpostMu = 1/(sigBLSW+1)*(-sigBLSW*Ranks)
        SpostVar = sigBLSW+1
        num = -jax.vmap(covdotRank,in_axes=[-1,None],out_axes=-1)(sigSN,Ranks)
        num = (SpostMu*SpostVar)[...,None] + num
        SpostMu = jax.vmap(firstpostmuup,in_axes=[-1,-1],out_axes=-1)(sigSN+(SpostVar*jnp.eye(3))[...,None],num)
        SpostVar = sigSN+(SpostVar*jnp.eye(3))[...,None]

        sigBLSB = sigBLSB*jnp.eye(3)
        num = covdotRank(sigBLSB,Ranks)
        NpostMu = jax.vmap(jax.vmap(jax.vmap(lambda a,b,c: fastinv(a+b)@c,in_axes=[None,-1,None],out_axes=-1)))(sigBLSB,SpostVar,num)
        NpostVar = noisepostvarup(sigBLSB,SpostVar)
        num = jax.vmap(covdotRank,in_axes=[-1,None],out_axes=-1)(sigESN,Ranks)
        num = jax.vmap(jax.vmap(jax.vmap(lambda a,b,c: a@b + c,in_axes=[-1,-1,-1],out_axes=-1)))(NpostVar,NpostMu,num)
        NpostMu = jax.vmap(jax.vmap(jax.vmap(lambda a,b,c: fastinv(a+b)@c,in_axes=[-1,-1,-1],out_axes=-1)))(sigESN,NpostVar,num)
        NpostVar = NpostVar + sigESN

        NpostVar = finaldiag(NpostVar)
        SpostVar = finaldiag(SpostVar)
        NpostMu = jnp.concatenate((jnp.zeros_like(NpostMu),NpostMu),-2)
        NpostVar = jnp.concatenate((SpostVar,NpostVar),-2)
        postMu = (SpostMu - NpostMu)
        postVar = jnp.sqrt((SpostVar+NpostVar))

        # Cumulative distribution to get the hit-rate for a Social or NonSocial stimuli with attributes W/I or B/W With activity cue
        PcriterionS = jstats.norm.cdf( (mucritS[...,None,None]-postMu[...,:2,:,:])/postVar[...,:2,:,:])
        APcriterionS = jstats.norm.cdf((mucritS[...,None,None]-postMu[...,[2],:,:])/postVar[...,[2],:,:])
        PcriterionS = PcriterionS*APcriterionS

        # partial interactions between stimuli at recall
        corrs = jax.vmap(jax.vmap(jax.vmap(lambda a,b: (a*b),in_axes=[-2,None])))(TD,wT).squeeze()
        logcorrs = jstats.norm.logpdf(corrs.mean((0,1,-2))).sum()
        logP += [logcorrs]
        corrs = CoVul(corrs,-1,1)

        biasL = jax.vmap(jax.vmap(jax.vmap(lambda a,b: makeCov2(a,b),in_axes=[None,-2],out_axes=-1)))(VarCritS.repeat(3,axis=-1),corrs) 
        # Normalization of weights (partial interactions)
        biasL = biasL/jnp.sqrt((biasL**2).sum(-2,keepdims=True))

        bias = jax.vmap(jax.vmap(jax.vmap(lambda z,L: L@z.squeeze(),in_axes=[None,-1],out_axes=-1)))(critS,biasL).squeeze() 
        Sbias = jax.vmap(jax.vmap(jax.vmap(lambda a,b: a[b],in_axes=-1)))(bias,Social)
        Abias = bias[...,-1,:]
        postMuT = itemselect(postMu,Social,Episode,Person)
        postVarT = itemselect(postVar,Social,Episode,Person)
        ApostMuT =  npitemselect(postMu[...,2,:,:],Episode,Person)
        ApostVarT = npitemselect(postVar[...,2,:,:],Episode,Person)

        corrP= jstats.norm.cdf( (mucritS + Sbias - postMuT)/(postVarT))
        AcorrP= jstats.norm.cdf((mucritS + Abias - ApostMuT)/(ApostVarT))
        corrP = corrP*AcorrP

        # bernoulli describes choice observation at a trial
        logchoiceS = jstats.bernoulli.logpmf(correct,corrP).sum()
        logP += [logchoiceS]

        return [corrP,PcriterionS,postMu,postVar,SpostMu,jnp.sqrt(SpostVar),NpostMu,jnp.sqrt(NpostVar)],(jnp.array(logP)).sum()

	        
    def inference_loop(kernel, num_samples, rng_key, initial_state,chainNo):
        def one_step(state, rng_key):
            rng_key,sampnum = rng_key
            jax.lax.cond(sampnum % 100 == 0,lambda s: jax.debug.print("Samp Num: {}, {}\r" ,chainNo,s), lambda s: None,sampnum)
            state, _ = kernel(rng_key, state)
            return state, state
    
        keys = jax.random.split(rng_key, num_samples)
        _, states = jax.lax.scan(jax.jit(one_step), initial_state, (keys,jnp.arange(len(keys))))
    
        return jax.tree_map(lambda x: x[::5],states)
    key = jax.random.PRNGKey(0)
    nchains = 8
    key = jax.random.split(key,nchains)
    
    def Chain(chain,key):
        keys = jax.random.split(key,30)
        keys = keys[1:]
    
        initial_position = {
            # Recall partial interaction weights
            "weightPS":(jax.random.normal(keys[2],shape=(1,1,1,6,))*0.1+0),
            "weightS":(jax.random.normal(keys[3],shape=(correct.shape[0],2,1,6,))*0.1+0),
            # Marginal recall variance
            "VarCritPS":(jax.random.normal(keys[22],shape=(1,1,1,2,))*0.1+0),
            "VarCritS":(jax.random.normal(keys[21],shape=(correct.shape[0],2,1,))*0.1+0),
            # Baseline recall bias
            "mucritPS":(jax.random.normal(keys[24],shape=(1,1,1,))*0.1+0),
            "mucritS":(jax.random.normal(keys[25],shape=(correct.shape[0],2,1,))*0.1+0),
            # Biases for particular stimuli at recall
            "critPS":(jax.random.normal(keys[24],shape=(1,1,3,))*0.1+0),
            "critS":(jax.random.normal(keys[25],shape=(correct.shape[0],2,3,))*0.1+0),
            # Non decision time
            "tNDPS":(jax.random.normal(keys[4],shape=(1,1,2,1,2,))*0.1+0),
            "tNDS":(jax.random.normal(keys[5],shape=(correct.shape[0],2,2,1,))*0.1+0),
            # Direction of encoding
            "axSocialPS":(jax.random.normal(keys[6],shape=(1,1,1,))*0.1+0),
            "axSocialS":(jax.random.normal(keys[7],shape=(1,2,1,))*0.1+0),
            "axNonSocialPS":(jax.random.normal(keys[8],shape=(1,1,1,))*0.1+0),
            "axNonSocialS":(jax.random.normal(keys[9],shape=(1,2,1,))*0.1+0),
            "axActPS":(jax.random.normal(keys[10],shape=(1,1,1,))*0.1+0),
            "axActS":(jax.random.normal(keys[11],shape=(1,2,1,))*0.1+0),
            # Baseline encoding
            "sigBLPS":(jax.random.normal(keys[12],shape=(1,1,1,1,2,))*0.1+0),
            "sigBLS":(jax.random.normal(keys[13],shape=(correct.shape[0],2,1,1,2,))*0.1+0),
            # Signal interactions between encoded stimuli
            "VarWIPM":(jax.random.normal(keys[14],shape=(1,1,3,5,))*0.1+0),
            "VarWIS":(jax.random.normal(keys[15],shape=(correct.shape[0],2,3,5,))*0.1+0),
            "CovWIPS":(jax.random.normal(keys[16],shape=(1,1,3,2,))*0.1+0),
            "CovWIS":(jax.random.normal(keys[17],shape=(correct.shape[0],2,3,))*0.1+0),
            # Noise interactions between encoded stimuli
            "VarBWPM":(jax.random.normal(keys[18],shape=(1,1,3,5,))*0.1+0),
            "VarBWS":(jax.random.normal(keys[19],shape=(correct.shape[0],2,3,5,))*0.1+0),
            "CovBWPS":(jax.random.normal(keys[20],shape=(1,1,3,2,))*0.1+0),
            "CovBWS":(jax.random.normal(keys[21],shape=(correct.shape[0],2,3,))*0.1+0),
        }
        logdensity = lambda x: Model(**x)[1]
        posteriorPoints = jax.vmap(lambda x: Model(**x)[0])
        keys = jax.random.split(keys[-1],2)[-1]
        print("Starting Warmup")
        warmup = blackjax.window_adaptation(blackjax.nuts,logdensity,target_acceptance_rate=0.8,progress_bar=True,initial_step_size=1,)
        AdaptRes,_ = warmup.run(keys,initial_position,num_steps=1000)
        kernel = jax.jit(blackjax.nuts(logdensity,AdaptRes.parameters['step_size'],AdaptRes.parameters['inverse_mass_matrix']).step)
        print("Starting Loop")
        keys = jax.random.split(keys,2)[-1]
        states = inference_loop(kernel,5000,keys,AdaptRes.state,chain)
        [posteriorPred,PImp,postMu,postVar,SpostMu,SpostVar,NpostMu,NpostVar] = posteriorPoints(states.position)
        # Post processing transformations
        states.position['posteriorPredictive'] = posteriorPred
        states.position['PosteriorProb'] = PImp 
        states.position['postMu'] =postMu 
        states.position['postVar'] = postVar 
        states.position['NpostMu'] =NpostMu 
        states.position['NpostVar'] = NpostVar 
        states.position['SpostMu'] =SpostMu 
        states.position['SpostVar'] = SpostVar 
        jax.debug.print("Finish Chain {}",chain)
        return states
    states = jax.vmap(Chain)(jnp.arange(nchains),key)
    print("Saving!")

    for key in states.position.keys():
        states.position[key] = states.position[key].squeeze()
    with open('Posterior_EpStrAltActCovDirRTBDP.pkl'.format(), 'wb') as f:
        pickle.dump(states, f)
    
# Subjects x Runs x Attribute
Res = np.concatenate([np.load("Perdistrep1Collect.npy"),np.load("Perdistrep2Collect.npy")[:,::-1]],0)
print(Res.shape)
Ranks = np.concatenate([np.load("PerRankingrep1.npy"),np.load("PerRankingrep2.npy")[:,::-1]],0).transpose(0,2,1)
PosteriorFit(Res,Ranks)
