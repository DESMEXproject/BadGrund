#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 10:48:33 2022

@author: nazari
"""


import numpy as np
from saem import CSEMData


# %% Reading Data
txpos = np.genfromtxt("Tx1.pos").T[:, ::-1]

data1 = CSEMData(datafile="Tx1_1/*.mat", txPos=txpos)
data2 = CSEMData(datafile="Tx1_2/*.mat", txPos=txpos)
# data4 = CSEMData(datafile="Tx1_4/tf/*.mat", txPos=txpos)
# data8 = CSEMData(datafile="Tx1_8/tf/*.mat", txPos=txpos)
# data32 = CSEMData(datafile="Tx1_32/tf/*.mat", txPos=txpos)
# %% Combining the datas

Sdist1=450.      # first  Switch between the different cycles
Sdist2=900.      # second Switch between the different cycles

data1.filter(minTxDist=150., maxTxDist=Sdist1)
data1.filter(every=16)
# data2.showData(amphi=False)
data1.showField("line",label='1 cycles')

data2.filter(minTxDist=200., maxTxDist=Sdist1)
data2.filter(every=8)
# data2.showData(amphi=False)
data2.showField("line",label='2 cycles')



# data2.addData(data1)
# data2.addData(data2)
# data2.addData(data8)

data2.showData(nf=5, amphi=False)
# %% Filtering Frequencies
data2.filter(fmin=12, fmax=1400)
data2.filter(fInd=np.arange(0, len(data2.f), 2))  # every second

# %% Denoising
data2.deactivateNoisyData(rErr=0.5)
data2.estimateError()  # 5%+1pV/A
data2.deactivateNoisyData(rErr=0.5)
print(np.min(data2.ERR.imag))

data2.estimateError(relError=0.1,f=0,cmp=0) # x 
data2.estimateError(relError=0.1,f=0,cmp=1) # y
data2.estimateError(relError=0.1,f=0,cmp=2) # z

# hack option to mask data, (cmp 0-2, f 0-nFreq, rx pos 0-nRpos)
# edit y component, 2nd freq, line 5 data
# data2.DATA[1, 2, data2.line==5] = np.nan + 1j*np.nan

# %%
data2.setOrigin([580000., 5740000.])
# %% Save Data
data2.basename = "Tx1IPHT_2"
data2.saveData(cmp='all')
data2.showField("line",label='All')
# %% E2
data2.filter(every=2)
data2.basename += "_E2"
data2.saveData(cmp='all')
data2.showField("line",label='E2')
# %% E4
data2.filter(every=2)
data2.basename = data2.basename.replace("E2", "E4")
data2.saveData(cmp='all')
data2.showField("line",label='E4')
# %% comparing sounding

# txpos = np.genfromtxt("Tx1.pos").T[:, ::-1]
# data4 = CSEMData(datafile="Tx1_4/tf/*.mat", txPos=txpos)
# data4.setOrigin([580000., 5740000.])
# data4.filter(fmin=12, fmax=2000)
# # data8 = CSEMData(datafile="8 cycles/*.mat", txPos=txpos)
# txpos = np.genfromtxt("Tx1.pos").T[:, ::-1]
# data2 = CSEMData(datafile="Tx1_32/tf/*.mat", txPos=txpos)
# data2.setOrigin([580000., 5740000.])
# data2.filter(fmin=12, fmax=2000)

# x=2800
# y=2090

# data4.setPos(position=[x,y], show=True)
# data2.setPos(position=[x,y], show=True)

# print(data2.rx[data2.nrx],data4.rx[data4.nrx])
# print(data2.ry[data2.nrx],data4.ry[data4.nrx])

# ax = data4.showSounding(position=[x,y], cmp=[1, 0, 0], color="blue", label="Bx (N=4)")
# data2.showSounding(position=[x,y], cmp=[1, 0, 0], color="lightblue", label="Bx (N=32)", ax=ax)
# data4.showSounding(position=[x,y], cmp=[0, 1, 0], color="red", label="By (N=4)", ax=ax)
# data2.showSounding(position=[x,y], cmp=[0, 1, 0], color="orange", label="By (N=32)", ax=ax)
# %%
dataname=data2.basename
with np.load( dataname + "Bx.npz") as data:
    f = data['freqs']
    print(f)