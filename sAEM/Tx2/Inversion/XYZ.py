#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 17:27:35 2022

@author: nazari
"""
from saem import CSEMSurvey, CSEMData
import numpy as np
# survey = CSEMSurvey()
# # way 1
# # survey.addPatch("Alldata/Tx2IPHT_2BxByBz.npz")
# survey.addPatch("Alldata/Tx2IPHT_32_4BxByBz.npz")


survey = CSEMSurvey()
# way 1
# survey.addPatch("Alldata/Tx2IPHT_2BxByBz.npz")
survey.addPatch("../Tx2IPHT_4_32BxByBz.npz")

# for pi, p in enumerate(survey.patches):
#     if pi == 0:
#         for fi in[0,1,2,3,4,5]:
#             p.DATA[:, fi, :] = np.nan + 1j * np.nan

for p in survey.patches:
    p.cmp = [1, 1, 1]  # components
    p.filter(every=1)    
Cmp= "XYZ"  
    
survey.patches[0].generateDataPDF(pdffile='New.pdf', what='relerror', log=False, alim=[-1,1])
    
dataname='Tx2_'+Cmp 
survey.saveData(dataname)
# %%
# tx2 = CSEMData("Tx2IPHT_32_4BxByBz.npz")
# tx2.filter(every=4) 
# survey.addPatch(tx2)
# tx4 = CSEMData("Tx4IPHT_32_4BxByBz.npz")
# tx4.filter(every=4) 
# survey.addPatch(tx4)
# %%
kw = dict(inner_area_cell_size=2e3,
                 cell_size=1e6,
                 depth=1500,
                 quality=1.2,
                 symlog_threshold=1e-3,
                  topo='merge.asc',
                 dim=6e3,
                 rx_refine=1.,
                 tx_refine=10.,
                 lam=1.)
# survey.patches[0].cmp = [1, 0, 0]
survey.basename += Cmp
survey.inversion(**kw)


survey = CSEMSurvey(dataname + ".npz", allow_pickle=True)
resultdir='inv_results/'"new"+Cmp+"_invmesh_new"+Cmp+'/' 
survey.loadResults(dirname=resultdir)
for i, p in enumerate(survey.patches):
    p.generateDataPDF(resultdir+f"fit{i+1}.pdf",
                      mode="linefreqwise", x="y", alim=[1e-3, 1])
    p.generateDataPDF(resultdir+f"wmisfit{i+1}.pdf",
                     mode="patchwise", log=False, what='wmisfit') 
    
    
# survey = CSEMSurvey('Alldata/' + dataname + ".npz",allow_pickle=True)
# resultdir = "inv_results/newXYZ_invmesh_newXYZ/"
# survey.loadResults(dirname=resultdir)
# survey.generateDataPDF(resultdir+"fit.pdf", mode="linefreqwise", x="y", alim=[1e-3, 1])




# saemdata = np.load('Alldata/' + dataname + ".npz", allow_pickle=True)
# resultdir = "inv_results/newXYZ_invmesh_newXYZ/"
# saemdata.loadResults(dirname=resultdir)
# saemdata.generateDataPDF(resultdir+"fit.pdf", mode="linefreqwise", x="y", alim=[1e-3, 1])
# way 2
# tx2 = CSEMData("Tx2.npz")
# tx2.filter(...) 
# survey.addPatch(tx2)
# tx4 = CSEMData("Tx2.npz")
# tx4.filter(...) 
# survey.addPatch(tx4)
# survey.saveData("Tx2Tx4.npz")