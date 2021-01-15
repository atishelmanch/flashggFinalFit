#!/usr/bin/env bash
node="cHHH0"
procs='GluGluToHHTo2G2l2nu'
year='2017'
cat='HHWWggTag_2'
path=`pwd`
cmsenv
source ./setup.sh
############################################
# Tree selectors#
cd ./Reweight/
sed -i "s#cHHH1#${node}#g" Selections.C
# root -b -q Selections.C
sed -i "s#${node}#cHHH1#g" Selections.C
mv GluGluToHHTo*.root  ../Trees2WS/
cd ../Trees2WS/


#########################################
# start tree to workspace
# python trees2ws.py --inputConfig HHWWgg_config.py --inputTreeFile ./${procs}_node_${node}_2017_applied_selections.root --inputMass node_${node} --productionMode ${procs}  --year ${year} --doSystematics
mkdir ../Signal/Input

mv ws_${procs}/GluGluToHHTo2G2l2nu_node_${node}_${year}_applied_selections_${procs}.root ../Signal/Input/output_M125_${procs}_node_${node}_${cat}.root 

#########################################
#shift dataset
cd ../Signal/
python ./scripts/shiftHiggsDatasets_test.py --inputDir ./Input/ --procs ${procs} --cats ${cat} --HHWWggLabel node_${node}



#######################################
# Run ftest
sed -i "s#cHHH2p45#${node}#g" HHWWgg_config_test_2017.py 
sed -i "s#INPUTDIR#${path}/Signal/Input/#g" HHWWgg_config_test_2017.py
python RunSignalScripts.py --inputConfig HHWWgg_config_test_2017.py --mode fTest --modeOpts "doPlots"
python RunSignalScripts.py --inputConfig HHWWgg_config_test_2017.py --mode calcPhotonSyst


python RunSignalScripts.py --inputConfig HHWWgg_config_test_2017.py --mode signalFit --groupSignalFitJobsByCat





sed -i "s#${path}/Signal/Input/#INPUTDIR#g" HHWWgg_config_test_2017.py
sed -i "s#${node}#cHHH2p45#g" HHWWgg_config_test_2017.py 
