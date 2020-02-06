'''
Generated by pydream_it
PyDREAM run script for necro.py 
'''
from pydream.core import run_dream
from pysb.simulator import ScipyOdeSimulator
import numpy as np
from pydream.parameters import SampledParam
from pydream.convergence import Gelman_Rubin
from scipy.stats import norm,uniform, halfnorm
from necro_uncal_new import model
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import random 
#random.seed(0)


par_priors = np.load('optimizer_best_100_100_9_20_necromulti_pso0.npy')
# DREAM Settings
# Number of chains - should be at least 3.
nchains = 5
# Number of iterations
niterations = 200000


obs_names = ['MLKLa_obs']

# Defining a few helper functions to use
def normalize(trajectories):
    """even though this is not really needed, if the data is already between 1 and 0!"""
    """Rescale a matrix of model trajectories to 0-1"""
    ymin = trajectories.min(0)
    ymax = trajectories.max(0)
    return (trajectories - ymin) / (ymax - ymin)

t = np.array([0, 30, 90, 270, 480, 600, 720, 840, 960])
y100_1 = np.array([0, 0.00885691708746097,0.0161886154261265,0.0373005242261882])
y100_2 = np.array([0.2798939020159581,0.510, .7797294067, 0.95,1])

# x10 = np.array([.5, 1.5, 4.5, 8, 10, 12, 14, 16])
y10_1 = np.array([0, 0.0106013664572332,0.00519576571714913,0.02967443048221])
y10_2 = np.array([0.050022163974868,0.108128107774737, 0.25,0.56055140114867, 0.77])

solver = ScipyOdeSimulator(model, tspan=t, compiler='cython') #, rtol=1e-6, # rtol : float or sequence relative tolerance for solution
                            #atol=1e-6) #atol : float or sequence absolute tolerance for solution

rate_params = model.parameters_rules() # these are only the parameters involved in the rules
param_values = np.array([p.value for p in model.parameters]) # these are all the parameters
rate_mask = np.array([p in rate_params for p in model.parameters])  # this picks the element of intersection

y100_data1 = halfnorm(loc=y100_1, scale = 0.10)
y100_data2 = norm(loc=y100_2, scale = 0.10)
y10_data1 = halfnorm(loc = y10_1, scale = 0.10)
y10_data2 = norm(loc = y10_2, scale = 0.10)

# plt.figure()
# plt.hist(y100_data1)
# plt.show()
# quit()
#
# print(y100_data1)
# quit()
def likelihood(position):
    params_tmp = np.copy(position)  # here you pass the parameter vector; the point of making a copy of it is in order not to modify it
    param_values[rate_mask] = 10 ** params_tmp  # see comment above *

    params_10 = np.copy(param_values)
    params_10[0] = 233
    pars = [param_values, params_10]
    result = solver.run(tspan=t, param_values=pars)

    ysim_norm100 = normalize(result.observables[0]['MLKLa_obs'])
    # print('ysimnorm 100')
    # print(ysim_norm100)

    ysim_norm10 = normalize(result.observables[1]['MLKLa_obs'])
    # print('ysimnorm 10')
    # print(ysim_norm10)
    # print(ysim_norm100)
    # quit()
    # result = solver.run(param_values=param_values)
    # ysim_norm = normalize(result.observables['MLKLa_obs'])
    # error = np.sum(((y100 - ysim_norm) ** 2))

    logp_y1001 = np.sum(y100_data1.logpdf(ysim_norm100[0:4]))
    logp_y1002 = np.sum(y100_data2.logpdf(ysim_norm100[4:]))
    logp_y101 = np.sum(y10_data1.logpdf(ysim_norm10[0:4]))
    logp_y102 = np.sum(y10_data2.logpdf(ysim_norm10[4:]))

    # print('y1001')
    # print(logp_y1001)
    # print('y1002')
    # print(logp_y1002)
    # print('y101')
    # print(logp_y101)
    # print('y102')
    # print(logp_y102)

    logp_total = logp_y1001 + logp_y1002 + logp_y101 + logp_y102

    if np.isnan(logp_total):
        logp_total = -np.inf

    # e1 = np.sum(((y100 - ysim_norm100) ** 2))
    # e2 = np.sum(((y10 - ysim_norm10) ** 2))
    # error = e1 + e2

    return logp_total


