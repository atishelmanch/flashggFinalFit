Table of Contents
=================

   * [FLASHgg Final Fits](#flashgg-final-fits)
      * [Contents](#contents)
      * [Known issues](#known-issues)
   * [HHWWgg Specific Instructions](#hhwwgg-specific-instructions)
      * [Clone Repository](#clone-repository)
      * [Background](#background)
         * [f-Test](#f-test)
      * [Signal](#signal)
      * [Datacard](#datacard)
      * [Combine](#combine)
      * [Plot](#plot)
   * [Known Issues](#known-issues-1)
      * [While running the signal model](#while-running-the-signal-model)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# FLASHgg Final Fits
The Final Fits package is a series of scripts which are used to run the final stages of the CMS Hgg analysis: signal modelling, background modelling, datacard creation and final statistical interpretation and final result plots.

## Contents
The FLASHgg Finals Fits package contains several subfolders which are used for the following steps:

* Create the Signal Model (see `Signal` dir)
* Create the Background Model (see `Background` dir)
* Generate a Datacard (see `Datacard` dir)
* Run `combine` and generate statistical interpretation plots. (see `Plots/FinalResults` dir)

Each of the relevant folders are documented with specific `README.md` files.

## Known issues

Recently some issues with memory have been observed with the workspaces (probably because there are so many processes and tags now). Crashes can occur due to a `std::bad_alloc()` error, which for now I have managed to circumvent by submitting to the batch (this is at Imperial College), e.g. for making the photon systematic dat files and the S+B fits. The problem is due to all the workspaces being loaded by the WSTFileWrapper class, so at some point this should be revisited and improved somwhow. 

# HHWWgg Specific Instructions 

## Clone Repository 

The cloning instructions are the same as above, except the forked repository should be cloned, like so:


```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git cms-init

# Install the GBRLikelihood package which contains the RooDoubleCBFast implementation
git clone git@github.com:jonathon-langford/HiggsAnalysis.git
# Install Combine as per the documentation here: cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit

# Compile external libraries
cd HiggsAnalysis
cmsenv
scram b -j 9

# Install Flashgg Final Fit packages
cd ..
git clone -b HHWWgg_Dev_runII_102x git@github.com:atishelmanch/flashggFinalFit.git # to clone via SSH 
cd flashggFinalFit/
```

Two packages need to be built with their own makefiles, if needed. Please note that there will be verbose warnings from BOOST etc, which can be ignored. So long as the `make` commands finish without error, then the compilation happened fine.:

```
cd ${CMSSW_BASE}/src/flashggFinalFit/Background
make
cd ${CMSSW_BASE}/src/flashggFinalFit/Signal
make
```

After cloning the repository, the main HHWWgg script to use is HHWWggFinalFitScript.sh, which is used to call each of the finalfit steps below.

## Background 

### f-Test

To produce a background model, you first need a config file. You can begin with the example `Background/HHWWgg_Synch_Background_Config.py`. This contains the parameters for running the background fits.

An explanation of the important parameters to set:

  * **inputWSDir**: Input workspace directory. This is the directory containing your hadded data workspace. If you are running on one year of data, for example 2017, this directory should contain one file: `allData.root`. This file name is hardcoded into the framework.
  * **website**: This contains the path of your webpage, where it will copy the necessary files.
  * **cats**: These are the categories to fit, where these categories are originally defined in flashgg. For example, for the current state of the HHWWgg semileptonic analysis there are two categories: HHWWggTag_0 corresponding to the semi-leptonic electron channel, and HHWWggTag_1 corresponding to the semi-leptonic muon channel. To produced background models for both categories, you should specify both categories separated by commas like so: 'HHWWggTag_0,HHWWggTag_1'
  * **ext**: Extension. This is used for the naming scheme of the output directory and files. This should be chosen and kept consistent for the extension used for the signal modelling. 
  * **year**: The data year. 2017 for 2017 data. 
  * **unblind**: (1): Data is unblinded. (0): Data blinded. 
  * **batch and queue**: These are for running in batch mode, which is currently not setup for HHWWgg. For now it automatically runs locally. 
  * **analysis**: This should be set to HHWWgg to run the HHWWgg specific naming schemes. 
  * **mode**: The function to run the script on. Options: [std,fTestOnly,bkgPlotsOnly].
  * **InSignalFitWSFile**: This is used for make background plot. When we don't have signal model then put `InSignalFitWSFile = ""`. Else, it will try to find the signal root file present in the signal directory. If RootFileName is `Signal/outdir_HHWWgg_v2-6_2017_ChannelTest_X550_HHWWgg_qqqq/CMS-HGG_sigfit_HHWWgg_v2-6_2017_ChannelTest_X550_HHWWgg_qqqq.root` then put `InSignalFitWSFile = "X550_HHWWgg_qqqq"`. 
  * **massStep**: This is used for make background plot. Step in which mass should vary. Put this to higher value for quick run.

After setting the python configuration file you want to use in the backgroundftest option in HHWWggFinalFitScript.sh, and setting the proper parameters in your configuration file, you can run the background ftest with:

```bash
. HHWWggFinalFitScript.sh backgroundftest
```

If this works properly, you should see the directory Background/outdir_<extension>/bkgfTest-Data containing many output images including multipdf_<category>.png/pdf showing the different functional fits to the data for each category. You should also see a root file Background/CMS-HGG-multipdf_<extension>.root containing the RooWorkspace "multipdf" containing the functional fit variables, pdfs and parameters, which can be seen with multipdf->Print(). 

## Signal 

Next are the functions to run on the signal. You can begin with the example configuration `Signal/HHWWgg_Synch_Signal_Config.py`.

This configuration contains the following parameters:
  * **systematics**: Set to 1 to look for systematic trees in signal workspace. Set to 0 to not generate a systematics dat file.
  * **inputWSDir**: Input workspace directory. This should contain all signal files you'd like to run over. For example, this could contain all resonant mass points. 
  * **useprocs**: Use production modes. For HHWWgg, this needs to be set to look for certain processes, as this needs to correspond to the file names. For example, to run on Spin-0 or Spin-2 resonant files, you would set this to ggF. To run on NMSSM, this should be set to GluGluToHHTo. Again, the point is this corresponds to the input file naming convention. 
  * **cats**: Categories. Same definition as Background instructions. These are the categories that will be looked for in the signal workspaces. 
  * **ext**: Extension. Same definition as Background instructions. This should be the same as the extension used for the background model you want to combine with your signal models. 
  * **analysis**: Set to HHWWgg to configure for HHWWgg file naming conventions.
  * **analysis_type**: Used for HHWWgg. Set to either EFT, Res or NMSSM. Used to configure the names of the workspaces, used for easily looping over mass points, mass pairs or benchmarks. 
  * **FinalState**: The HHWWgg final state. For now the options are: qqlnu, lnulnu or qqqq, corresponding to the Semi-Leptonic, Fully-Leptonic, and Fully-Hadronic final states. The FinalState you enter here will be looked for in file and RooDataSet names. This is meant to be used if you are running on HHWWgg signal files for a given final state. When we run our tagger on a signal final containing all final states, a "combined" option will be added here.
  * **year**: Data taking year. 
  * **scales, scalesCorr, scalesGlobal, smears**: Systematic trees to look for in signal workspaces. 
  * **batch and queue**: Set to empty strings as HHWWgg only configured to run locally. 
  * **mode**: Function to run on signal. To run with systematics, set to "std" and run HHWWggFinalFitScript.sh twice. To run without systematics, run the following steps in order: std, sigFitOnly, packageOnly, sigPlotsOnly 

After setting the parameters properly, you are ready to run the signal fit steps. 

To run with systematics, you should set the mode to "std", make sure the correct configuration file name is specified in HHWWggFinalFitScript for the signal step, and then run the command 

```bash
. HHWWggFinalFitScript.sh signal
```

This should run the fTest step, providing the recommended number of gaussians to use to fit each signal category. If this runs properly, you should find a directory Signal/outdir_<entension>_<signalPoint>_<Process>. In this directory you should find sigfTest containing the gaussian sum f-test fits for rv (right vertex) and wv (wrong vertex) for each category.

To continue with the signal fitting, run the same command: `. HHWWggFinalFitScript.sh signal`. If this runs properly, you should see many new folders added to the Signal/outdir directory. 

**NOTE**: If you want to run the fTest again then you have to delete the `dat` directory which is present inside the `Signal` directory.

```bash
# to re-run the fTest
rm -rf Signal/dat
```

## Datacard 

The next step is to create the datacard containing information from the Background and Signal workspaces to be used by combine. An example configuration file used for this step is `HHWWgg_Synch_Combine_Config.py`. Most if not all of the parameters here are previously explained in either the Signal or Background sections. The main thing to remember is that the extension needs to stay consistent here. As long as the parameters are set properly, and the datacard step of HHWWggFinalFitScript.sh is looking for the proper configuration file, you should now run: 

```bash
. HHWWggFinalFitScript.sh datacard
```

If it works properly, this should create a directory Datacard/<extension>, containing the datacard. Note that the datacard ending with "\_cleaned.txt" is the one used in the combine step.



## Combine

If you are satisfied with the datacard, you can now run combine with: 

```bash
. HHWWggFinalFitScript.sh combine  
```

If this works properly, the background and signal models will be used to compute the upper limit of the signal process. Note that if a branching ratio was not defined in the signal model steps (for HHWWgg, it is currently not) then this result will be the quantile values of the upper limit of cross section (production->HH->WWgg->finalstate). In order to obtain the upper limit on WWgg you need to divide by the branching ratio of the final state * 2 because either W can decay into this, and then divide by the branching ratio of HH->WWgg * 2 because either H can decay to WW or gg. For the moment, these computations are done in Plots/FinalResults/plot_limits.py


## Plot

```bash
. HHWWggFinalFitScript.sh plot
```

# Known Issues

## While running the signal model

Also, while running the signal model there is some memory leak issue because of which we get the error as shown below. Again, this is not affecting our taks. So, temporarily we can live with this.
```bash
finished mass shift:  5
*** Error in `python': free(): invalid pointer: 0x000000000721a71c ***
======= Backtrace: =========
/lib64/libc.so.6(+0x81299)[0x7f233b40a299]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libRooFitCore.so(_ZN13RooLinkedList6DeleteEPKc+0x23)[0x7f232cee7c23]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libRooFitCore.so(_ZN12RooWorkspaceD1Ev+0x39)[0x7f232cfa8a59]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libRooFitCore.so(_ZN12RooWorkspaceD0Ev+0x9)[0x7f232cfa8be9]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/external/slc7_amd64_gcc700/lib/libCore.so(_ZN6TClass10DestructorEPvb+0x35)[0x7f233a99c8b5]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libPyROOT.so(_ZN6PyROOT17op_dealloc_nofreeEPNS_11ObjectProxyE+0xe7)[0x7f233b2f63c7]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libPyROOT.so(+0x67509)[0x7f233b2f6509]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/external/slc7_amd64_gcc700/lib/libpython2.7.so.1.0(+0xbd518)[0x7f233c139518]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/external/slc7_amd64_gcc700/lib/libpython2.7.so.1.0(+0x9b942)[0x7f233c117942]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/external/slc7_amd64_gcc700/lib/libpython2.7.so.1.0(PyDict_SetItem+0x7e)[0x7f233c11a7ae]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/external/slc7_amd64_gcc700/lib/libpython2.7.so.1.0(_PyModule_Clear+0x12b)[0x7f233c11f5bb]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/external/slc7_amd64_gcc700/lib/libpython2.7.so.1.0(PyImport_Cleanup+0x41b)[0x7f233c19d4db]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/external/slc7_amd64_gcc700/lib/libpython2.7.so.1.0(Py_Finalize+0x101)[0x7f233c1af731]
/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/external/slc7_amd64_gcc700/lib/libpython2.7.so.1.0(Py_Main+0x537)[0x7f233c1c82e7]
/lib64/libc.so.6(__libc_start_main+0xf5)[0x7f233b3ab555]
python[0x40066e]
======= Memory map: ========
00400000-00401000 r-xp 00000000 00:32 528473                             /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/python/2.7.14-omkpbe4/bin/python2.7
00401000-00402000 r--p 00000000 00:32 528473                             /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/python/2.7.14-omkpbe4/bin/python2.7
00402000-00403000 rw-p 00001000 00:32 528473                             /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/python/2.7.14-omkpbe4/bin/python2.7
01563000-0904d000 rw-p 00000000 00:00 0                                  [heap]
7f2324000000-7f2324021000 rw-p 00000000 00:00 0 
7f2324021000-7f2328000000 ---p 00000000 00:00 0 
7f232b47b000-7f232bb7d000 rw-p 00000000 00:00 0 
7f232bc0e000-7f232bc25000 r-xp 00000000 fc:01 6376382                    /usr/lib64/libnsl-2.17.so
7f232bc25000-7f232be24000 ---p 00017000 fc:01 6376382                    /usr/lib64/libnsl-2.17.so
7f232be24000-7f232be25000 r--p 00016000 fc:01 6376382                    /usr/lib64/libnsl-2.17.so
7f232be25000-7f232be26000 rw-p 00017000 fc:01 6376382                    /usr/lib64/libnsl-2.17.so
7f232be26000-7f232be28000 rw-p 00000000 00:00 0 
7f232be59000-7f232beec000 r-xp 00000000 00:32 436837                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/lib/slc7_amd64_gcc700/libDataFormatsStdDictionaries.so
7f232beec000-7f232beed000 ---p 00093000 00:32 436837                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/lib/slc7_amd64_gcc700/libDataFormatsStdDictionaries.so
7f232beed000-7f232bef1000 r--p 00093000 00:32 436837                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/lib/slc7_amd64_gcc700/libDataFormatsStdDictionaries.so
7f232bef1000-7f232bef2000 rw-p 00097000 00:32 436837                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_13/lib/slc7_amd64_gcc700/libDataFormatsStdDictionaries.so
7f232bef2000-7f232beff000 rw-p 00000000 00:00 0 
7f232c026000-7f232c140000 r-xp 00000000 00:32 343441                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libGpad.so
7f232c140000-7f232c141000 ---p 0011a000 00:32 343441                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libGpad.so
7f232c141000-7f232c14c000 r--p 0011a000 00:32 343441                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libGpad.so
7f232c14c000-7f232c14e000 rw-p 00125000 00:32 343441                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libGpad.so
7f232c14e000-7f232c154000 rw-p 00000000 00:00 0 
7f232c154000-7f232c1e9000 r-xp 00000000 00:32 343436                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libGraf3d.so
7f232c1e9000-7f232c1f3000 r--p 00094000 00:32 343436                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libGraf3d.so
7f232c1f3000-7f232c1f5000 rw-p 0009e000 00:32 343436                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libGraf3d.so
7f232c1f5000-7f232c1f9000 rw-p 00000000 00:00 0 
7f232c1f9000-7f232c399000 r-xp 00000000 00:32 343247                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libTreePlayer.so
7f232c399000-7f232c39a000 ---p 001a0000 00:32 343247                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libTreePlayer.so
7f232c39a000-7f232c3a5000 r--p 001a0000 00:32 343247                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libTreePlayer.so
7f232c3a5000-7f232c3a8000 rw-p 001ab000 00:32 343247                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/lcg/root/6.12.07-gnimlf5/lib/libTreePlayer.so
7f232c3a8000-7f232c3f0000 rw-p 00000000 00:00 0 
7f232c3f0000-7f232c480000 r-xp 00000000 00:32 611814                     /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/freetype/2.5.3-omkpbe2/lib/libfreetype.so.6.11.2./runSignalScripts.sh: line 389:  9208 Aborted                 (core dumped) python DirecShiftHiggsDatasets.py $fileDir $ID $HHWWggLabel $CATS $ANALYSIS_TYPE $proc $FINALSTATE
ANALYSIS: HHWWgg
```

