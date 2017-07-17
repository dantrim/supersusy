
#!/bin/env python

import sys
sys.path.append('../../../../../')
import supersusy.utils.plot as plot
import supersusy.utils.signal as signal
import supersusy.utils.background as background
import supersusy.utils.region as region


#############################################
# Set up the samples
#############################################
rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/d_jan30/mc/Raw/"
signal_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/h_jun26/mc/Raw/"
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/d_jan30/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0232val/filelists/"
backgrounds = []

#### MC
lumi_ = {}
lumi_[36.0] = 100.0

lumi_val = 36.0

lines = open("dihiggs_signal_list.txt").readlines()
for iline, line in enumerate(lines[1:]) :
    if not line : continue
    line = line.strip()

    line = line.split()
    dsid = line[0]
    mx = line[1]

    funny = "hh_%s"%mx
    notfunny = "X %s"%mx
    name = "sig%d"%iline
    

    s = background.Background(funny, notfunny)
    s.setSignal()
    s.set_debug()
    s.scale_factor = lumi_[lumi_val]
    s.set_treename(name)
    s.set_chain_from_list_CONDOR(filelist_dir+ "wwbb_susy2/", signal_rawdir, dsid)
    backgrounds.append(s)

#############################################
# Set up the regions
#############################################
regions = []

isEE = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && mll>20 && abs(mll-91.2)>10."
isMM = "nLeptons==2 && nMuons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && mll>20 && abs(mll-91.2)>10."
isEM = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && mll>20"
isALL = "( ( %s ) || ( %s ) || ( %s ) )"%(isEE, isMM, isEM)
trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"

dRll_cut = "0.9"
ht2cut = "0.8"

reg = region.Region()
reg.name = "WWBBOPTEE"
reg.displayname = "WWBBOPTEE"
presel = " ( %s ) && %s "%(isEE, trigger)
cut = presel
cut += " && nBJets>=2"
cut += " && mt2_llbb_vec[0]>90 && mt2_llbb_vec[0]<140"
cut += " && mbb_vec[0]>100 && mbb_vec[0]<140"
cut += " && dRll<%s"%dRll_cut
cut += " && HT2Ratio_vec[0]>%s"%ht2cut
#cut += " && dRll<0.9"
#cut += " && HT2Ratio_vec[0]>0.8"
reg.tcut = cut
regions.append(reg)

reg = region.Region()
reg.name = "WWBBOPTMM"
reg.displayname = "WWBBOPTMM"
presel = " ( %s ) && %s "%(isMM, trigger)
cut = presel
cut += " && nBJets>=2"
cut += " && mt2_llbb_vec[0]>90 && mt2_llbb_vec[0]<140"
cut += " && mbb_vec[0]>100 && mbb_vec[0]<140"
cut += " && dRll<%s"%dRll_cut
cut += " && HT2Ratio_vec[0]>%s"%ht2cut
#cut += " && HT2Ratio_vec[0]>0.8"
#cut += " && dRll<0.9"
reg.tcut = cut
regions.append(reg)

reg = region.Region()
reg.name = "WWBBOPTEM"
reg.displayname = "WWBBOPTEM"
presel = " ( %s ) && %s "%(isEM, trigger)
cut = presel
cut += " && nBJets>=2"
cut += " && mt2_llbb_vec[0]>90 && mt2_llbb_vec[0]<140"
cut += " && mbb_vec[0]>100 && mbb_vec[0]<140"
cut += " && dRll<%s"%dRll_cut
cut += " && HT2Ratio_vec[0]>%s"%ht2cut
#originalcut += " && dRll<0.9"
#originalcut += " && HT2Ratio_vec[0]>0.8"
reg.tcut = cut
regions.append(reg)

reg = region.Region()
reg.name = "WWBBOPTALL"
reg.displayname = "WWBBOPTALL"
presel = " %s && %s "%(isALL, trigger)
cut = presel
cut += " && nBJets>=2"
cut += " && mt2_llbb_vec[0]>90 && mt2_llbb_vec[0]<140"
cut += " && mbb_vec[0]>100 && mbb_vec[0]<140"
cut += " && dRll<%s"%dRll_cut
cut += " && HT2Ratio_vec[0]>%s"%ht2cut
#originalcut += " && dRll<0.9"
#originalcut += " && HT2Ratio_vec[0]>0.8"
reg.tcut = cut
regions.append(reg)


