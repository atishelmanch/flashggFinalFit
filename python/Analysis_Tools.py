#####################################################################################################
#-- Abraham Tishelman-Charny                                                                        #
#-- 18 April 2021                                                                                   #
#                                                                                                   #
# The purpose of this module is to define methods to be called by the Analysis class                #
#####################################################################################################

##-- Imports 
import os 

##-- Define standard configuration parameters 
ConfigParams = {
    "nTupleDirec" : "/eos/user/a/atishelm/ntuples/HHWWgg_flashgg/January_2021_Production/", ##-- Location of 2016, 2017, 2018 folders each containing 
    "WorkingDirectory" : "/afs/cern.ch/work/a/atishelm/private/fggfinalfit/CMSSW_10_2_13/src/flashggFinalFit/" ,
    "doSystematics" : 0
}

##-- Get single higgs tree label from file name 
def GetSingleHiggsString(f):
    SingleHiggsStrings = {
        "GluGluHToGG" : "ggh",
        "VBFHToGG" : "vbf",
        "VHToGG" : "wzh", 
        "ttHJetToGG" : "tth"
    }
    for SingleHiggsString in SingleHiggsStrings:
        if (SingleHiggsString in f):
            process = SingleHiggsStrings[SingleHiggsString]

    return process 

##-- Rename trees to standard (HHWWgg) convention 
def RenameTrees(SingleHiggs, year, process, InputFile, analysisLabel, input_node, doSystematics):
    print "Renaming Trees..."   #
    WorkingDirectory = ConfigParams["WorkingDirectory"]
    os.chdir(WorkingDirectory)    
    UniqueExt = "SL_%s_%s_%s"%(analysisLabel, process, year)
    if(SingleHiggs):
        outputFile = "./%s_%s.root"%(year, UniqueExt)
    else: 
        # outputFile = ""
        outputFile = "./" + process + "_node_" + input_node  + "_" + year + "_" + UniqueExt + ".root"
    RenamedCats = 'HHWWggTag_SLDNN_0,HHWWggTag_SLDNN_1,HHWWggTag_SLDNN_2,HHWWggTag_SLDNN_3' # output cat name, it will be used in subsequence step
    InputTreeCats = 'HHWWggTag_SL_0,HHWWggTag_SL_1,HHWWggTag_SL_2,HHWWggTag_SL_3' #input cat name in the tree
    ##-- Selections to apply, if desired 
    SELECTIONS = "" ##-- If desired can add single H scale factors here to account for half single higgs events used in DNN training 
    RENAME_COMMAND = 'root -b -q RenameTrees/RenameTrees.C\\(\\%s\\,\\"%s\\",\\"%s\\",\\"%s\\"\\,\\"%s\\"\\,\\"%s\\"\\,\\"%s\\"\\,\\"%s\\"\\,\\"%s\\"\\,\\%s\\)'%(str(SingleHiggs), str(year), str(process), str(InputFile), str(outputFile), str(RenamedCats), str(InputTreeCats), str(SELECTIONS), str(input_node), str(doSystematics)) ##-- Cannot have spaces in C file argument! 
    os.system(RENAME_COMMAND)
    ##-- Move output file to proper location 
    WorkingDirectory = ConfigParams["WorkingDirectory"]
    os.system("mv %s/%s %s/Trees2WS"%(WorkingDirectory, outputFile, WorkingDirectory))

