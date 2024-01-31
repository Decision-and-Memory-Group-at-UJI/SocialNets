import numpy as np
import pickle
import blackjax
import jax
import jax.numpy as jnp
import jax.scipy.stats as jstats
import os


def PosteriorFit(ChoiceRes,Ranks):
    correct = ChoiceRes[:,:,0].astype(int)
    Social = ChoiceRes[:,:,1].astype(int)
    Episode = ChoiceRes[:,:,2].astype(int)
    Person = ChoiceRes[:,:,3].astype(int)
    Confidence = ChoiceRes[:,:,-3].astype(float)
    RConf = [[[] for j in range(2)] for i in range(2)]
    for i in range(115):
        for j in range(2):
            for k in range(2):
                RConf[j][k].append(Confidence[i,j][Social[i,j]==k].mean())
    RankConf = jnp.array(RConf).transpose(2,0,1)
    confcorr = jax.vmap(jax.vmap(lambda a,b:jnp.corrcoef(a.ravel(),b.ravel())[0,1],in_axes=[None,-1]),in_axes=[-1,None])
    invlogit = lambda x: 1/(1+jnp.exp(-x))
    CoVoo = lambda x: invlogit(x)
    logdCoVoo = lambda x: invlogit(x)*(1-invlogit(x))
    CoV = lambda x: jnp.exp(x) # CoV
    logdCoV = lambda x: x # The absolute log derivative of CoV
    def Model( 
            criterionPM,criterionPS,criterionS,
            sigPM,sigPS,sigS,
            ):
        logP = []

        # The criterion K 
        logcriterionPM = (jstats.norm.logpdf(criterionPM,1,scale=3)).sum()
        logP += [logcriterionPM]

        oldcriterionPS =logdCoV(criterionPS)
        criterionPS = CoV(criterionPS)
        logcriterionPS = (oldcriterionPS+jstats.gamma.logpdf(criterionPS,1,scale=10)).sum()
        logP += [logcriterionPS]

        logcriterionS = (jstats.norm.logpdf(criterionS)).sum()
        criterionS = criterionPM + criterionS/criterionPS
        logP += [logcriterionS]

        # Uncertainty on role performance given social or nonsocial stimuli
        oldsigPM = logdCoV(sigPM)
        sigPM = CoV(sigPM)
        logsigPM = (oldsigPM + jstats.gamma.logpdf(sigPM,1,scale=1)).sum()
        logP += [logsigPM]

        oldsigPS =logdCoV(sigPS)
        sigPS = CoV(sigPS)
        logsigPS = (oldsigPS+jstats.gamma.logpdf(sigPS,1,scale=1)).sum()
        logP += [logsigPS]

        oldsigS =logdCoV(sigS)
        sigS = CoV(sigS)
        logsigS = (oldsigS + jstats.gamma.logpdf(sigS,sigPM,scale=sigPS)).sum()
        logP += [logsigS]

        # The prior distribution is a standard normal located at 1
        postMu = 1/(sigS + 1)*(1-sigS*Ranks[...,1,None,None,None])
        postVar = jnp.sqrt((sigS + 1)**(-1))

        # For Savage Dickey's ratio BF on explained variance
        mucorr = confcorr(postMu.squeeze(),RankConf)**2
        varcorr = confcorr(postVar.squeeze(),RankConf)**2
        sigcorr = confcorr(jnp.sqrt(1/sigS).squeeze(),RankConf)**2
        logmucorr = jstats.norm.logpdf(mucorr[...,  0,:]-mucorr[..., 1,:],0,0.01).sum()
        logvarcorr = jstats.norm.logpdf(varcorr[...,0,:]-varcorr[...,1,:],0,0.01).sum()
        logsigcorr = jstats.norm.logpdf(sigcorr[...,0,:]-sigcorr[...,1,:],0,0.01).sum()
        logP += [logmucorr,logvarcorr,logsigcorr]

        # Cumulative distribution to get the hit-rate for a Social or NonSocial stimuli with attributes W/I or B/W With activity cue
        PcriterionS = jstats.norm.cdf((criterionS-postMu)/postVar)

        # For Savage Dickey's ratio BF on social vs nonsocial stimuli
        logSvNS = jstats.norm.logpdf((PcriterionS[...,0,:,:] - PcriterionS[...,1,:,:]).mean((0,1,-1)),0,0.05).sum()
        logP += [logSvNS]

        # Get what stimuli-attribute pairings were presented at each trial
        corrP = jax.vmap(jax.vmap(jax.vmap(lambda SS,A,B,C: SS[A,B,C],in_axes=[None,0,0,0])))(PcriterionS,Social,Episode,Person)
        postMuT = jax.vmap(jax.vmap(jax.vmap(lambda SS,A,B,C: SS[A,B,C],in_axes=[None,0,0,0])))(postMu,Social,Episode,Person)
        postVarT = jax.vmap(jax.vmap(jax.vmap(lambda SS,A,B,C: SS[A,B,C],in_axes=[None,0,0,0])))(postVar,Social,Episode,Person)

        # bernoulli describes choice observation at a trial
        logchoiceS = jstats.bernoulli.logpmf(correct,corrP).sum()
        logP += [logchoiceS]
        return [corrP,PcriterionS,postMu,postVar,postMuT,postVarT],(jnp.array(logP)).sum()

	        
    def inference_loop(kernel, num_samples, rng_key, initial_state,chainNo):
        def one_step(state, rng_key):
            rng_key,sampnum = rng_key
            jax.lax.cond(sampnum % 100 == 0,lambda s: jax.debug.print("Samp Num: {}, {}\r" ,chainNo,s), lambda s: None,sampnum)
            state, _ = kernel(rng_key, state)
            return state, state
    
        keys = jax.random.split(rng_key, num_samples)
        _, states = jax.lax.scan(jax.jit(one_step), initial_state, (keys,jnp.arange(len(keys))))
    
        return states
    key = jax.random.PRNGKey(0)
    nchains = 8
    key = jax.random.split(key,nchains)
    
    def Chain(chain,key):
        keys = jax.random.split(key,20)
        keys = keys[1:]
    
        initial_position = {
            "criterionPM":(jax.random.normal(keys[0],shape=(1,1,1,2,5,))*0.1+0),
            "criterionPS":(jax.random.normal(keys[1],shape=(1,1,1,2,5,))*0.1+0),
            "criterionS":(jax.random.normal(keys[2],shape=(correct.shape[0],2,1,2,5,))*0.1+0),
            "sigPM":(jax.random.normal(keys[3],shape=(1,1,2,1,1,))*0.1+0),
            "sigPS":(jax.random.normal(keys[4],shape=(1,1,2,1,1,))*0.1+0),
            "sigS":(jax.random.normal(keys[5],shape=(correct.shape[0],2,2,1,1,))*0.1+0),
        }
        logdensity = lambda x: Model(**x)[1]
        posteriorPoints = jax.vmap(lambda x: Model(**x)[0])
        keys = jax.random.split(keys[-1],2)[-1]
        print("Starting Warmup")
        warmup = blackjax.window_adaptation(blackjax.nuts,logdensity,target_acceptance_rate=0.90,progress_bar=True,initial_step_size=1,)
        AdaptRes,_ = warmup.run(keys,initial_position,num_steps=1000)
        kernel = jax.jit(blackjax.nuts(logdensity,AdaptRes.parameters['step_size'],AdaptRes.parameters['inverse_mass_matrix']).step)
        print("Starting Loop")
        keys = jax.random.split(keys,2)[-1]
        states = inference_loop(kernel,5000,keys,AdaptRes.state,chain)
        [posteriorPred,PImp,postMu,postVar,postMuT,postVarT] = posteriorPoints(states.position)
        # Post processing transformations
        states.position['posteriorPredictive'] = posteriorPred
        states.position['PosteriorProb'] = PImp 
        states.position['postMu'] =postMu 
        states.position['postVar'] = postVar 
        states.position['postMuT'] =postMuT
        states.position['postVarT'] = postVarT 
        states.position['criterionS'] = states.position['criterionPM'] + states.position['criterionS']*CoV(states.position['criterionPS'])
        states.position['sigS'] = jnp.sqrt(1/CoV(states.position['sigS']))
        states.position['sigPM'] = jnp.sqrt(1/CoV(states.position['sigPM']))
        jax.debug.print("Finish Chain {}",chain)
        return states
    states = jax.vmap(Chain)(jnp.arange(nchains),key)
    print("Saving!")
    for key in states.position.keys():
        states.position[key] = states.position[key].squeeze()
    with open('Posterior_EpStrBDP.pkl'.format(), 'wb') as f:
        pickle.dump(states, f)
    
# Subjects x Runs x Attribute
Res = np.concatenate([np.load("distrep1Collect.npy"),np.load("distrep2Collect.npy")[:,::-1]],0)
Ranks = np.concatenate([np.load("Rankingrep1.npy"),np.load("Rankingrep2.npy")[:,::-1]],0).transpose(0,2,1)
PosteriorFit(Res,Ranks)