#PREVIOUS CODE

# x100 = np.array([30, 90, 270, 480, 600, 720, 840, 960])
# y100 = np.array([0.00885691708746097,0.0161886154261265,0.0373005242261882,0.2798939020159581,0.510, .7797294067, 0.95,1])
#
# # x10 = np.array([.5, 1.5, 4.5, 8, 10, 12, 14, 16])
# y10 = np.array([0.0106013664572332,0.00519576571714913,0.02967443048221,0.050022163974868,0.108128107774737, 0.25,0.56055140114867, 0.77])
# solver = ScipyOdeSimulator(model, tspan=x100) #, rtol=1e-6, # rtol : float or sequence relative tolerance for solution
#                             #atol=1e-6) #atol : float or sequence absolute tolerance for solution
#
# rate_params = model.parameters_rules() # these are only the parameters involved in the rules
# param_values = np.array([p.value for p in model.parameters]) # these are all the parameters
# rate_mask = np.array([p in rate_params for p in model.parameters])  # this picks the element of intersection
#
# y100_data = norm(loc=y100, scale = 0.05)
# y10_data = norm(loc = y10, scale = 0.05)
#
#
#
#
# def likelihood(position):
#     params_tmp = np.copy(position)  # here you pass the parameter vector; the point of making a copy of it is in order not to modify it
#     param_values[rate_mask] = 10 ** params_tmp  # see comment above *
#
#     params_10 = np.copy(param_values)
#     params_10[0] = 233
#     pars = [param_values, params_10]
#     result = solver.run(param_values=pars)
#
#     ysim_norm100 = normalize(result.observables[0]['MLKLa_obs'])
#     ysim_norm10 = normalize(result.observables[1]['MLKLa_obs'])
#     # result = solver.run(param_values=param_values)
#     # ysim_norm = normalize(result.observables['MLKLa_obs'])
#     # error = np.sum(((y100 - ysim_norm) ** 2))
#
#     logp_y100 = np.sum(y100_data.logpdf(ysim_norm100))
#     logp_y10 = np.sum(y10_data.logpdf(ysim_norm10))
#
#     logp_total = logp_y100 + logp_y10
#
#     if np.isnan(logp_total):
#         logp_total = -np.inf
#
#     # e1 = np.sum(((y100 - ysim_norm100) ** 2))
#     # e2 = np.sum(((y10 - ysim_norm10) ** 2))
#     # error = e1 + e2
#
#     return logp_total
# sampled_params_list = [SampledParam(norm, loc=par_priors, scale=2)]


