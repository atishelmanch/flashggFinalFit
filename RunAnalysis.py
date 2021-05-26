#####################################################################################################
# Abraham Tishelman-Charny                                                                          #
# 18 April 2021                                                                                     #
#                                                                                                   #
# The purpose of this module is to create analysis instances and run corresponding final fit steps. #
#####################################################################################################
 
##-- Import analysis class and configuration parameters 
from python.Analysis import Analysis, ConfigParams  

# Analysis instance members: Signal trees, Data trees
# Output: Signal models, background models, limit 

year = "2016"
analysisLabel = "HHWWyyDNN_binary_EFT_noHgg_noNegWeights_BalanceYields_allBkgs_LOSignals_noPtOverM_withKinWeight_weightSel"

nTupleDirec = ConfigParams["nTupleDirec"]
doSystematics = ConfigParams["doSystematics"]
firstStep = 3 ##-- 0, 1, 2, ... 
analysis = Analysis(nTupleDirec, year, analysisLabel, doSystematics, firstStep)
SingleHiggsFiles = analysis.SingleHiggsFiles
SingleHiggs = 0 
SignalFiles = analysis.SignalFiles 

# ##-- Create Single Higgs models 
# for i, f in enumerate(SingleHiggsFiles):
#     # if(i <= 2):
#     #     print "Skipping %sth single higgs on purpose"%(i)
#     #     continue 
#     SingleHiggs = 1
#     analysis.FitSignal(f, SingleHiggs)

##-- Create HH->WWgg Signal Models
for i, f in enumerate(SignalFiles):
    SingleHiggs = 0
    print "Signal file:",f 
    analysis.FitSignal(f, SingleHiggs)

##-- Create Background Models 

del analysis 