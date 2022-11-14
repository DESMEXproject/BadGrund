#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 16:03:35 2022

@author: nazari
"""

from saem import CSEMSurvey

survey=CSEMSurvey()
survey.addPatch("Tx1IPHT_32_4BxByBz.npz")
survey.showPositions()
survey.inversion(check=True, inner_boundary_factor=.1)
