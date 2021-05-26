#####################################################################################################
#-- Abraham Tishelman-Charny                                                                        #
#-- 18 April 2021                                                                                   #
#                                                                                                   #
# The purpose of this module is to define the Analysis class for running all final fit steps        #
#####################################################################################################

##-- Imports 
import os 
from python.Analysis_Tools import *
    
##-- Define Analysis class 
class Analysis: 

    ##-- Constructor 
    def __init__(self, nTupleDirec, year, analysisLabel, doSystematics, firstStep):

        ##-- Set class instance attributes to constructor arguments 
        self.nTupleDirec = nTupleDirec
        self.year = year 
        self.analysisLabel = analysisLabel ##-- A uniquely defining analysis label to keep analysis outputs separate
        self.doSystematics = doSystematics
        self.firstStep = firstStep 

        ##-- Define signal and data file paths 
        self.fullDirec = "%s/%s/%s/"%(self.nTupleDirec, self.year, self.analysisLabel)
        # self.SignalFile = "%s/Signal_cHHH1_%s_all_CategorizedTrees.root"%(self.fullDirec, self.year) ##-- For EFT, get all nodes 
        self.SignalFiles = ["%s/Signal_1_%s_all_CategorizedTrees.root"%(self.fullDirec, self.year)] ##-- For EFT, get all nodes 
        # self.SignalFiles = ["%s/Signal_%s_%s_all_CategorizedTrees.root"%(self.fullDirec, str(node), self.year) for node in range(1,13)] ##-- For EFT, get all nodes 
        self.DataFile = "%s/Data_%s_CategorizedTrees.root"%(self.fullDirec, self.year)
        self.SingleHiggsFiles = ["%s/Single_H/%s"%(self.fullDirec, f) for f in os.listdir("%s/Single_H/"%(self.fullDirec))]

    ##-- Print Analysis MetaData 
    def PrintMetaData(self):
        print "Analysis Metadata:"
        print "Signal File:",self.SignalFile
        print "Data File:",self.DataFile
        print "Single Higgs Files:"
        for f in self.SingleHiggsFiles:
            print f

    ##-- Fit Signal Model
    def FitSignal(self, f, SingleHiggs):
        print "Fitting signal %s"%(f)

        ##-- Single Higgs
        if(SingleHiggs):
            process = GetSingleHiggsString(f)
            input_node = ""

        ##-- EFT nodes 
        else:
            process = "GluGluToHHTo2G2Qlnu"
            input_node = f.split('/')[-1].split('_')[1]

        ##-- Signal Fit steps 
        if(self.firstStep <= 0): RenameTrees(SingleHiggs, self.year, process, f, self.analysisLabel, input_node, self.doSystematics) ##-- Rename trees -- ##-- Can also use for applying SFs or custom weights / selections                 
        if(self.firstStep <= 1): TreesToWS(self.analysisLabel, process, self.year, SingleHiggs, input_node, self.doSystematics) ##-- Convert to workspaces                     
        if(self.firstStep <= 2): Ftest(self.analysisLabel, process, self.year, SingleHiggs, self.doSystematics, input_node) ##-- Run fTest           
        if(self.firstStep <= 3): FinalSignalFit(self.analysisLabel, process, self.year, SingleHiggs, input_node) ##-- Fit function from ftest and build signal model 
