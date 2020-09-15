#!/bin/bash
#
#########################################################################################
# Abraham Tishelman-Charny                                                              #
# 11 March 2020                                                                         #
#                                                                                       #
# The purpose of this script is to run all fggfinalfit steps for the HHWWgg analysis    #
#                                                                                       #
# Example usage:                                                                        #
# . HHWWggFinalFitScript.sh backgroundftest                                             #
# . HHWWggFinalFitScript.sh signal                                                      #
#########################################################################################

step=$1
year=$2

cmsenv
#-- Background 
if [ $step == "backgroundftest" ]; then 
    cd Background 
    python RunBackgroundScripts.py --inputConfig HHWWgg_Synch_Background_Config.py
    # python RunBackgroundScripts.py --inputConfig HHWWgg_SMqqqq${year}_Config.py
    # python RunBackgroundScripts.py --inputConfig HHWWgg_SM${year}_Config.py
    # python RunBackgroundScripts.py --inputConfig HHWWgg_v2-7_Config.py 
    cd .. 
fi

##-- Not yet configured
# if [ $step == "backgroundplots" ]; then
#     cd Background
#     python RunBackgroundScripts.py bkgPlotsOnly --inputConfig config_HHWWgg_v2-3_2017.py
#     # python RunBackgroundScripts.py bkgPlotsOnly --inputConfig config_HHWWgg_v2-3_2017_2Cats.py
#     cd ..
# fi

#-- Signal
if [ $step == "signal" ]; then
    cd Signal
    python RunSignalScripts.py --inputConfig HHWWgg_Synch_Signal_Config.py # signal models
    # python RunSignalScripts.py --inputConfig HHWWgg_SMqqqq${year}_Config.py # signal models 
    # python RunSignalScripts.py --inputConfig HHWWgg_SM${year}_Config.py # signal models 
    # python RunSignalScripts.py --inputConfig HHWWgg_v2-7_Config.py # signal models 
    cd .. 
fi

#-- Datacards
if [ $step == "datacard" ]; then 
    python RunCombineScripts.py datacard --inputConfig HHWWgg_Synch_Combine_Config.py # Make datacard
    #python RunCombineScripts.py datacard --inputConfig HHWWgg_SMqqqq${year}_Config.py # Make datacard 
    # python RunCombineScripts.py datacard --inputConfig HHWWgg_SM${year}_Config.py # Make datacard 
    # python RunCombineScripts.py datacard --inputConfig HHWWgg_v2-7_Config.py # Make datacard 
fi

#-- Combine 
if [ $step == "combine" ]; then 
    python RunCombineScripts.py combine --inputConfig HHWWgg_Synch_Combine_Config.py # Make datacard
    #python RunCombineScripts.py combine --inputConfig HHWWgg_SMqqqq${year}_Config.py
    # python RunCombineScripts.py combine --inputConfig HHWWgg_SM${year}_Config.py
    # python RunCombineScripts.py combine --inputConfig HHWWgg_SMRun2_Config.py
    # python RunCombineScripts.py combine --inputConfig HHWWgg_v2-7_Config.py 
fi

