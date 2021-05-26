# Script for making signal model plot
import os, sys
import ROOT
import re, glob
import json
from optparse import OptionParser

from commonTools import *
from commonObjects import *
from tools.plottingTools import *

def get_options():
  parser = OptionParser()
  parser.add_option('--procs', dest='procs', default='all', help="Comma separated list of processes to include. all = sum all signal procs")  
  parser.add_option('--years', dest='years', default='2016,2017,2018', help="Comma separated list of years to include")  
  parser.add_option('--cats', dest='cats', default='', help="Comma separated list of analysis categories to include. all = sum of all categories, wall = weighted sum of categories (requires S/S+B from ./Plots/getCatInfo.py)")
  parser.add_option('--loadCatWeights', dest='loadCatWeights', default='', help="Load S/S+B weights for analysis categories (path to weights json file)")
  parser.add_option('--ext', dest='ext', default='test', help="Extension: defines output dir where signal models are saved")
  parser.add_option("--xvar", dest="xvar", default='CMS_hgg_mass:m_{#gamma#gamma}:GeV', help="x-var (name:title:units)")
  parser.add_option("--mass", dest="mass", default='125', help="Mass of datasets")
  parser.add_option("--HHWWggLabel", dest="HHWWggLabel", default='cHHH1', help="nodes")
  parser.add_option("--MH", dest="MH", default='125', help="Higgs mass (for pdf)")
  parser.add_option("--nBins", dest="nBins", default=80, type='int', help="Number of bins")
  parser.add_option("--pdf_nBins", dest="pdf_nBins", default=3200, type='int', help="Number of bins")
  parser.add_option("--threshold", dest="threshold", default=0.001, type='float', help="Threshold to prune process from plot default = 0.1% of total category norm")
  parser.add_option("--translateCats", dest="translateCats", default=None, help="JSON to store cat translations")
  parser.add_option("--translateProcs", dest="translateProcs", default=None, help="JSON to store proc translations")
  parser.add_option("--label", dest="label", default='Simulation Preliminary', help="CMS Sub-label")
  parser.add_option("--doFWHM", dest="doFWHM", default=False, action='store_true', help="Do FWHM")
  parser.add_option("--HHWWggSingleHiggsScale", dest = "HHWWggSingleHiggsScale", action = "store_true", help = "Apply scale factor of 2 to single higgs processes in HHWWgg analysis, in case half events are used for training and half for evaluation")
  return parser.parse_args()
(opt,args) = get_options()

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# Extract input files: for first file extract xvar
inputFiles = od()
citr = 0
if opt.cats in ['all','wall']:
  fs = glob.glob("%s/outdir_%s/CMS-HGG_sigfit_%s_*.root"%(swd__,opt.ext,opt.ext))
  for f in fs:
    cat = re.sub(".root","",f.split("/")[-1].split("_%s_"%opt.ext)[-1])
    inputFiles[cat] = f
    if citr == 0:
      w = ROOT.TFile(f).Get("wsig_13TeV")
      xvar = w.var(opt.xvar.split(":")[0])
      xvar.setPlotLabel(opt.xvar.split(":")[1])
      xvar.setUnit(opt.xvar.split(":")[2])
      alist = ROOT.RooArgList(xvar)
    citr += 1
else:
  for cat in opt.cats.split(","):
    f = "%s/outdir_%s/CMS-HGG_sigfit_%s_%s.root"%(swd__,opt.ext,opt.ext,cat)
    inputFiles[cat] = f
    if citr == 0:
      w = ROOT.TFile(f).Get("wsig_13TeV")
      xvar = w.var(opt.xvar.split(":")[0])
      xvar.setPlotLabel(opt.xvar.split(":")[1])
      xvar.setUnit(opt.xvar.split(":")[2])
      alist = ROOT.RooArgList(xvar)
    citr += 1

# Load cat S/S+B weights
if opt.loadCatWeights != '':
  with open( opt.loadCatWeights ) as jsonfile: catsWeights = json.load(jsonfile)

