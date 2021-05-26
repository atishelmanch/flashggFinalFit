import ROOT
from ROOT import *

import sys
import os

from optparse import OptionParser
def get_options():
  parser = OptionParser()
  # Take inputs from config file
  parser.add_option('--procs', dest='procs', default='', help="process")
  parser.add_option('--cats', dest='cats', default='', help="cats")
  parser.add_option('--inputDir', dest='inputDir', default='./', help="Input Dir")
  return parser.parse_args()
(opt,args) = get_options()

inDir = opt.inputDir
outDir = inDir 

values = [-5,0,5]
higgs_mass = 125
for cat in opt.cats.split(","):
    ws_name = 'tagsDumper/cms_hgg_13TeV'
    dataset_name = '%s_125_13TeV_%s'%(opt.procs,cat)
    temp_ws = TFile(inDir+'output_M125_%s_%s.root'%(opt.procs,cat)).Get(ws_name)
    for value in values:
        shift = value + higgs_mass
        dataset1 = (temp_ws.data(dataset_name)).Clone('%s_'%opt.procs + str(shift)+'_13TeV_%s'%(cat)) # includes process and category
        dataset1.Print()
        dataset1.changeObservableName('CMS_hgg_mass','CMS_hgg_mass_old')
        higgs_old = dataset1.get()['CMS_hgg_mass_old']
        higgs_new = RooFormulaVar( 'CMS_hgg_mass', 'CMS_hgg_mass', "(@0+%.1f)"%value,RooArgList(higgs_old) );
        dataset1.addColumn(higgs_new).setRange(105,145)
        dataset1.Print()
        output = TFile(outDir + 'Shifted_M'+str(shift)+'_%s_%s.root'%(opt.procs,cat),'RECREATE')
        output.mkdir("tagsDumper")
        output.cd("tagsDumper")
        ws_new = ROOT.RooWorkspace("cms_hgg_13TeV")
        getattr(ws_new,'import')(dataset1,RooCmdArg())
        ws_new.Write()
        output.Close()
