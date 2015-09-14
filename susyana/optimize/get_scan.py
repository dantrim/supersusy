#!/usr/bin/env python

from tabulate import tabulate
from math import sqrt
import os
import sys
sys.path.append(os.environ['SUSYDIR'])

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(False)

r.TCanvas.__init__._creates = False
r.TH1F.__init__._creates = False
r.TGraph2D.__init__._creates = False


regions = ['ttbar', 'st', 'ww', 'wz', 'bwn250_160']


class BkgCount :
    def __init__(self, name) :
        self.name = name
        self.tot_yield = 0.0
        self.tot_error = 0.0

class RegionYield :
    def __init__(self, scan_init="", scan_fin="") :
        self.init = scan_init
        self.fin  = scan_fin 

        self.bkgyields = []

        self.tot_yield = 0.0
        self.tot_error = 0.0

        self.significance = 0.0

        self.s_over_b = 0.0

if __name__=="__main__" :
    print "Scan over X and Y :"
    print "\tnLeptons==2 && nMuons==1 && nElectrons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && mt2>80 && R2>0.65 && DPB>(X*abs(cosThetaB) + Y)"
    filename = "dpb_cos_fasimov_scan.log"
    lines= open(filename).readlines()
    bkg_counts = []
    reg_yields = []
    for iline, line in enumerate(lines) :
        if "scan:" in line :
            line = line.strip()
            scan = line.split()
            reg_yield = RegionYield(scan[1], scan[2])
            ttbar_line = lines[iline+3]
            st_line    = lines[iline+4]
            ww_line    = lines[iline+5]
            wz_line    = lines[iline+6]
            susy_line  = lines[iline+7]

            ttbar = BkgCount('ttbar')
            st    = BkgCount('st')
            ww    = BkgCount('ww')
            wz    = BkgCount('wz')
            susy  = BkgCount('(250,160)')


            ttbar.tot_yield = ttbar_line.split()[1]
            ttbar.tot_error = ttbar_line.split()[3]
            reg_yield.bkgyields.append(ttbar)

            st.tot_yield = st_line.split()[1]
            st.tot_error = st_line.split()[3]
            reg_yield.bkgyields.append(st)

            ww.tot_yield = ww_line.split()[1]
            ww.tot_error = ww_line.split()[3]
            reg_yield.bkgyields.append(ww)

            wz.tot_yield = wz_line.split()[1]
            wz.tot_error = wz_line.split()[3]
            reg_yield.bkgyields.append(wz)

            susy.tot_yield = susy_line.split()[1]
            susy.tot_error = susy_line.split()[3]
            reg_yield.bkgyields.append(susy)


            total_bkg_yield_line = lines[iline+13]
            reg_yield.tot_yield = total_bkg_yield_line.split()[3]
            reg_yield.tot_error   = total_bkg_yield_line.split()[5]

            reg_yield.s_over_b = float(susy.tot_yield) / sqrt(float(reg_yield.tot_yield)**2 + float(reg_yield.tot_error)**2)

            signif_line = lines[iline+15]
            reg_yield.significance = signif_line.split()[2]

            reg_yields.append(reg_yield)

    headers = ["(x,y)"]
    for reg in reg_yields[:1] :
        for process in reg.bkgyields :
            headers.append(process.name)
    headers.append("Tot. Exp. Bkg.")
    headers.append("deltaS / S")
    headers.append("deltaB / B")
    headers.append("S/sqrt(B^2 + deltaB^2)")
    headers.append("Significance")

    table = []
    reg_yields = sorted(reg_yields, key=lambda x: x.init)
    for r in reg_yields :
        line = []
        scan_ = "(%s, %s)"%(r.init, r.fin)
        line.append(scan_)
        for process in r.bkgyields :
            process_yield = "%.2f +/- %.2f"%(float(process.tot_yield), float(process.tot_error))
            line.append(process_yield)
        total_region_yield = "%.2f +/- %.2f"%(float(r.tot_yield), float(r.tot_error))
        line.append(total_region_yield)

        sig_error_line = "%2.f %%"%(float(r.bkgyields[-1].tot_error) / float(r.bkgyields[-1].tot_yield) * 100.)
        line.append(sig_error_line)

        frac_error_line = "%2.f %%"%(float(r.tot_error)/(float(r.tot_yield)) * 100.)
        line.append(frac_error_line)


        s_over_b_line = "%.2f"%float(r.s_over_b)
        line.append(s_over_b_line)
        sig_line = "%.2f"%float(r.significance)
        line.append(sig_line)
        table.append(line)

    print tabulate(table, headers, tablefmt="rst", numalign="right", stralign="left")
    

