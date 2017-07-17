
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
rawdir = signal_rawdir
data_rawdir = "/data/uclhc/uci/user/dantrim/ntuples/n0232/d_jan30/data/Raw/"
filelist_dir = "/data/uclhc/uci/user/dantrim/n0232val/filelists/"
backgrounds = []

#### MC
lumi_ = {}
lumi_[36.0] = 100.0

lumi_val = 36.0

# ttbro
ttbar = background.Background("ttbar", "t#bar{t}")
ttbar.set_debug()
ttbar.scale_factor = lumi_[lumi_val]
ttbar.set_fillStyle(0)
ttbar.setLineStyle(1)
ttbar.set_color(r.TColor.GetColor("#e4706a"))
ttbar.set_treename("ttbar_powheg")
ttbar.set_chain_from_list_CONDOR(filelist_dir+ "ttbar/", rawdir)
backgrounds.append(ttbar)

wt = background.Background("stWt", "Wt")
wt.set_debug()
wt.scale_factor = lumi_[lumi_val]
wt.set_fillStyle(0)
wt.setLineStyle(1)
wt.set_color(r.TColor.GetColor("#db101c"))
wt.set_treename("STWT")
wt.set_chain_from_list_CONDOR(filelist_dir + "Wt/", rawdir)
backgrounds.append(wt)

ztt = background.Background("ztt", "Z+jets (tt)")
ztt.set_debug()
ztt.scale_factor = lumi_[lumi_val]
ztt.set_fillStyle(0)
ztt.setLineStyle(1)
ztt.set_color(r.TColor.GetColor("ece1b6"))
ztt.set_treename("ztt")
ztt.set_chain_from_list_CONDOR(filelist_dir + "zjets_sherpa_tt/", rawdir)
backgrounds.append(ztt)



mx_list = []
lines = open("dihiggs_signal_list.txt").readlines()
for iline, line in enumerate(lines[1:]) :
    if not line : continue
    line = line.strip()

    line = line.split()
    dsid = line[0]
    mx = line[1]
    mx_list.append(int(mx))

    funny = "hh_%s"%mx
    notfunny = "X %s"%mx
    name = "sig%d"%iline
    

    s = background.Background(funny, notfunny)
    s.setSignal()
    s.set_debug()
    s.scale_factor = lumi_[lumi_val]
    s.set_treename(name)
    s.set_chain_from_list_CONDOR(filelist_dir+ "wwbb_susy2/", signal_rawdir, dsid)
    #backgrounds.append(s)

#############################################
# Set up the regions
#############################################
regions = []

isEE = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && mll>20 && abs(mll-91.2)>10."
isMM = "nLeptons==2 && nMuons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && mll>20 && abs(mll-91.2)>10."
isEM = "nLeptons==2 && nElectrons==1 && nMuons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && mll>20"
isALL = "( ( %s ) || ( %s ) || ( %s ) )"%(isEE, isMM, isEM)
trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"

def mt1_window(xmass) :
    lower = 0.9*xmass
    upper = 1.08*xmass
    #originalupper = 1.1*xmass
    cut = "MT_1_scaled > %d && MT_1_scaled < %d"%(lower, upper)
    return cut

for mxval in mx_list :
    if mxval > 3000 : continue
    #reg = region.Region()
    #reg.name = "WWBBOPTEE_%d"%mxval
    #reg.displayname = "WWBBOPTEE_%d"%mxval
    #presel = " ( %s ) && %s "%(isEE, trigger)
    #cut = presel
    #cut += " && dRll<0.9"
    #cut += " && mt2_llbb_vec[0]>90 && mt2_llbb_vec[0]<140"
    #cut += " && mbb_vec[0]>90 && mbb_vec[0]<140"
    #cut += " && HT2Ratio_vec[0]>0.8"
    #cut += " && %s"%(mt1_window(mxval))
    #reg.tcut = cut
    #regions.append(reg)
    #
    #reg = region.Region()
    #reg.name = "WWBBOPTMM_%d"%mxval
    #reg.displayname = "WWBBOPTMM_%d"%mxval
    #presel = " ( %s ) && %s "%(isMM, trigger)
    #cut = presel
    #cut += " && dRll<0.9"
    #cut += " && mt2_llbb_vec[0]>90 && mt2_llbb_vec[0]<140"
    #cut += " && mbb_vec[0]>90 && mbb_vec[0]<140"
    #cut += " && HT2Ratio_vec[0]>0.8"
    #cut += " && %s"%(mt1_window(mxval))
    #reg.tcut = cut
    #regions.append(reg)
    #
    #reg = region.Region()
    #reg.name = "WWBBOPTEM_%d"%mxval
    #reg.displayname = "WWBBOPTEM_%d"%mxval
    #presel = " ( %s ) && %s "%(isEM, trigger)
    #cut = presel
    #cut += " && dRll<0.9"
    #cut += " && mt2_llbb_vec[0]>90 && mt2_llbb_vec[0]<140"
    #cut += " && mbb_vec[0]>90 && mbb_vec[0]<140"
    #cut += " && HT2Ratio_vec[0]>0.8"
    #cut += " && %s"%(mt1_window(mxval))
    #reg.tcut = cut
    #regions.append(reg)
    
    reg = region.Region()
    reg.name = "WWBBOPTALL_%d"%mxval
    reg.displayname = "WWBBOPTALL_%d"%mxval
    presel = " %s && %s "%(isALL, trigger)
    cut = presel
    #originalcut += " && nBJets>=2"
    #originalcut += " && dRll<0.9"
    #originalcut += " && mt2_llbb_vec[0]>90 && mt2_llbb_vec[0]<140"
    #originalcut += " && mbb_vec[0]>90 && mbb_vec[0]<140"
    #originalcut += " && HT2Ratio_vec[0]>0.8"
    #originalcut += " && %s"%(mt1_window(mxval))
    cut += " && nBJets>=2"
    cut += " && dRll<0.9"
    cut += " && mt2_llbb_vec[0]>90 && mt2_llbb_vec[0]<140"
    cut += " && mbb_vec[0]>100 && mbb_vec[0]<140"
    cut += " && HT2Ratio_vec[0]>0.8"
    cut += " && %s"%(mt1_window(mxval))
    reg.tcut = cut
    regions.append(reg)