##-- Convert trees to workspaces 
def TreesToWS(analysisLabel, process, year, SingleHiggs, input_node, doSystematics):
    WorkingDirectory = ConfigParams["WorkingDirectory"]
    UniqueExt = "SL_%s_%s_%s"%(analysisLabel, process, year)
    inputWorkspace = "%s/Workspaces_%s"%(WorkingDirectory, analysisLabel)
    InWSdirec = "%s/Signal/Input/%s/"%(inputWorkspace, year) ##-- SIGNAL direc
    inDirExists = os.path.exists(InWSdirec)
    if(not inDirExists):
        os.system("mkdir -p %s"%(InWSdirec))
    os.chdir("%s/Trees2WS"%(WorkingDirectory))
    if(SingleHiggs):
        outputFile = "./%s_%s.root"%(year, UniqueExt)
    else: 
        outputFile = "./" + process + "_node_" + input_node  + "_" + year + "_" + UniqueExt + ".root"
    ##-- Determine to skip prefire from year flag in tree2ws.py 
    cats = 'HHWWggTag_SLDNN_0,HHWWggTag_SLDNN_1,HHWWggTag_SLDNN_2,HHWWggTag_SLDNN_3' #output cat name, it will be used in subsequence step
    mass = "125"
    SYST_FLAG = " "
    if(not doSystematics): 
        SYST_FLAG = " "
        # inputConfig = "HHWWgg_config_noSyst.py"

    else:
        SYST_FLAG = "--doSystematics"
        # inputConfig = "HHWWgg_config.py"

    TREESTOWS_COMMAND = "python trees2ws.py --inputConfig HHWWgg_config.py --inputTreeFile ./%s  --inputMass %s --productionMode %s  --year %s %s --UniqueName %s --cats %s"%(outputFile, mass, process, year, SYST_FLAG, UniqueExt, cats)
    os.system(TREESTOWS_COMMAND)
    catNames = [c for c in cats.split(',')]
    for catName in catNames:
        COPY_COMMAND_ONE = "cp ws_%s_%s/%s.root %s/Signal/Input/%s/Shifted_M125_%s_%s.root"%(process, UniqueExt, UniqueExt, inputWorkspace, year, process, catName)
        COPY_COMMAND_TWO = "cp ws_%s_%s/%s.root %s/Signal/Input/%s/output_M125_%s_%s.root"%(process, UniqueExt, UniqueExt, inputWorkspace, year, process, catName)
        os.system(COPY_COMMAND_ONE)
        os.system(COPY_COMMAND_TWO)
    os.system("rm %s"%(outputFile))

def Ftest(analysisLabel, process, year, SingleHiggs, doSystematics, input_node):
    WorkingDirectory = ConfigParams["WorkingDirectory"]
    print "Running Ftest"
    os.chdir("%s/Signal"%(WorkingDirectory))
    inputWorkspace = "%s/Workspaces_%s"%(WorkingDirectory, analysisLabel)
    InWSdirec = "%s/Signal/Input/%s/"%(inputWorkspace, year) ##-- SIGNAL direc
    ext = "SL_%s_%s"%(analysisLabel, process)
    if(SingleHiggs):
        node = ""
    else:
        node = input_node
        # pass 
    categories = 'HHWWggTag_SLDNN_0,HHWWggTag_SLDNN_1,HHWWggTag_SLDNN_2,HHWWggTag_SLDNN_3'
    configParams = {
        "{NODE}" : node,
        "{YEAR}" : year, 
        "{PROCS}" : process,
        "{EXT}" : ext,
        "{CAT}" : categories,
        "{INPUTDIR}" : InWSdirec
    }
    ##-- Create configuration file based on template 

    if(SingleHiggs):
        configFileName = "HHWWgg_single_higgs"
    else:
        configFileName = "HHWWgg_config"

    os.system("rm %s.py"%(configFileName))
    fin = open("%s_TEMPLATE.txt"%(configFileName), "rt")
    fout = open("%s.py"%(configFileName), "wt")
    for line in fin:
        replaceInLine = 0 
        for key in configParams:
            if key in line:
                replaceInLine = 1 
                fout.write(line.replace(key, configParams[key]))

        if(not replaceInLine):
            fout.write(line)
    fin.close()
    fout.close()
    if(SingleHiggs): FTEST_COMMAND = 'python RunSignalScripts.py --inputConfig %s.py --mode fTest --modeOpts "doPlots" '%(configFileName)
    else: FTEST_COMMAND = 'python RunSignalScripts.py --inputConfig %s.py --mode fTest --modeOpts "doPlots"'%(configFileName)
    os.system(FTEST_COMMAND)

    websiteOutDir = ""
    if(SingleHiggs):
        websiteOutDir = process
    else:
        websiteOutDir = "node_%s"%(node)    

    print "COPYING PLOTS:"
    phpLoc = "/eos/user/a/atishelm/www/HHWWgg/fggfinalfit/index.php" ##-- Location of php file for copying to new website directories 
    website = "/eos/user/a/atishelm/www/HHWWgg/fggfinalfit/%s/%s/%s/"%(analysisLabel, year, websiteOutDir)
    os.system("mkdir -p %s"%(website))
    os.system("cp %s /eos/user/a/atishelm/www/HHWWgg/fggfinalfit/%s"%(phpLoc, analysisLabel))
    os.system("cp %s /eos/user/a/atishelm/www/HHWWgg/fggfinalfit/%s/%s"%(phpLoc, analysisLabel, year))
    os.system("cp %s %s"%(phpLoc, website))

    extLabel = ""
    if(SingleHiggs):
        extLabel = "single_Higgs"
    else:
        extLabel = "node_%s"%(node)

    COPY_COMMAND_ONE = "cp %s/Signal/outdir_%s_%s_%s/fTest/Plots/*.png %s"%(WorkingDirectory, ext, year, extLabel, website)
    COPY_COMMAND_TWO = "cp %s/Signal/outdir_%s_%s_%s/fTest/Plots/*.pdf %s"%(WorkingDirectory, ext, year, extLabel, website)
    os.system(COPY_COMMAND_ONE)
    os.system(COPY_COMMAND_TWO)
    if(doSystematics):
        RUN_SYSTEMATICS_COMMAND = "python RunSignalScripts.py --inputConfig %s.py --mode calcPhotonSyst"%(configFileName)
        os.system(RUN_SYSTEMATICS_COMMAND)

