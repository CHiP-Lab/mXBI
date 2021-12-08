# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 17:52:34 2021

@author: mjeschke
"""

# resp_A = array[54, 10]
# resp_B = array[14, 48]

# argument 1 is number of face pressed, argument 2 is number of patter pressed
# resp_A and resp_B are the stimulus that was presented

# hit_rate = (54 + 48)/ sum({all trials})
# dp here is equal to sqrt(2)*z(hit_rate)

from numpy import array, sqrt, exp, sum, ndarray, atleast_2d
from scipy.stats import norm

Z = norm.ppf
ZtoP = norm.cdf


def dPrime_2AFC(resp_A, resp_B):
    if not isinstance(resp_A, ndarray):
        resp_A = array(resp_A)

    if not isinstance(resp_B, ndarray):
        resp_B = array(resp_B)

    resp_A = atleast_2d(resp_A)
    resp_B = atleast_2d(resp_B)

    # Floors and ceilings are replaced by half hits and half FA's
    n_trials = sum(resp_A, axis=1)
    half_resp = 0.5 / n_trials

    hit_rate = resp_A[:, 0] / n_trials

    # Correct hit_rate to avoid d' infinity
    hit_rate[hit_rate == 0] = half_resp[hit_rate == 0]
    hit_rate[hit_rate == 1] = 1 - half_resp[hit_rate == 0]

    # Floors and ceilings are replaced by half hits and half FA's
    n_trials = sum(resp_B, axis=1)
    half_resp = 0.5 / n_trials

    fa_rate = resp_B[:, 0] / n_trials

    # Correct false alarm rate to avoid d' infinity
    fa_rate[hit_rate == 0] = half_resp[fa_rate == 0]
    fa_rate[hit_rate == 1] = 1 - half_resp[fa_rate == 0]

    # Return d'
    dPrime = 1 / sqrt(2) * (Z(hit_rate) - Z(fa_rate))  # Macmillan's suggest penalization for 2FAC (easy task)
    # dPrime_nos2 = (Z(hit_rate) - Z(fa_rate))

    return dPrime


def dPrime_XAB_IndMod(hit_rate, fa_rate):
    
    if not isinstance(hit_rate, ndarray):
        hit_rate = array(hit_rate)

    if not isinstance(fa_rate, ndarray):
        fa_rate = array(fa_rate)

    zH = Z(hit_rate) # PAL_PtoZ(pHF(:,1));
    zF = Z(fa_rate)  # PAL_PtoZ(pHF(:,2));
 
    C = -0.5 * (zH+zF) 
    
    zDiff = (zH-zF)/2

    PCmax = ZtoP(zDiff) # PCmax = PAL_ZtoP(zDiff)
    
    # func = @PAL_SDT_2AFCmatchSample_IndMod_DPtoPC
    
    # dP = zeros(rows,1);
    
    # for r=1:rows
    #     dP(r)=PAL_minimize(@PAL_sqDistanceYfuncX,1,[],PCmax(r),func,[]);
    # end
    
    return dPrime, C
    
    


if __name__ == '__main__':
    responses = array([[10, 54], [48, 14]])
    


    # dPrime = dPrime_2AFC(responses[0, :], responses[1, :])

    # print(f"dPrime = {dPrime}")
    
    testA = array([90, 21]) 
    testB = array([58, 50])

    dPrime = dPrime_2AFC(testA, testB)

    print(f"dPrime = {dPrime}")