sampled_params_list = list()
sp_p1f = SampledParam(norm, loc=np.log10(3.304257e-02), scale=2.0)
sampled_params_list.append(sp_p1f)
sp_p1r = SampledParam(norm, loc=np.log10(0.009791216), scale=2.0)
sampled_params_list.append(sp_p1r)
sp_p2f = SampledParam(norm, loc=np.log10(0.006110069), scale=2.0)
sampled_params_list.append(sp_p2f)
sp_p3f = SampledParam(norm, loc=np.log10(4.319219e-02), scale=2.0)
sampled_params_list.append(sp_p3f)
sp_p3r = SampledParam(norm, loc=np.log10(0.004212645), scale=2.0)
sampled_params_list.append(sp_p3r)
sp_p4f = SampledParam(norm, loc=np.log10(1.164332e-02), scale=2.0)
sampled_params_list.append(sp_p4f)
sp_p4r = SampledParam(norm, loc=np.log10(0.02404257), scale=2.0)
sampled_params_list.append(sp_p4r)
sp_p5f = SampledParam(norm, loc=np.log10(3.311086e-02), scale=2.0)
sampled_params_list.append(sp_p5f)
sp_p5r = SampledParam(norm, loc=np.log10(0.04280399), scale=2.0)
sampled_params_list.append(sp_p5r)
sp_p6f = SampledParam(norm, loc=np.log10(2.645815e-02), scale=2.0)
sampled_params_list.append(sp_p6f)
sp_p6r = SampledParam(norm, loc=np.log10(0.01437707), scale=2.0)
sampled_params_list.append(sp_p6r)
sp_p7f = SampledParam(norm, loc=np.log10(0.2303744), scale=2.0)
sampled_params_list.append(sp_p7f)
sp_p8f = SampledParam(norm, loc=np.log10(2.980688e-02), scale=2.0)
sampled_params_list.append(sp_p8f)
sp_p8r = SampledParam(norm, loc=np.log10(0.04879773), scale=2.0)
sampled_params_list.append(sp_p8r)
sp_p9f = SampledParam(norm, loc=np.log10(1.121503e-02), scale=2.0)
sampled_params_list.append(sp_p9f)
sp_p9r = SampledParam(norm, loc=np.log10(0.001866713), scale=2.0)
sampled_params_list.append(sp_p9r)
sp_p10f = SampledParam(norm, loc=np.log10(0.7572178), scale=2.0)
sampled_params_list.append(sp_p10f)
sp_p11f = SampledParam(norm, loc=np.log10(1.591283e-02), scale=2.0)
sampled_params_list.append(sp_p11f)
sp_p11r = SampledParam(norm, loc=np.log10(0.03897146), scale=2.0)
sampled_params_list.append(sp_p11r)
sp_p12f = SampledParam(norm, loc=np.log10(3.076363), scale=2.0)
sampled_params_list.append(sp_p12f)
sp_p13f = SampledParam(norm, loc=np.log10(3.73486), scale=2.0)
sampled_params_list.append(sp_p13f)
sp_p13r = SampledParam(norm, loc=np.log10(3.2162e-02), scale=2.0)
sampled_params_list.append(sp_p13r)
sp_p14f = SampledParam(norm, loc=np.log10(8.78243e-02), scale=2.0)
sampled_params_list.append(sp_p14f)
sp_p14r = SampledParam(norm, loc=np.log10(0.02906341), scale=2.0)
sampled_params_list.append(sp_p14r)
sp_p15f = SampledParam(norm, loc=np.log10(5.663104e-02), scale=2.0)
sampled_params_list.append(sp_p15f)
sp_p15r = SampledParam(norm, loc=np.log10(0.02110469), scale=2.0)
sampled_params_list.append(sp_p15r)
sp_p16f = SampledParam(norm, loc=np.log10(0.1294086), scale=2.0)
sampled_params_list.append(sp_p16f)
sp_p16r = SampledParam(norm, loc=np.log10(0.3127598), scale=2.0)
sampled_params_list.append(sp_p16r)
sp_p17f = SampledParam(norm, loc=np.log10(0.429849), scale=2.0)
sampled_params_list.append(sp_p17f)
sp_p18f = SampledParam(norm, loc=np.log10(2.33291e-02), scale=2.0)
sampled_params_list.append(sp_p18f)
sp_p18r = SampledParam(norm, loc=np.log10(0.007077505), scale=2.0)
sampled_params_list.append(sp_p18r)
sp_p19f = SampledParam(norm, loc=np.log10(0.6294062), scale=2.0)
sampled_params_list.append(sp_p19f)
sp_p20f = SampledParam(norm, loc=np.log10(0.06419313), scale=2.0)
sampled_params_list.append(sp_p20f)
sp_p21f = SampledParam(norm, loc=np.log10(0.008584654), scale=2.0)
sampled_params_list.append(sp_p21f)
sp_p22f = SampledParam(norm, loc=np.log10(8.160445e-02), scale=2.0)
sampled_params_list.append(sp_p22f)
sp_p22r = SampledParam(norm, loc=np.log10(4.354384e-03), scale=2.0)
sampled_params_list.append(sp_p22r)
sp_p23f = SampledParam(norm, loc=np.log10(0.008584654), scale=2.0)
sampled_params_list.append(sp_p23f)
sp_p24f = SampledParam(norm, loc=np.log10(8.160445e-02), scale=2.0)
sampled_params_list.append(sp_p24f)
sp_p24r = SampledParam(norm, loc=np.log10(4.354384e-02), scale=2.0)
sampled_params_list.append(sp_p24r)
sp_p25f = SampledParam(norm, loc=np.log10(1.278903), scale=2.0)
sampled_params_list.append(sp_p25f)

