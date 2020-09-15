# Config file: options for combine fitting

import sys

mode = sys.argv[1] # datacard or combine
print'mode: ',mode

_year = '2017'

combineScriptCfg = {

  # Setup
  'analysis':'HHWWgg',
  'analysis_type':'EFT',
  # 'analysis_type':'NMSSM',
  # 'analysis_type':'Res',
  'FinalState':'qqqq', # for HHWWgg. qqlnu, lnulnu, or qqqq. Will add combined eventually.
  'mode':mode,
  # 'mode':'combine',
  'doSystematics':1, # 0: do not include systematics in datacard. 1: include systematics in datacard
  'inputWSDir':'/eos/user/r/rasharma/post_doc_ihep/double-higgs/ntuples/September11_AllCut/HHWWgg_v2_6_AllCut_WW_Workspace_Hadded',
  #Procs will be inferred automatically from filenames
  #'HHWWggCatLabel':'2TotCatsCOMBINEDWithSyst', # for name of combine output files
  'HHWWggCatLabel':'2TotCatsbothcombined',
  # 'cats':'HHWWggTag_0',
  # 'cats':'HHWWggTag_1',
  'cats':'HHWWggTag_2',
  'ext':'HHWWgg_v2-6_%s_ChannelTest'%_year,
  # 'ext':'HHWWgg_v2-3_2017_2CatsSyst',
  # 'ext':'HHWWgg_v2-3_2017_2CatsSyst',
  'year':'2017',
  'signalProcs':'GluGluToHHTo', # "ggF" for Radion, FOR EFT "GluGluToHHTo"
  # 'signalProcs':'ggF', # "ggF" for Radion, FOR EFT "GluGluToHHTo"

  # Add UE/PS systematics to datacard (only relevant if mode == datacard)
  'doUEPS':0, # should I have this on?

  #Photon shape systematics
  'scales':'HighR9EB,HighR9EE,LowR9EB,LowR9EE,Gain1EB,Gain6EB',
  'scalesCorr':'MaterialCentralBarrel,MaterialOuterBarrel,MaterialForward,FNUFEE,FNUFEB,ShowerShapeHighR9EE,ShowerShapeHighR9EB,ShowerShapeLowR9EE,ShowerShapeLowR9EB',
  'scalesGlobal':'NonLinearity:UntaggedTag_0:2,Geant4',
  'smears':'HighR9EBPhi,HighR9EBRho,HighR9EEPhi,HighR9EERho,LowR9EBPhi,LowR9EBRho,LowR9EEPhi,LowR9EERho',

  # Job submission options
  # 'batch':'HTCONDOR',
  # 'queue':'workday',

  'batch':'',
  'queue':'',

  'printOnly':0, # For dry-run: print command only

}
