# Hold defs of writing functions for datacard
import os, sys, re

def writePreamble(f,options):
  f.write("CMS HGG Datacard - %s - 13TeV\n"%(options.years)) 
  f.write("Auto-generated by flashggFinalFits/Datacard/makeDatacard.py\n")
  f.write("Run with: combine\n")
  f.write("---------------------------------------------\n")
  f.write("imax *\n")
  f.write("jmax *\n")
  f.write("kmax *\n")
  f.write("---------------------------------------------\n")
  return True

def writeProcesses(f,d,options):
  f.write("\n")
  # If opt.prune then remove all rows from dataFrame with prune=1
  d = d[d['prune']==0]
  # d = Pandas DataFrame
  # Shapes
  # Loop over categories in dataframe
  # print'd:'d
  for cat in d.cat.unique():
    # Loop over rows for respective category
    for ir,r in d[d['cat']==cat].iterrows():
      # Write to datacard
      # print'r:',r
      
      if(options.analysis=="HHWWgg"): 
        # print' r["type"]:',r['type']
        model = r['model']
        if r['type']=='sig': 
          # print'r["modelWSFile"]:',r['model']
          yr = r['year']
          model = model.replace('hggpdfsmrel_13TeV','hggpdfsmrel_%s_13TeV'%yr) # HHWWgg fix for running 2017 only
        if r['type']=='data' or r['type']=='bkg':
          yr = r['year']
          # model = model.replace('_%s_'%yr,'_') # HHWWgg fix for running 2017 only

        yr = r['year']
        thiscat = r['cat']
        # thiscat.replace('%s'%yr,'13TeV')
        f.write("shapes      %-55s %-40s %s %s\n"%(r['proc'],thiscat,r['modelWSFile'],model))
      else: 
        f.write("shapes      %-55s %-40s %s %s\n"%(r['proc'],r['cat'],r['modelWSFile'],r['model']))

  # Bin, observation and rate lines
  lbreak = '----------------------------------------------------------------------------------------------------------------------------------'
  lbin_cat = '%-30s'%"bin"
  lobs_cat = '%-30s'%"observation"
  lbin_procXcat = '%-30s'%"bin"
  lproc = '%-30s'%"process"
  lprocid = '%-30s'%"process"
  lrate = '%-30s'%"rate"     
  yr = r['year']   
  # yr='2017'
  # Loop over categories
  for cat in d.cat.unique():
    # if(options.analysis=="HHWWgg"):
      # cat.replace('_%s'%yr,'_13TeV')
      # print'cat:',cat 
    lbin_cat += "%-55s "%cat
    lobs_cat += "%-55s "%"-1"
    sigID = 0
    # Loop over rows for respective category
    for ir,r in d[d['cat']==cat].iterrows():
      if r['proc'] == "data_obs": continue
      lbin_procXcat += "%-55s "%cat
      lproc += "%-55s "%r['proc']
      if r['proc'] == "bkg_mass": lprocid += "%-55s "%"1"
      else:
        lprocid += "%-55s "%sigID
        sigID -= 1
      lrate += "%-55.1f "%r['rate']
  #Remove final space from lines and add to file
  f.write("\n")
  for l in [lbreak,lbin_cat,lobs_cat,lbreak,lbin_procXcat,lproc,lprocid,lrate,lbreak]: 
    l = l[:-1]
    f.write("%s\n"%l)
    
  f.write("\n")
  return True


