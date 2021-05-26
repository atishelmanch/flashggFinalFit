# Input config file for running trees2ws

trees2wsCfg = {

  # Name of RooDirectory storing input tree
  'inputTreeDir':'tagsDumper/trees',

  # Variables to be added to dataframe: use wildcard * for common strings
  'mainVars':["CMS_hgg_mass","weight","dZ","centralObjectWeight","genMhh","LooseMvaSFUp01sigma","LooseMvaSFDown01sigma","PreselSFUp01sigma","PreselSFDown01sigma",
              "electronVetoSFUp01sigma","electronVetoSFDown01sigma","TriggerWeightUp01sigma","TriggerWeightDown01sigma","FracRVWeightUp01sigma","FracRVWeightDown01sigma",
              "MuonIDWeightUp01sigma","MuonIDWeightDown01sigma","ElectronIDWeightUp01sigma","ElectronIDWeightDown01sigma","ElectronRecoWeightUp01sigma","ElectronRecoWeightDown01sigma",
              "MuonIsoWeightUp01sigma","MuonIsoWeightDown01sigma","JetBTagCutWeightUp01sigma","JetBTagCutWeightDown01sigma","JetBTagReshapeWeightUp01sigma","JetBTagReshapeWeightDown01sigma",
              "prefireWeightUp01sigma","prefireWeightDown01sigma","puweight","lumi"], # Vars for the nominal RooDataSets

              ##-- For non-EFT signals 
              # "prefireWeightUp01sigma","prefireWeightDown01sigma","scaleWeights","pdfWeights","alphaSWeights","puweight","lumi"], # Vars for the nominal RooDataSets

              ##-- scaleWeights, pdfWeights, alphaSWeights missing from EFT BM production. 

  'dataVars':["CMS_hgg_mass","weight"], # Vars to be added for data
  'stxsVar':'',
  'notagVars':["weight"], # Vars to add to NOTAG RooDataset
  'systematicsVars':["CMS_hgg_mass","weight"], # Variables to add to sytematic RooDataHists
  'theoryWeightContainers':{},

  # List of systematics: use string YEAR for year-dependent systematics
  'systematics':["FNUFEB","FNUFEE","JECAbsoluteYEAR","JECAbsolute","JECBBEC1YEAR",
                 "JECBBEC1","JECEC2YEAR","JECEC2","JECFlavorQCD","JECHFYEAR","JECHF","JECRelativeBal",
                 "JECRelativeSampleYEAR","JEC","JER","MCScaleGain1EB","MCScaleGain6EB","MCScaleHighR9EB",
                 "MCScaleHighR9EE","MCScaleLowR9EB","MCScaleLowR9EE","MCSmearHighR9EBPhi","MCSmearHighR9EBRho",
                 "MCSmearHighR9EEPhi","MCSmearHighR9EERho","MCSmearLowR9EBPhi","MCSmearLowR9EBRho",
                 "MCSmearLowR9EEPhi","MCSmearLowR9EERho","MaterialCentralBarrel","MaterialForward",
                 "MaterialOuterBarrel","MvaShift","PUJIDShift","ShowerShapeHighR9EB","ShowerShapeHighR9EE",
                 "ShowerShapeLowR9EB","ShowerShapeLowR9EE","SigmaEOverEShift",
                 "metJecUncertainty","metJerUncertainty","metPhoUncertainty","metUncUncertainty"],

  # Analysis categories: python list of cats or use 'auto' to extract from input tree

  'cats':'auto' ##-- Pass as flag for HHWWgg 

}
