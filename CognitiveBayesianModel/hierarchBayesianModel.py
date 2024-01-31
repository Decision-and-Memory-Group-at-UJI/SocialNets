import numpy as np
import pickle
import blackjax
import jax
import jax.numpy as jnp
import jax.scipy.stats as jstats
import os


def PosteriorFit(ChoiceRes):
    correct = ChoiceRes[:,:,0].astype(int)
    Social = ChoiceRes[:,:,1].astype(int)
    Episode = ChoiceRes[:,:,2].astype(int)
    Cue = ChoiceRes[:,:,3].astype(int)
    invlogit = lambda x: 1/(1+jnp.exp(-x))
    CoVul = lambda x,a,b: a + (b-a)*invlogit(x)
    logdCoVul = lambda x,a,b: (b-a)*invlogit(x)*(1-invlogit(x))
    logdsoftplus = lambda x: sigmoid(x)
    CoV = lambda x: jnp.exp(x) # CoV
    logdCoV = lambda x: x 
    def Model( 
            selfEpSocPM,selfEpSocPS,selfEpSocS,
            ):
        logP = []

        # We made the experiment to ensure that the population of participants will surely score above chance in memory recall
        # Thus, we keep the parameter strictly positive (logistic(theta) > 0.5 for theta > 0). Logistic(1) ~ 73% 
        dselfEpSocPM = logdCoV(selfEpSocPM)
        selfEpSocPM = CoV(selfEpSocPM)
        logselfEpSocPM = (dselfEpSocPM + jstats.gamma.logpdf(selfEpSocPM,1,scale=1)).sum()
        logP += [logselfEpSocPM]

        # We don't want to make any strong a priori hypothesis on the variation of population performances, so we keep a large
        # width that on average the probability the score has a 95% conf interval between (logistic(1-1.96*2) and logistic(1+1.96*2)
        # That would mean (5%, 99%)
        oldselfEpSocPS =logdCoV(selfEpSocPS)
        selfEpSocPS = CoV(selfEpSocPS)
        logselfEpSocPS = (oldselfEpSocPS+jstats.gamma.logpdf(selfEpSocPS,2,scale=1)).sum()
        logP += [logselfEpSocPS]

        # This is the probability that a participant has the sampled logistic parameter
        logselfEpSocS = (jstats.norm.logpdf(selfEpSocS,selfEpSocPM,selfEpSocPS)).sum()
        logP += [logselfEpSocS]

        # Logistic function to map attribute and person effects to bernoulli probability parameter for correct choice
        corrP = jax.vmap(jax.vmap(lambda SS,A,B,C: SS[A,B,C]))(selfEpSocS,Social,Episode,Cue)
        corrP = CoVul(corrP,0,1)
        
        # bernoulli describes choice behavior, which is conditional on the logistic parameter for the given cue, 
        # whether it is a social or nonsocial discrimination task, and whether it's between or within person memory recall
        logchoiceS = jstats.bernoulli.logpmf(correct,corrP).sum()
        logP += [logchoiceS]
        return corrP,(jnp.array(logP)).sum()

	        
    def inference_loop(kernel, num_samples, rng_key, initial_state,chainNo):
        def one_step(state, rng_key):
            rng_key,sampnum = rng_key
            jax.lax.cond(sampnum % 1000 == 0,lambda s: jax.debug.print("Samp Num: {}, {}\r" ,chainNo,s), lambda s: None,sampnum)
            state, _ = kernel(rng_key, state)
            return state, state
    
        keys = jax.random.split(rng_key, num_samples)
        _, states = jax.lax.scan(jax.jit(one_step), initial_state, (keys,jnp.arange(len(keys))))
    
        return states
    key = jax.random.PRNGKey(0)
    nchains = 8
    key = jax.random.split(key,nchains)
    
    def Chain(chain,key):
        keys = jax.random.split(key,10)
        keys = keys[1:]
    
        initial_position = {
            # Logistic parameter group mean
            "selfEpSocPM":(jax.random.normal(keys[0],shape=(1,2,2,2,5,))*0.1+0),
            # Logistic parameter group standard deviation
            "selfEpSocPS":(jax.random.normal(keys[1],shape=(1,2,2,2,5,))*0.1+0),
            # Logistic parameter participant level RV 
            "selfEpSocS":(jax.random.normal(keys[2],shape=(correct.shape[0],2,2,2,5))*0.1+0),
            # Shape : Participant x Run x Social/NonSocial x Within or Between Episode Stimuli x Activity
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
        # Run inference chain
        states = inference_loop(kernel,1000,keys,AdaptRes.state,chain)
        # Get posterior predictive distribution
        posteriorPred = posteriorPoints(states.position)
        states.position['posteriorPredictive'] = posteriorPred
        jax.debug.print("Finish Chain {}",chain)
        return states
    states = jax.vmap(Chain)(jnp.arange(nchains),key)
    print("Saving!")

    # Save Population parameters in transformed space
    states.position['selfEpSocPM'] = CoV(states.position['selfEpSocPM'])#,0,10)
    states.position['selfEpSocPS'] = CoV(states.position['selfEpSocPS'])#,0,10)

    for key in states.position.keys():
        states.position[key] = states.position[key].squeeze()
    with open('Posterior_FullJoint.pkl'.format(), 'wb') as f:
        pickle.dump(states, f)
    
# Subjects x Runs x Attributes
Res = np.concatenate([np.load("distrep1Collect.npy"),np.load("distrep2Collect.npy")[:,::-1]],0)
PosteriorFit(Res)