#Starting arrays from PSO output for each chain
pso0 = np.load('optimizer_best_100_100_9_20_necromulti_pso0.npy')
pso1 = np.load('optimizer_best_100_100_9_20_necromulti_pso1.npy')
pso2 = np.load('optimizer_best_100_100_9_20_necromulti_pso2.npy')
pso3 = np.load('optimizer_best_100_100_9_20_necromulti_pso3.npy')
pso4 = np.load('optimizer_best_100_100_9_20_necromulti_pso4.npy')
startvals = [pso0, pso1, pso2, pso3, pso4]

#Starting pydream calibration

if __name__ == '__main__':

    # Run DREAM sampling.  Documentation of DREAM options is in Dream.py.
    converged = False
    total_iterations = niterations
    sampled_params, log_ps = run_dream(parameters=sampled_params_list, likelihood=likelihood,
                                       niterations=niterations, nchains=nchains, multitry=False,
                                       gamma_levels=4, adapt_gamma=True, history_thin=1,
                                       model_name='necro_smallest_dreamzs116_5chainnew2', verbose=True)

    # Save sampling output (sampled parameter values and their corresponding logps).
    for chain in range(len(sampled_params)):
        np.save('necro_smallest_dreamzs_5chain_sampled_params_chain116_new2' + str(chain)+'_'+str(total_iterations), sampled_params[chain])
        np.save('necro_smallest_dreamzs_5chain_logps_chain116_new2' + str(chain)+'_'+str(total_iterations), log_ps[chain])

    #Check convergence and continue sampling if not converged

    GR = Gelman_Rubin(sampled_params)
    print('At iteration: ',total_iterations,' GR = ',GR)
    np.savetxt('necro_smallest_dreamzs_5chain116_GelmanRubin_iteration_new2'+str(total_iterations)+'.txt', GR)

    old_samples = sampled_params
    if np.any(GR>1.2):
        starts = [sampled_params[chain][-1, :] for chain in range(nchains)]
        while not converged:
            total_iterations += niterations
            sampled_params, log_ps = run_dream(parameters=sampled_params_list, likelihood=likelihood,
                                               niterations=niterations, nchains=nchains, start=starts, multitry=False, gamma_levels=4,
                                               adapt_gamma=True, history_thin=1, model_name='necro_smallest_dreamzs116_5chainnew2',
                                               verbose=True, restart=True)


            # Save sampling output (sampled parameter values and their corresponding logps).
            for chain in range(len(sampled_params)):
                np.save('necro_smallest_dreamzs116_5chain_sampled_params_chainnew2_' + str(chain)+'_'+str(total_iterations), sampled_params[chain])
                np.save('necro_smallest_dreamzs116_5chain_logps_chainnew2_' + str(chain)+'_'+str(total_iterations), log_ps[chain])

            old_samples = [np.concatenate((old_samples[chain], sampled_params[chain])) for chain in range(nchains)]
            GR = Gelman_Rubin(old_samples)
            print('At iteration: ',total_iterations,' GR = ',GR)
            np.savetxt('necro_smallest_dreamzs116_5chain_GelmanRubin_iterationnew2_' + str(total_iterations)+'.txt', GR)

            if np.all(GR<1.2):
                converged = True

    try:
        #Plot output
        import seaborn as sns
        from matplotlib import pyplot as plt
        total_iterations = len(old_samples[0])
        burnin = total_iterations/2
        samples = np.concatenate(tuple([old_samples[i][int(burnin):, :] for i in range(nchains)]))

        ndims = len(sampled_params_list)
        colors = sns.color_palette(n_colors=ndims)
        for dim in range(ndims):
            fig = plt.figure()
            sns.distplot(samples[:, dim], color=colors[dim], norm_hist=True)
            fig.savefig('PyDREAM_necro116_smallest_dimensionnew2_'+str(dim))

    except ImportError:
        pass

else:

    run_kwargs = {'parameters':sampled_params_list, 'likelihood':likelihood, 'niterations':niterations, 'nchains':nchains, \
                  'multitry':False, 'gamma_levels':4, 'adapt_gamma':True, 'history_thin':1, 'model_name':'necro_smallest_dreamzs116_5chainnew2', 'verbose':False}

