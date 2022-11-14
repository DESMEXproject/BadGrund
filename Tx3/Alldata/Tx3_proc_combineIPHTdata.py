# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 17:42:39 2022
"""


import numpy as np
from saem import CSEMData


# %% Reading Data
txpos = np.genfromtxt("Tx3.pos").T[:, ::-1]

data4 = CSEMData(datafile="Tx3_4/*.mat", txPos=txpos)
# data8 = CSEMData(datafile="8 cycles/*.mat", txPos=txpos)
data32 = CSEMData(datafile="Tx3_32/*.mat", txPos=txpos)
# data32.generateDataPDF("data32.pdf")
# data4.generateDataPDF("data4.pdf")
# %% Combining the datas
Sdist=900.      # Switch between the different cycles
data32.filter(minTxDist=Sdist, maxTxDist=3000)
# data32.showData(amphi=True)
data32.showField("line",label='32')

data4.filter(minTxDist=450., maxTxDist=Sdist)
data4.filter(every=8)
# data4.showData(amphi=False)
data4.showField("line",label='4')
data32.addData(data4)
data32.showData(nf=5, amphi=False)
# %% remove Lines
data32.line[data32.line==1] = 0
data32.removeNoneLineData()
data32.line[data32.line==2] = 0
data32.removeNoneLineData()
data32.line[data32.line==3] = 0
data32.removeNoneLineData()
data32.line[data32.line==4] = 0
data32.removeNoneLineData()
# %% Generate PDF
data32.generateDataPDF("After_data32.pdf")
# data4.generateDataPDF("data4.pdf")
# %% Filtering Frequencies
data32.filter(fmin=12, fmax=1400)
data32.filter(fInd=np.arange(0, len(data32.f), 2))  # every second

# %% Denoising
data32.deactivateNoisyData(rErr=0.5)
data32.estimateError()  # 5%+1pV/A
data32.deactivateNoisyData(rErr=0.5)
print(np.min(data32.ERR.imag))

# data32.estimateError(relError=0.1,f=0,cmp=0) # x 
# data32.estimateError(relError=0.1,f=0,cmp=1) # y
# data32.estimateError(relError=0.1,f=0,cmp=2) # z

# hack option to mask data, (cmp 0-2, f 0-nFreq, rx pos 0-nRpos)
# edit y component, 2nd freq, line 5 data
# data32.DATA[1, 2, data32.line==5] = np.nan + 1j*np.nan

# %%
data32.setOrigin([580000., 5740000.])
# %% Save Data
data32.basename = "Tx3IPHT_32_4"
data32.saveData(cmp='all',txdir=1)
data32.showField("line",label='All')
# %% E2
data32.filter(every=2)
data32.basename += "_E2"
data32.saveData(cmp='all',txdir=1)
data32.showField("line",label='E2')
# %% E4
data32.filter(every=2)
data32.basename = data32.basename.replace("E2", "E4")
data32.saveData(cmp='all',txdir=1)
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
with np.load('Tx3IPHT_32_4_E2Bx.npz') as data:
    f = data['freqs']
    print(f)