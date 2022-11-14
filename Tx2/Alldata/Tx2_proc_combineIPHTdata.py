# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 17:42:39 2022
"""


import numpy as np
from saem import CSEMData


# %% Reading Data
txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]

data1 = CSEMData(datafile="Tx2_1/*.mat", txPos=txpos)
data2 = CSEMData(datafile="Tx2_2/*.mat", txPos=txpos)
data4 = CSEMData(datafile="Tx2_4/*.mat", txPos=txpos)
data8 = CSEMData(datafile="Tx2_8/*.mat", txPos=txpos)
data32 = CSEMData(datafile="Tx2_32/*.mat", txPos=txpos)
# %% Combining the datas

Sdist1=450.      # first  Switch between the different cycles
Sdist2=900.      # second Switch between the different cycles

# data1.filter(minTxDist=200., maxTxDist=Sdist1)
# data1.filter(every=16)
# data1.filter(fmin=12, fmax=1400)
# data1.filter(fInd=np.arange(0, len(data1.f), 2))  # every second
# for fi in[4,5,6]:
#     data1.DATA[:, fi, :] = np.nan + 1j * np.nan
# # data1.showData(amphi=False)
# data1.showField("line",label='1 cycles')
# # data1.basename = "Tx2IPHT_1"
# # data1.saveData(cmp='all')
# # data1.showField("line",label='All')
# # dataname=data1.basename
# # with np.load( dataname + "Bx.npz") as data:
# #     f = data['freqs']
# #     print(f)

data2.filter(minTxDist=300., maxTxDist=Sdist1)
data2.filter(every=8)
# data2.showData(amphi=False)
data2.showField("line",label='2 cycles')

data4.filter(minTxDist=Sdist1, maxTxDist=Sdist2)
data4.filter(every=8)
# data4.showData(amphi=False)
data4.showField("line",label='4 cycles')

data8.filter(minTxDist=Sdist1, maxTxDist=Sdist2)
data8.filter(every=4)
# data4.showData(amphi=False)
data8.showField("line",label='8 cycles')

data32.filter(minTxDist=Sdist2, maxTxDist=3000)
# data32.showData(amphi=True)
data32.showField("line",label='32 cycles')

# data32.addData(data1)
# data32.addData(data2)
data32.addData(data4)
# data32.addData(data8)

data32.showData(nf=5, amphi=False)
# %% Filtering Frequencies
data32.filter(fmin=12, fmax=1400)
data32.filter(fInd=np.arange(0, len(data32.f), 2))  # every second

# %% Denoising
data32.deactivateNoisyData(rErr=0.5)
data32.estimateError()  # 5%+1pV/A
data32.deactivateNoisyData(rErr=0.5)
print(np.min(data32.ERR.imag))

data32.estimateError(relError=0.1,f=0,cmp=0) # x 
data32.estimateError(relError=0.1,f=0,cmp=1) # y
data32.estimateError(relError=0.1,f=0,cmp=2) # z

# hack option to mask data, (cmp 0-2, f 0-nFreq, rx pos 0-nRpos)
# edit y component, 2nd freq, line 5 data
# data32.DATA[1, 2, data32.line==5] = np.nan + 1j*np.nan

# %%
data32.setOrigin([580000., 5740000.])
# %% Save Data
data32.basename = "Tx2IPHT_32_4"
data32.saveData(cmp='all')
data32.showField("line",label='All')
# %% E2
data32.filter(every=2)
data32.basename += "_E2"
data32.saveData(cmp='all')
data32.showField("line",label='E2')
# %% E4
data32.filter(every=2)
data32.basename = data32.basename.replace("E2", "E4")
data32.saveData(cmp='all')
data32.showField("line",label='E4')
# %% comparing sounding

# txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]
# data4 = CSEMData(datafile="Tx2_4/tf/*.mat", txPos=txpos)
# data4.setOrigin([580000., 5740000.])
# data4.filter(fmin=12, fmax=2000)
# # data8 = CSEMData(datafile="8 cycles/*.mat", txPos=txpos)
# txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]
# data32 = CSEMData(datafile="Tx2_32/tf/*.mat", txPos=txpos)
# data32.setOrigin([580000., 5740000.])
# data32.filter(fmin=12, fmax=2000)

# x=2800
# y=2090

# data4.setPos(position=[x,y], show=True)
# data32.setPos(position=[x,y], show=True)

# print(data32.rx[data32.nrx],data4.rx[data4.nrx])
# print(data32.ry[data32.nrx],data4.ry[data4.nrx])

# ax = data4.showSounding(position=[x,y], cmp=[1, 0, 0], color="blue", label="Bx (N=4)")
# data32.showSounding(position=[x,y], cmp=[1, 0, 0], color="lightblue", label="Bx (N=32)", ax=ax)
# data4.showSounding(position=[x,y], cmp=[0, 1, 0], color="red", label="By (N=4)", ax=ax)
# data32.showSounding(position=[x,y], cmp=[0, 1, 0], color="orange", label="By (N=32)", ax=ax)
# %%
dataname=data32.basename
with np.load( dataname + "Bx.npz") as data:
    f = data['freqs']
    print(f)