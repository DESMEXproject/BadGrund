#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 09:46:05 2022

@author: nazari
"""
import numpy as np
from saem import CSEMData
# %% comparing sounding

txpos = np.genfromtxt("Tx4.pos").T[:, ::-1]
data4 = CSEMData(datafile="Tx4_4/*.mat", txPos=txpos)
data4.setOrigin([580000., 5740000.])
data4.filter(fmin=12, fmax=2000)

# txpos = np.genfromtxt("Tx4.pos").T[:, ::-1]
# data8 = CSEMData(datafile="Tx4_8/*.mat", txPos=txpos)
# data8.setOrigin([580000., 5740000.])
# data8.filter(fmin=12, fmax=2000)

txpos = np.genfromtxt("Tx4.pos").T[:, ::-1]
data32 = CSEMData(datafile="Tx4_32/*.mat", txPos=txpos)
data32.setOrigin([580000., 5740000.])
data32.filter(fmin=12, fmax=2000)

x=3000
y=0

data4.setPos(position=[x,y], show=True)
# data8.setPos(position=[x,y], show=True)
data32.setPos(position=[x,y], show=True)

print(data32.rx[data32.nrx],data4.rx[data4.nrx])
print(data32.ry[data32.nrx],data4.ry[data4.nrx])

# %%
ax = data4.showSounding(position=[x,y], cmp=[1, 0, 0], color="blue", label="Bx (N=4)")
# data8.showSounding(position=[x,y], cmp=[1, 0, 0], color="k", label="Bx (N=8)", ax=ax)
data32.showSounding(position=[x,y], cmp=[1, 0, 0], color="lightblue", label="Bx (N=32)", ax=ax)

ax=data4.showSounding(position=[x,y], cmp=[0, 1, 0], color="red", label="By (N=4)")
# data8.showSounding(position=[x,y], cmp=[0, 1, 0], color="k", label="By (N=8)", ax=ax)
data32.showSounding(position=[x,y], cmp=[0, 1, 0], color="orange", label="By (N=32)", ax=ax)

ax=data4.showSounding(position=[x,y], cmp=[0, 0, 1], color="g", label="Bz (N=4)")
# data8.showSounding(position=[x,y], cmp=[0, 0, 1], color="k", label="Bz (N=8)", ax=ax)
data32.showSounding(position=[x,y], cmp=[0, 0, 1], color="m", label="Bz (N=32)", ax=ax)

# %%
ax = data4.showSounding(position=[x,y], cmp=[1, 0, 0], color="blue", label="Bx (N=4)")
data32.showSounding(position=[x,y], cmp=[1, 0, 0], color="lightblue", label="Bx (N=32)", ax=ax)
ax=data4.showSounding(position=[x,y], cmp=[0, 1, 0], color="red", label="By (N=4)", ax=ax)
data32.showSounding(position=[x,y], cmp=[0, 1, 0], color="orange", label="By (N=32)", ax=ax)
ax=data4.showSounding(position=[x,y], cmp=[0, 0, 1], color="g", label="Bz (N=4)", ax=ax)
data32.showSounding(position=[x,y], cmp=[0, 0, 1], color="m", label="Bz (N=32)", ax=ax)