def writeSystematic(f,d,s,options,stxsMergeScheme=None):

  # For signal shape systematics add simple line
  if s['type'] == 'signal_shape':
    lsyst = "%-50s  param    %-6s %-6s"%(s['title'],s['mean'],s['sigma'])
    f.write("%s\n"%lsyst)
    return True
 
  # Else: for yield variation uncertainties...
  # Remove all rows from dataFrame with prune=1 (includes NoTag)
  mask = (d['prune']==0)
  d = d[mask]

  # If theory: loop over tiers else run over once
  tiers = []
  if 'tiers' in s: tiers = s['tiers']
  if(not options.doSTXSBinMerging)&('mnorm' in tiers): tiers.remove("mnorm")
  if len(tiers)==0: tiers = ['']
  for tier in tiers:
    if tier != '': tierStr = "_%s"%tier
    else: tierStr = ''
    
    # If calculating merged bin: loop over mergings else run over once
    mns = []
    if tier == 'mnorm':
      if options.doSTXSBinMerging:
        for mergeName in stxsMergeScheme: mns.append(mergeName)
    if len(mns) == 0: mns.append('')
    for mn in mns:
      if mn != '': mergeStr = "_%s"%mn
      else: mergeStr = ''
    
      # Construct syst line/lines if separate by year
      if s['correlateAcrossYears'] == 1:
	stitle = "%s%s%s"%(s['title'],mergeStr,tierStr)
	lsyst = '%-50s  %-10s    '%(stitle,s['prior'])
	# Loop over categories and then iterate over rows in category
	for cat in d.cat.unique():
	  for ir,r in d[d['cat']==cat].iterrows():
	    if r['proc'] == "data_obs": continue
	    # Extract value and add to line (with checks)
	    sval = r["%s%s%s"%(s['name'],mergeStr,tierStr)]
	    lsyst = addSyst(lsyst,sval,stitle,r['proc'],cat)
	# Remove final space from line and add to file
	f.write("%s\n"%lsyst[:-1])
      else:
	for year in options.years.split(","):
	  stitle = "%s%s%s_%s"%(s['title'],mergeStr,tierStr,year)
	  sname = "%s%s%s_%s"%(s['name'],mergeStr,tierStr,year)
	  lsyst = '%-50s  %-10s    '%(stitle,s['prior'])
	  # Loop over categories and then iterate over rows in category
	  for cat in d.cat.unique():
	    for ir,r in d[d['cat']==cat].iterrows():
	      if r['proc'] == "data_obs": continue
	      # Extract value and add to line (with checks)
	      sval = r[sname]
	      lsyst = addSyst(lsyst,sval,stitle,r['proc'],cat)
	  # Remove final space from line and add to file
	  f.write("%s\n"%lsyst[:-1])
  return True
          

def addSyst(l,v,s,p,c):
  #l-systematic line, v-value, s-systematic title, p-proc, c-cat
  if type(v) is str: 
    l += "%-15s "%v
    return l
  elif type(v) is list: 
    # Symmetric:
    if len(v) == 1: 
      # Check 1: variation is non-negligible. If not then skip
      if abs(v[0]-1)<0.0005: l += "%-15s "%"-"
      # Check 2: variation is not negative. Print message and add - to datacard (cleaned later)
      elif v[0] < 0.: 
        print " --> [WARNING] systematic %s: negative variation for (%s,%s)"%(s,p,c)
        #vstr = "%s"%v[0]
        vstr = "-"
        l += "%-15s "%v[0]
      else:
        l += "%-15.3f "%v[0]
    # Anti-symmetirc
    if len(v) == 2:
      # Check 1: variation is non-negligible. If not then skip
      if(abs(v[0]-1)<0.0005)&(abs(v[1]-1)<0.0005): l += "%-15s "%"-"
      # Check 2: neither variation is negative. Print message and add - to datacard (cleaned later)
      elif(v[0]<0.)|(v[1]<0.):
        print " --> [WARNING] systematic %s: negative variation for (%s,%s)"%(s,p,c)
        #vstr = "%.3f/%.3f"%(v[0],v[1])
        vstr = "-"
        l += "%-15s "%vstr
      # Check 3: effect is approximately symmetric: then just add single up variation
      elif( abs((v[0]*v[1])-1)<0.0005 ): l += "%-15.3f "%v[1]
      else: 
        vstr = "%.3f/%.3f"%(v[0],v[1])
        l += "%-15s "%vstr
    return l
  else:
    print " --> [ERROR] systematic %s: value does not have type string or list for (%s,%s). Leaving..."%(s['title'],p,c)
    sys.exit(1)

def writePdfIndex(f,d,options):
  f.write("\n")
  for cat in d[~d['cat'].str.contains("NOTAG")].cat.unique(): 
    indexStr = "pdfindex_%s_13TeV"%cat
    # print'indexStr:',indexStr
    # if(options.analysis=="HHWWgg"): 
      # print'replace'
      # indexStr = indexStr.replace("_2016_","_")
      # indexStr = indexStr.replace("_2017_","_")
      # indexStr = indexStr.replace("_2018_","_")
    # print'indexStr:',indexStr
    # else: indexStr = "pdfindex_%s_13TeV"%cat
      # yr = r['year']
      # yr='2017'
      # indexStr.replace('_%s_'%yr,'_')
    
    # print'indexStr:',indexStr
    f.write("%-55s  discrete\n"%indexStr)
  return True

def writeBreak(f):
  lbreak = '----------------------------------------------------------------------------------------------------------------------------------'
  f.write("%s\n"%lbreak)

