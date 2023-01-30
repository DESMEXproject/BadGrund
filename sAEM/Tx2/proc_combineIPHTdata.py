# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 17:42:39 2022
"""


import numpy as np
from saem import CSEMData
from saem import plotting
from custEM.meshgen import DEM
import matplotlib.pyplot as plt
# %% Reading Data
txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]

data1 = CSEMData(datafile="tfN1/*.mat", txPos=txpos)
data2 = CSEMData(datafile="tfN2/*.mat", txPos=txpos)
data4 = CSEMData(datafile="tfN4/*.mat", txPos=txpos)
data8 = CSEMData(datafile="tfN8/*.mat", txPos=txpos)
data16 = CSEMData(datafile="tfN16/*.mat", txPos=txpos)
data32 = CSEMData(datafile="tfN32/*.mat", txPos=txpos)
data64 = CSEMData(datafile="tfN64/*.mat", txPos=txpos)

# %% Topography & Elevation
dem = DEM("Inversion/merge.asc")
# dem.show()
ez = dem(data4.rx, data4.ry)

plt.scatter(data4.rx, data4.ry, s=10, c=data4.rz-ez)
plt.colorbar()
xl = plt.gca().get_xlim()
yl = plt.gca().get_ylim()

fig, ax = plt.subplots()
dem.show(ax=ax)
plt.scatter(data4.rx, data4.ry, s=1, c=data4.rz-ez)
plt.colorbar()
ax.set_xlim(xl)
ax.set_ylim(yl)
# %% Combining the datas

start=100.
Sdist1=400.      # first  Switch between the different cycles
Sdist2=900.      # second Switch between the different cycles
end=3000.

# data1.filter(minTxDist=200., maxTxDist=Sdist1)
# data1.filter(every=16)
# data1.filter(fmin=12, fmax=1400)
# data1.filter(fInd=np.arange(0, len(data1.f), 2))  # every second
# for fi in[4,5,6]:
#     data1.DATA[:, fi, :] = np.nan + 1j * np.nan
# # data1.showData(amphi=False)
# data1.showField("line",label='1 cycles')
# # data1.basename = "Tx3IPHT_1"
# # data1.saveData(cmp='all')
# # data1.showField("line",label='All')


# data2.filter(minTxDist=start, maxTxDist=Sdist1)
# data2.filter(every=8)
# data2.showData(amphi=False)
# data2.showField("line",label='2 cycles', radius=50.)

data4.filter(minTxDist=Sdist1, maxTxDist=Sdist2)
data4.filter(every=8)
# data4.showData(amphi=False)
data4.showField("line",label='4 cycles', radius=50.)

# data8.filter(minTxDist=500, maxTxDist=1500)
# data8.filter(every=4)
# data4.showData(amphi=False)
# data8.showField("line",label='8 cycles', radius=50.)

data32.filter(minTxDist=Sdist2, maxTxDist=end)
# data32.showData(amphi=True)
data32.showField("line",label='32 cycles', radius=50.)

# data32.addData(data1)
# data32.addData(data2)
data32.addData(data4)
# data32.addData(data8)
# data32.showField("line",label='All', radius=50.)
# %% Topo
plotting.plotSymbols(data32.rx, data32.ry, data32.alt
                     , radius=50.,cmap='turbo'
                     , label='Altitude',bbox_inches="tight",background = "BKG")
# %%
# ztfs.topo(data32)                 
# %% remove Lines
# data32.line[data32.line==5] = 0
# data32.removeNoneLineData()
# data32.line[data32.line==2] = 0
# data32.removeNoneLineData()
# data32.line[data32.line==3] = 0
# data32.removeNoneLineData()
# data32.line[data32.line==4] = 0
# data32.removeNoneLineData()
# data32.showField("line",label='Removed', radius=50.)
# %% Generate PDF
# data32.generateDataPDF("After_data32.pdf")
# %% Filtering Frequencies
data32.filter(fmin=12, fmax=2050)
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
data32.basename = "Tx3IPHT_4_32"
dataname=data32.basename
data32.saveData(cmp=[1,1,1],txdir=-1)
data32.showField("line",label='All', radius=50.)

# %%
print(data32)
with np.load( dataname + "BxByBz.npz") as data:
    f = data['freqs']
    print(f)