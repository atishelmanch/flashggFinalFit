#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pickle

# 重点是rb和r的区别，rb是打开2进制文件，文本文件用r
f = open('/afs/cern.ch/work/c/chuw/HHWWgg/FinalFit/CMSSW_10_2_13/src/flashggFinalFit/Signal/outdir_dcb_2017/calcPhotonSyst/pkl/HHWWggTag_3.pkl','rb')
data = pickle.load(f)
print(data)
