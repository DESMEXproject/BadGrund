#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 09:46:05 2022

@author: nazari
"""
import numpy as np
from saem import CSEMData
# %% comparing sounding

txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]
data1 = CSEMData(datafile="Tx2_1/*.mat", txPos=txpos) # 1 Cycle
data1.setOrigin([580000., 5740000.])
data1.filter(fmin=12, fmax=2000)

txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]
data2 = CSEMData(datafile="Tx2_2/*.mat", txPos=txpos) # 2 Cycle
data2.setOrigin([580000., 5740000.])
data2.filter(fmin=12, fmax=2000)

txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]
data4 = CSEMData(datafile="Tx2_4/*.mat", txPos=txpos) # 4 Cycle
data4.setOrigin([580000., 5740000.])
data4.filter(fmin=12, fmax=2000)

txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]
data8 = CSEMData(datafile="Tx2_8/*.mat", txPos=txpos) # 8 Cycle
data8.setOrigin([580000., 5740000.])
data8.filter(fmin=12, fmax=2000)

txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]
data16 = CSEMData(datafile="Tx2_16/*.mat", txPos=txpos) # 16 Cycle
data16.setOrigin([580000., 5740000.])
data16.filter(fmin=12, fmax=2000)

txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]
data32 = CSEMData(datafile="Tx2_32/*.mat", txPos=txpos) # 32 Cycle
data32.setOrigin([580000., 5740000.])
data32.filter(fmin=12, fmax=2000)

txpos = np.genfromtxt("Tx2.pos").T[:, ::-1]
data64 = CSEMData(datafile="Tx2_64/*.mat", txPos=txpos) # 64 Cycle
data64.setOrigin([580000., 5740000.])
data64.filter(fmin=12, fmax=2000)

x=3850
y=2000

data4.setPos(position=[x,y], show=True)
data8.setPos(position=[x,y], show=True)
data32.setPos(position=[x,y], show=True)
data64.setPos(position=[x,y], show=True)

print(data32.rx[data32.nrx],data4.rx[data4.nrx],data8.rx[data8.nrx])
print(data32.ry[data32.nrx],data4.ry[data4.nrx],data8.ry[data8.nrx])

# %% Bx

ax =data1.showSounding(position=[x,y], cmp=[1, 0, 0], color="red", label="Bx (N=1)")
data2.showSounding(position=[x,y], cmp=[1, 0, 0], color="g", label="Bx (N=2)", ax=ax)
data4.showSounding(position=[x,y], cmp=[1, 0, 0], color="orange", label="Bx (N=4)", ax=ax)
data8.showSounding(position=[x,y], cmp=[1, 0, 0], color="k", label="Bx (N=8)", ax=ax)
data16.showSounding(position=[x,y], cmp=[1, 0, 0], color="lightblue", label="Bx (N=16)", ax=ax)
# data32.showSounding(position=[x,y], cmp=[1, 0, 0], color="blue", label="Bx (N=32)", ax=ax)
# data64.showSounding(position=[x,y], cmp=[1, 0, 0], color="m", label="Bx (N=64)", ax=ax)

# %% By

ax=data1.showSounding(position=[x,y], cmp=[0, 1, 0], color="red", label="By (N=1)")
data2.showSounding(position=[x,y], cmp=[0, 1, 0], color="g", label="By (N=2)", ax=ax)
data4.showSounding(position=[x,y], cmp=[0, 1, 0], color="orange", label="By (N=4)" , ax=ax)
data8.showSounding(position=[x,y], cmp=[0, 1, 0], color="k", label="By (N=8)", ax=ax)
data16.showSounding(position=[x,y], cmp=[0, 1, 0], color="lightblue", label="By (N=16)", ax=ax)
# data32.showSounding(position=[x,y], cmp=[0, 1, 0], color="blue", label="By (N=32)", ax=ax)
# data64.showSounding(position=[x,y], cmp=[0, 1, 0], color="m", label="By (N=64)", ax=ax)

# %% Bz

ax=data1.showSounding(position=[x,y], cmp=[0, 0, 1], color="red", label="Bz (N=1)")
data2.showSounding(position=[x,y], cmp=[0, 0, 1], color="g", label="Bz (N=2)", ax=ax)
data4.showSounding(position=[x,y], cmp=[0, 0, 1], color="orange", label="Bz (N=4)", ax=ax)
data8.showSounding(position=[x,y], cmp=[0, 0, 1], color="k", label="Bz (N=8)", ax=ax)
data16.showSounding(position=[x,y], cmp=[0, 0, 1], color="lightblue", label="Bz (N=16)", ax=ax)
# data32.showSounding(position=[x,y], cmp=[0, 0, 1], color="blue", label="Bz (N=32)", ax=ax)
# data64.showSounding(position=[x,y], cmp=[0, 0, 1], color="m", label="Bz (N=64)", ax=ax)

# %% All
ax = data4.showSounding(position=[x,y], cmp=[1, 0, 0], color="blue", label="Bx (N=4)")
data32.showSounding(position=[x,y], cmp=[1, 0, 0], color="lightblue", label="Bx (N=32)", ax=ax)
ax=data4.showSounding(position=[x,y], cmp=[0, 1, 0], color="red", label="By (N=4)", ax=ax)
data32.showSounding(position=[x,y], cmp=[0, 1, 0], color="orange", label="By (N=32)", ax=ax)
ax=data4.showSounding(position=[x,y], cmp=[0, 0, 1], color="g", label="Bz (N=4)", ax=ax)
data32.showSounding(position=[x,y], cmp=[0, 0, 1], color="m", label="Bz (N=32)", ax=ax)