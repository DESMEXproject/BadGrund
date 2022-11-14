#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:24:33 2022

@author: nazari
"""

from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt
import numpy as np
from saem import CSEMData , CSEMSurvey

# %%
# %% Reading Data
txpos = np.genfromtxt("Tx1.pos").T[:, ::-1]

# data1 = CSEMData(datafile="Tx1_1/tf/*.mat", txPos=txpos)
data2 = CSEMData(datafile="Tx1_2/*.mat", txPos=txpos)
data4 = CSEMData(datafile="Tx1_4/*.mat", txPos=txpos)
data8 = CSEMData(datafile="Tx1_8/*.mat", txPos=txpos)
data32 = CSEMData(datafile="Tx1_32/*.mat", txPos=txpos)

# %%
data = data4
dataCmp = data32
DIF = np.zeros_like(dataCmp.DATA)
for c in range(3):
    for f in range(data32.nF):
        interp = LinearNDInterpolator(list(zip(data.rx, data.ry)), data.DATA[c, f, :])
        F = interp(dataCmp.rx, dataCmp.ry) 
        DIF[c, f, :] = F / dataCmp.DATA[c, f, :]
        # DIF[c, f, :] = F.real / data32.DATA[c, f, :].real - 1 + (
        #     F.imag / data32.DATA[c, f, :].imag - 1) * 1j
        
# %%
dataCmp.showPatchData(4, what=DIF, amphi=True, alim=[0.5, 2], plim=[-20, 20])