#-- Plots
if [ $step == "plot" ]; then
    cd Plots/FinalResults/
    tagLabel="2TotCatsbothcombined"
    # SecondTagLabel="2TotCatsbothcombined"
    campaignOne="HHWWgg_v2-6"
    FinalState="qqqq"
    website="/eos/user/r/rasharma/www/doubleHiggs/HHWWgg/fggfinalfit/September15_EFT_WW_AllCuts/"
    # campaignOne="HHWWgg_v2-3"
    # campaignTwo="HHWWgg_v2-6"
    # SecondTagLabel="2TotCatsCOMBINEDWithoutSyst"
    # tagLabel="2TotCatsTag0WithSyst"
    # SecondTagLabel="2TotCatsTag0WithoutSyst"
    # HHWWgg_v2-6_2017_X1000_2TotCatsCOMBINEDWithSyst_HHWWgg_qqlnu.root

    ## qqqq Radion
    # python plot_limits.py -a  --HHWWggCatLabel $tagLabel --website ${website}  --systematics  --campaignOne $campaignOne  --yboost 1 --ymin 0.1 --ymax 1 --unit fb --FinalState ${FinalState} --resultType HH  --ymin 1e1 --ymax 1e6 --campaign HHWWgg_dummy # ratio of all points
    # python plot_limits.py -a  --HHWWggCatLabel $tagLabel --website ${website}  --systematics  --campaignOne $campaignOne  --yboost 1 --ymin 0.1 --ymax 1 --unit fb --FinalState ${FinalState} --resultType WWgg  --ymin 0.1 --ymax 1e2 --campaign HHWWgg_dummy # ratio of all points
    
    ## qqqq Radion: Grid
    # python plot_limits.py -a -g --GridLabels $tagLabel  --resultType HH --unit fb --ymin 0.1 --ymax 1 --yboost 1 --FinalState ${FinalState}  --website ${website}

    # qqqq EFT
    # python plot_limits.py --EFT --HHWWggCatLabel $tagLabel --systematics --campaign $campaignOne --resultType WWgg --unit pb --ymin 0.001 --ymax 1e2 --yboost -0.32  --FinalState ${FinalState} --website ${website} # EFT
    python plot_limits.py --EFT --HHWWggCatLabel $tagLabel --systematics --campaign $campaignOne --resultType HH --unit pb --ymin 0.001 --ymax 1e4 --yboost -0.32  --FinalState ${FinalState} --website ${website} # EFT
    # python plot_limits.py --EFT --HHWWggCatLabel $tagLabel --systematics --campaign $campaignOne --resultType HH --unit pb --ymin 10.0 --ymax 1e4 --yboost -0.32  --FinalState ${FinalState} --website ${website} # EFT
    
    ##- Grid
    # python plot_limits.py -a -g --GridLabels 2TotCatsCOMBINEDWithSyst 2TotCatsCOMBINEDWithoutSyst 2TotCatsTag0WithSyst 2TotCatsTag0WithoutSyst 2TotCatsTag1WithSyst 2TotCatsTag1WithoutSyst 1TotCatWithSyst 1TotCatWithoutSyst
    # python plot_limits.py -a -g --GridLabels 2TotCatsTag0WithoutSyst 2TotCatsTag0WithSyst 2TotCatsTag1WithoutSyst 2TotCatsTag1WithSyst 1TotCatWithoutSyst 1TotCatWithSyst 2TotCatsCOMBINEDWithoutSyst 2TotCatsCOMBINEDWithSyst
    # python plot_limits.py -a -g --GridLabels 2TotCatsTag0WithSyst 2TotCatsTag1WithSyst 1TotCatWithSyst 2TotCatsCOMBINEDWithSyst

    ##- Ratio plots
    # python plot_limits.py -a --HHWWggCatLabel $tagLabel --systematics
    # python plot_limits.py -a --HHWWggCatLabel $SecondTagLabel
    # python plot_limits.py -a -r --HHWWggCatLabel $tagLabel --SecondHHWWggCatLabel $SecondTagLabel --campaignOne $campaignOne --campaignTwo $campaignTwo --yboost 1 --ymin 0.1 --ymax 1 --unit fb --resultType HH --campaign HHWWgg_dummy # ratio of all points

    # python plot_limits.py -SM -r --HHWWggCatLabel $tagLabel --SecondHHWWggCatLabel $SecondTagLabel --campaignOne $campaignOne --yboost 1 --ymin 0.1 --ymax 1 --unit fb --resultType HH --campaign HHWWgg_dummy # ratio of all points
    # python plot_limits.py -a -r --HHWWggCatLabel $tagLabel --SecondHHWWggCatLabel $SecondTagLabel --campaignOne $campaignOne --campaignTwo $campaignTwo --yboost 1 --ymin 0.1 --ymax 1 --unit fb --resultType HH --campaign HHWWgg_dummy # ratio of all points
    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics
    # python plot_limits.py -SM --HHWWggCatLabel $SecondTagLabel
    # python plot_limits.py -SM -r --HHWWggCatLabel $tagLabel --SecondHHWWggCatLabel $SecondTagLabel # ratio of SM

    ##- Comparison plots
    # python plot_limits.py -AC --HHWWggCatLabel  $tagLabel --systematics --campaign HHWWgg_v2-6_2017 --resultType WWgg --unit pb --ymin 1.000001 --ymax 1 --yboost 0.09 # atlas compare
    # python plot_limits.py -CMSC --HHWWggCatLabel  $tagLabel --systematics --campaign HHWWgg_v2-6_2017 --resultType HH --unit fb --ymin 10 --ymax 1e5 --yboost -0.2



    ###used this ####python plot_limits.py -CMSC --HHWWggCatLabel  $tagLabel --systematics --campaign HHWWgg_v2-3_2017 --resultType HH --unit fb --ymin 10 --ymax 1e5 --yboost -0.2


    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-3_2017 --resultType HH --unit fb --ymin 10 --ymax 1e6 --yboost -0.32 # standard model
    # python plot_limits.py --EFT --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-3_2017 --resultType HH --unit pb --ymin 1 --ymax 100 --yboost 0.09 # EFT
    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-3_2017 --resultType HH --unit pb --ymin 1 --ymax 100 --yboost 0.09 # standard model
    # python plot_limits.py --NMSSM --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-4_2017 --resultType HH --unit fb --ymin 10 --ymax 1e6 --yboost 0.075 # standard model
    # python plot_limits.py --NMSSM --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-4_2017 --resultType HH --unit fb --ymin 10 --ymax 1e6 --yboost 0.075 # standard model
    # python plot_limits.py -a -r -SM --HHWWggCatLabel $tagLabel --SecondHHWWggCatLabel $SecondTagLabel --campaignOne $campaignOne --campaignTwo $campaignTwo --yboost 1 --ymin 0.1 --ymax 1 --unit fb --resultType HH --year Run2 # ratio of all points
    
    ##- Comparison plots 
    #python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --year ${year} --campaign $campaignOne --resultType HH --unit pb --ymin 1.001 --ymax 100 --yboost 0.09 # standard model  

    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --campaign $campaignOne --resultType HH --unit fb --ymin 10 --ymax 1e6 --yboost -0.32 # standard model 
    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --year 2016 --campaign $campaignOne --resultType HH --unit pb --ymin 1.001 --ymax 100 --yboost 0.09 # standard model  
    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --year 2017 --campaign $campaignOne --resultType HH --unit pb --ymin 1.001 --ymax 100 --yboost 0.09 # standard model  
    
    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --year Run2 --campaign $campaignOne --resultType HH --unit pb --ymin 1.001 --ymax 100 --yboost 0.09 # standard model  
    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --year Run2 --campaign $campaignOne --resultType HH --unit pb --ymin 1.001 --ymax 100 --yboost 0.09 # standard model  

    python plot_limits.py -CMSC --HHWWggCatLabel  $tagLabel --systematics --campaign $campaignOne --resultType WWgg --unit fb --ymin 1.001 --ymax 700 --yboost 0.09 --year 2017 # atlas compare 
    # python plot_limits.py -AC --HHWWggCatLabel  $tagLabel --systematics --campaign $campaignOne --resultType HH --unit pb --ymin 1.001 --ymax 700 --yboost 0.09 --lumiRescale 2017_2016 # atlas compare 
    # python plot_limits.py -CMSC --HHWWggCatLabel  $tagLabel --systematics --campaign $campaignOne --resultType HH --unit fb --ymin 10 --ymax 1e5 --yboost -0.2
    # python plot_limits.py -CMSC --HHWWggCatLabel  $tagLabel --systematics --campaign $campaignOne --resultType HH --unit fb --ymin 10 --ymax 1e5 --yboost -0.2 --lumiRescale 2017_2016

    # python plot_limits.py --EFT --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-3_2017 --resultType HH --unit fb --ymin 10 --ymax 1e6 --yboost -0.32 # EFT 
    # python plot_limits.py --EFT --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-3_2017 --resultType HH --unit pb --ymin 1 --ymax 100 --yboost 0.09 # EFT 
    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-3_2017 --resultType HH --unit fb --ymin 10 --ymax 1e6 --yboost -0.32 # standard model 
    # python plot_limits.py -SM --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-3_2017 --resultType HH --unit pb --ymin 1 --ymax 100 --yboost 0.09 # standard model     
    # python plot_limits.py --NMSSM --HHWWggCatLabel $tagLabel --systematics --campaign HHWWgg_v2-4_2017 --resultType HH --unit fb --ymin 10 --ymax 1e6 --yboost 0.075 # standard model 
    # NMSSM: 2TotCatsCOMBINEDWithSyst_limits/HHWWgg_v2-4_2017_MX300_MY170_2TotCatsCOMBINEDWithSyst_HHWWgg_qqlnu.root
    # EFT: 2TotCatsCOMBINEDWithSyst_limits/HHWWgg_v2-3_2017_node2_2TotCatsCOMBINEDWithSyst_HHWWgg_qqlnu.root
    cd ../../
fi