# Define dict to store data histogram and inclusive + per-year pdf histograms
hists = od()
hists['data'] = xvar.createHistogram("h_data", ROOT.RooFit.Binning(opt.nBins))
hists['data_2016'] = xvar.createHistogram("h_data", ROOT.RooFit.Binning(opt.nBins))
hists['data_2017'] = xvar.createHistogram("h_data", ROOT.RooFit.Binning(opt.nBins))
hists['data_2018'] = xvar.createHistogram("h_data", ROOT.RooFit.Binning(opt.nBins))
# print opt.nBins
hists['temp'] = xvar.createHistogram("temp", ROOT.RooFit.Binning(opt.nBins))
# Loop over files
for cat,f in inputFiles.iteritems():
  print " --> Processing %s: file = %s"%(cat,f)

  # Define cat weight
  wcat = catsWeights[cat] if opt.loadCatWeights != '' else 1.

  # Open signal workspace
  fin = ROOT.TFile(f)
  w = fin.Get("wsig_13TeV")
  w.var("MH").setVal(float(opt.MH))
  # Extract normalisations
  norms = od()
  data_rwgt = od()
  hpdfs = od()
  for year in opt.years.split(","):
    if opt.procs == 'all':
      allNorms = w.allFunctions().selectByName("*%s*normThisLumi"%year)
      for norm in rooiter(allNorms):
        proc = norm.GetName().split("%s_"%outputWSObjectTitle__)[-1].split("_%s"%year)[0]
        k  =  "%s__%s"%(proc,year)
        _id = "%s_%s_%s_%s"%(proc,year,cat,sqrts__)
        norms[k] = w.function("%s_%s_normThisLumi"%(outputWSObjectTitle__,_id))
    else:
      for proc in opt.procs.split(","):
        k = "%s__%s"%(proc,year)
        _id = "%s_%s_%s_%s"%(proc,year,cat,sqrts__)
        norms[k] = w.function("%s_%s_normThisLumi"%(outputWSObjectTitle__,_id))
    
  # Iterate over norms: extract total category norm
  catNorm = 0
  for k, norm in norms.iteritems():
    proc, year = k.split("__")
    w.var("IntLumi").setVal(lumiScaleFactor*lumiMap[year])
    # print lumiScaleFactor*lumiMap[year]
    catNorm += norm.getVal()

  # Iterate over norms and extract data sets + pdfs
  # print("norms:",norms)
  for k, norm in norms.iteritems():
    proc, year = k.split("__")
    _id = "%s_%s_%s_%s"%(proc,year,cat,sqrts__)
    # print("_id:",_id)
    w.var("IntLumi").setVal(lumiScaleFactor*lumiMap[year])

    # Prune
    nval = norm.getVal()

    # if nval < opt.threshold*catNorm: continue # Prune processes which contribute less that threshold of signal mod

    # Make empty copy of dataset
    d = w.data("sig_mass_m%s_%s"%(opt.mass,_id))
    d_rwgt = d.emptyClone(_id)
    # print("d_rwgt:",d_rwgt)
    # Calc norm factor
    if d.sumEntries() == 0: nf = 0
    else: nf = nval/d.sumEntries()
    # Fill dataset with correct normalisation + reweight if using cat weights
    for i in range(d.numEntries()):
      p = d.get(i)
      rw, rwe = d.weight()*nf*wcat, d.weightError()*nf*wcat
      d_rwgt.add(p,rw,rwe)
    # Add dataset to container
    data_rwgt[_id] = d_rwgt

    # Extract pdf and create histogram
    pdf = w.pdf("extend%s_%sThisLumi"%(outputWSObjectTitle__,_id)) 
    hpdfs[_id] = pdf.createHistogram("h_pdf_%s"%_id,xvar,ROOT.RooFit.Binning(opt.pdf_nBins))
    hpdfs[_id].Scale(wcat*float(opt.nBins)/80) # FIXME: hardcoded 320

  # Fill total histograms: data, per-year pdfs and pdfs
  # print("data_rwgt:",data_rwgt)
  # print("HHWWggLabel:",opt.HHWWggLabel)
  for _id,d in data_rwgt.iteritems(): 
      # print "Check:",_id,"  ",d
      d.fillHistogram(hists['temp'],alist)
      # print "inte befor:",hists['data'].Integral()

      halfHiggsTrainings = ["SL_ggh", "SL_vbf", "SL_tth", "SL_wzh"]

      if( (opt.HHWWggLabel in halfHiggsTrainings) and (opt.HHWWggSingleHiggsScale)):
        print("SCALING PLOT OF SIGNAL BY FACTOR 2 ----- Should only be done if evaluating fits on half of original events")
        hists['temp'].Scale(2.)

      # if("2017" in _id and "SL_cHHH1" in opt.HHWWggLabel):
      #   print "DO NOT APPLY SCALE FACTOR"
      #   if ("HHWWggTag_SLDNN_0" in _id):
      #       print "tag0"
      #       hists['temp'].Scale(1.993)
      #   elif ("HHWWggTag_SLDNN_1" in _id):
      #       print "tag1"
      #       hists['temp'].Scale(1.984)
      #   elif ( "HHWWggTag_SLDNN_2" in _id ):
      #       print "tag2"
      #       hists['temp'].Scale(2.007)
      #   else: 
      #       print "tag3"
      #       hists['temp'].Scale(1.979)

      hists['data'].Add(hists['temp'],hists['data'])
      if ("2017" in _id ):
          hists['data_2017'].Add(hists['temp'],hists['data_2017'])
      elif ("2018" in _id ):
          hists['data_2018'].Add(hists['temp'],hists['data_2018'])
      elif("2016" in _id ):
          hists['data_2016'].Add(hists['temp'],hists['data_2016'])
      hists['temp'].Reset()
      # print "inte:",hists['data'].Integral()
      # print "inte16:",hists['data_2016'].Integral()
      # print "inte17:",hists['data_2017'].Integral()
      # print "inte18:",hists['data_2018'].Integral()

  # Sum pdf histograms
  # print("hpdfs:",hpdfs)
  for _id,p in hpdfs.iteritems():
    # print "PDF:",_id,"  ",p
    if 'pdf' not in hists: 
      hists['pdf'] = p.Clone("h_pdf")
      hists['pdf'].Reset()

    halfHiggsTrainings = ["SL_ggh", "SL_vbf", "SL_tth", "SL_wzh"]

    if( (opt.HHWWggLabel in halfHiggsTrainings) and (opt.HHWWggSingleHiggsScale) ):
      print("SCALING PLOT OF SIGNAL BY FACTOR 2 ----- Should only be done if evaluating fits on half of original events")
      p.Scale(2.)

    # Fill
    # if ("2017" in _id and "SL_cHHH1" in opt.HHWWggLabel):
    #     if "HHWWggTag_SLDNN_0" in _id:
    #         p.Scale(1.993)
    #     elif "HHWWggTag_SLDNN_1" in _id:
    #         p.Scale(1.984)
    #     elif "HHWWggTag_SLDNN_2" in _id:
    #         p.Scale(2.007)
    #     else:
    #         p.Scale(1.979)

    hists['pdf'] += p

  # print("hists:",hists)
  # print "==========Integral pdf:",hists['pdf'].Integral()
  # Per-year pdf histograms
  if len(opt.years.split(",")) > 1:
    #  hists['pdf_2016']=hists['pdf'].Clone()
    #  hists['pdf_2016'].Scale(0)
    #  print "Before:",hists['pdf_2016'].GetMaximum()
    for year in opt.years.split(","):
      if 'pdf_%s'%year not in hists or hists['pdf_2016'].Integral() == 0:
          print "Do not have pdf_",year
          hists['pdf_%s'%year] = hists['pdf'].Clone()
          hists['pdf_%s'%year].Scale(0)
      # Fill
      # print hists['pdf_2016'].GetMaximum()
      for _id,p in hpdfs.iteritems():
          #  print "P value:",_id,p.Integral()
          if year in _id:
              # print 'pdf_%s'%year,hists['pdf_%s'%year].GetMaximum()
              hists['pdf_%s'%year] += p
  
  
  # Garbage removal
  for d in data_rwgt.itervalues(): d.Delete()
  for p in hpdfs.itervalues(): p.Delete()
  w.Delete()
  fin.Close()
#  if ( opt.cats == "all"):
    #  output = ROOT.TFile(opt.HHWWggLabel+'_Run2_AllCats.root',"RECREATE")
#  else:
    #  output = ROOT.TFile(opt.HHWWggLabel+'Run2_'+opt.cats+".root","RECREATE")
#  output.mkdir("wsig_13TeV")
#  hists['pdf'].SetName("Run2_SL")
#  print hists['pdf'].GetMaximum()
#  hists['pdf'].Write()
#  output.Close()
# Make plot
if not os.path.isdir("%s/outdir_%s/Plots"%(swd__,opt.ext)): os.system("mkdir %s/outdir_%s/Plots"%(swd__,opt.ext))
plotSignalModel(hists,opt,_outdir="%s/outdir_%s/Plots"%(swd__,opt.ext),Label=opt.HHWWggLabel)