def FinalSignalFit(analysisLabel, process, year, SingleHiggs, node):
    print "Fitting Signal"
    ext = "SL_%s_%s"%(analysisLabel, process)
    WorkingDirectory = ConfigParams["WorkingDirectory"]
    os.chdir("%s/Signal"%(WorkingDirectory))
    if(SingleHiggs):
        SIGNAL_FIT_COMMAND = "python RunSignalScripts.py --inputConfig HHWWgg_single_higgs.py --mode signalFit --groupSignalFitJobsByCat"
    else: 
        SIGNAL_FIT_COMMAND = "python RunSignalScripts.py --inputConfig HHWWgg_config.py --mode signalFit --groupSignalFitJobsByCat"
    os.system(SIGNAL_FIT_COMMAND)
    categories = 'HHWWggTag_SLDNN_0,HHWWggTag_SLDNN_1,HHWWggTag_SLDNN_2,HHWWggTag_SLDNN_3'
    for catName in categories.split(','):
        print "On category: ",catName

        extLabel = ""
        if(SingleHiggs):
            extLabel = "single_Higgs"
        else:
            extLabel = "node_%s"%(node)



        outDir = "%s/Signal/outdir_%s_%s_%s"%(WorkingDirectory, ext, year, extLabel)
        outFile = "CMS-HGG_sigfit_%s_%s_%s_%s_%s_%s.root"%(ext, year, extLabel, process, year, catName)
        outFileCopy = "CMS-HGG_sigfit_%s_%s_%s_%s.root"%(ext, year, extLabel, catName)
        os.system("cp %s/signalFit/output/%s %s/%s"%(outDir, outFile, outDir, outFileCopy))
        PLOT_COMMAND = "python RunPlotter.py --procs all --years %s --cats %s --ext %s_%s_%s --HHWWggLabel %s "%(year, catName, ext, year, extLabel, ext)
        os.system(PLOT_COMMAND)

        websiteOutDir = ""
        if(SingleHiggs):
            websiteOutDir = process
        else:
            websiteOutDir = "node_%s"%(node)  

        print "COPYING PLOTS:"
        phpLoc = "/eos/user/a/atishelm/www/HHWWgg/fggfinalfit/index.php" ##-- Location of php file for copying to new website directories 
        website = "/eos/user/a/atishelm/www/HHWWgg/fggfinalfit/%s/%s/%s/"%(analysisLabel, year, websiteOutDir)
        os.system("mkdir -p %s"%(website))
        os.system("cp %s /eos/user/a/atishelm/www/HHWWgg/fggfinalfit/%s"%(phpLoc, analysisLabel))
        os.system("cp %s /eos/user/a/atishelm/www/HHWWgg/fggfinalfit/%s/%s"%(phpLoc, analysisLabel, year))
        os.system("cp %s %s"%(phpLoc, website))
        COPY_COMMAND_ONE = "cp %s/Signal/outdir_%s_%s_%s/Plots/*.png %s"%(WorkingDirectory, ext, year, extLabel, website)
        COPY_COMMAND_TWO = "cp %s/Signal/outdir_%s_%s_%s/Plots/*.pdf %s"%(WorkingDirectory, ext, year, extLabel, website)
        os.system(COPY_COMMAND_ONE)
        os.system(COPY_COMMAND_TWO)
    os.chdir(WorkingDirectory)