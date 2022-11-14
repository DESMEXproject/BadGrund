#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
custEM-based inversion
"""

#import matplotlib
#matplotlib.use("tkagg")
from custEM.meshgen.meshgen_tools import BlankWorld
from custEM.meshgen import meshgen_utils as mu
from custEM.inv.inv_utils import MultiFWD
import numpy as np
from scipy.spatial import ConvexHull
import pygimli as pg
from saem import CSEMData

tx = '2'
invmod = 'Z'
invmesh = 'invmesh_' + invmod

dataname = 'Tx' + tx + 'IPHT_32_4_E2Bz'
saemdata = np.load('Alldata/' + dataname + ".npz", allow_pickle=True)

sig_bg = 2e-3
# %% mesh generation
print(saemdata["rotation"])
M = BlankWorld(name=invmesh,
               x_dim=[-1e4, 1e4],
               y_dim=[-1e4, 1e4],
               z_dim=[-1e4, 1e4],
               preserve_edges=True,
               t_dir='./',
               topo='BadGrundUTM32.asc',
               inner_area_cell_size=1e4,
               easting_shift=-saemdata['origin'][0],
               northing_shift=-saemdata['origin'][1],
               rotation=float(saemdata['rotation'])*180/np.pi,
               outer_area_cell_size=1e8,
               )
txs = [mu.refine_path(saemdata['tx'][0], length=50.)]

points = saemdata["DATA"][0]["rx"][:, :2]
ch = ConvexHull(points)
pp = ch.points.T
invpoly = np.array([[*points[v, :]] for v in ch.vertices])
mp = np.mean(points, axis=0)
invpoly = invpoly - mp
invpoly *= 1.2
invpoly = invpoly + mp
invpoly = np.column_stack((invpoly, np.zeros(invpoly.shape[0])))
if 0:
    fig, ax = pg.plt.subplots()
    ax.plot(invpoly[:, 0], invpoly[:, 1], "k-")
    for data in saemdata["DATA"]:
        rx = data["rx"]         
        ax.scatter(rx[:, 0], rx[:, 1])
    for txi in txs:
        ax.plot(txi[:, 0], txi[:, 1])
    fig.savefig("pos.pdf")

M.build_surface(insert_line_tx=txs)
M.add_inv_domains(-1500., invpoly, cell_size=1.6e6)
M.build_halfspace_mesh()
# %%
allrx = mu.resolve_rx_overlaps([data["rx"] for data in saemdata["DATA"]], 1.)
rx_tri = mu.refine_rx(allrx, 5., 60.)
M.add_paths(rx_tri)
# add receiver locations to parameter file for all receiver patches
for rx in [data["rx"] for data in saemdata["DATA"]]:
    M.add_rx(rx)

M.extend_world(10., 10., 10.)
M.call_tetgen(tet_param='-pq1.3aA', print_infos=False)

#sdfsfsdfsd
###############################################################################
# %% run inversion

# set up forward operator
fop = MultiFWD(invmod, invmesh, saem_data=saemdata, sig_bg=sig_bg,
               n_cores=60, p_fwd=1, start_iter=0)
fop.setRegionProperties("*", limits=[1e-4, 1])

# set up inversion operator
inv = pg.Inversion(fop=fop)
inv.setPostStep(fop.analyze)
# inv.setRegularization(limits=[1e-4, 1], correlationLengths=[100, 200, 20])
dT = pg.trans.TransSymLog(1e-3)
inv.dataTrans = dT

# run inversion
invmodel = inv.run(fop.measured, fop.errors, lam=10., verbose=True,
                    # robustData=True,
                    # blockyModel=True,
                   startModel=fop.sig_0, maxIter=21)

###############################################################################
# %% post-processingelf
np.save(fop.inv_dir + 'inv_model.npy', invmodel)
res = 1. / invmodel
pgmesh = fop.mesh()
pgmesh['sigma'] = invmodel
pgmesh['res'] = res
pgmesh.exportVTK(fop.inv_dir + invmod + '_final_invmodel.vtk')
#fop._jac.save(fop.inv_dir + 'jacobian')
self = CSEMData('Alldata/' + dataname + ".npz")
resultdir = "inv_results/" + invmod + "_" +invmesh + "/"
self.loadResults(dirname=resultdir)
self.generateDataPDF(resultdir+"fit.pdf", mode="linefreqwise", x="y", alim=[1e-3, 1])
