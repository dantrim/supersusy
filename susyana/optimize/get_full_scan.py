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


import supersusy.utils.plot_utils as pu

r.TCanvas.__init__._creates = False
r.TH1F.__init__._creates = False
r.TGraph2D.__init__._creates = False
r.TLatex.__init__._creates = False



scan_map = {} # { # : [ mt2, r2, x, y ] }

class BkgCount :
    def __init__(self, name) :
        self.name = name
        self.tot_yield = 0.0
        self.tot_error = 0.0

class RegionYield :
    def __init__(self, region_number = 0) :
        self.number = region_number
        
        self.bkgyields = []

        self.tot_yield = 0.0
        self.tot_error = 0.0

        self.rel_error = 0.0

        self.significance = 0.0

        self.s_over_b = 0.0

if __name__=="__main__" :

    print "Scan over A, B, X, and Y"
    print "\tnLeptons==2 && nMuons==1 && nElectrons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && nBJets==0 && mt2 > A && R2 > B && DPB>(X*abs(cosThetaB) + Y)"

    filename = "mt2_r2_x_y_zn_scan.log"
    lines = open(filename).readlines()
    bkg_counts = []
    region_yields = []
    for iline, line in enumerate(lines) :
        if "scan:" in line :

            # get the region ID number
            region_ = int(lines[iline+1].split()[2])

            scan_map[region_] = {}
            line = line.strip()

            # get the information on the cuts for this scan point
            # store the relevant information in the scan_map
            scan_ = line.split()
            scan_ = scan_[1:]
            for var in scan_ :
                v = var.split("=")
                scan_map[region_][v[0]] = v[1]

            ######################################            
            # get the yield object
            region_yield = RegionYield(region_)

            # total bkg yield for the region
            bkg_yld_line = lines[iline+14].split()
            region_yield.tot_yield = bkg_yld_line[3]
            region_yield.tot_error = bkg_yld_line[5]
            region_yield.rel_error = float(region_yield.tot_error) / float(region_yield.tot_yield)

            # s over b
            # total signal
            total_sig_line = lines[iline+8].split()
            total_signal = total_sig_line[1]
            deltaS = total_sig_line[3]

            region_yield.s_over_b = float(total_signal) / sqrt( float(region_yield.tot_yield)**2 + float(region_yield.tot_error)**2) 


            # significance for this region
            significance_line = lines[iline+16].split()
            region_yield.significance = float(significance_line[2])

            ######################################
            # get the process yields

            # ttbar
            ttbar = BkgCount("ttbar")
            proc_line = lines[iline+4]
            ttbar.tot_yield = proc_line.split()[1]
            ttbar.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(ttbar)

            # single-top
            st    = BkgCount("st")
            proc_line = lines[iline+5]
            st.tot_yield = proc_line.split()[1]
            st.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(st)

            # ww
            ww    = BkgCount("ww")
            proc_line = lines[iline+6]
            ww.tot_yield = proc_line.split()[1]
            ww.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(ww)

            # wz
            wz    = BkgCount("wz")
            proc_line = lines[iline+7]
            wz.tot_yield = proc_line.split()[1]
            wz.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(wz)

            # signal
            susy  = BkgCount("(250,160)")
            proc_line = lines[iline+8]
            susy.tot_yield = proc_line.split()[1]
            susy.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(susy)

            ######################################
            # store this regions information
            region_yields.append(region_yield)


    ## get the fasimov #'s
    filename = "mt2_r2_x_y_fasimov_scan.log"
    lines = open(filename).readlines()
    bkg_counts_fas = []
    region_yields_fas = []
    for iline, line in enumerate(lines) :
        if "scan:" in line :

            # get the region ID number
            region_ = int(lines[iline+1].split()[2])

            line = line.strip()


            ######################################            
            # get the yield object
            region_yield = RegionYield(region_)

            # total bkg yield for the region
            bkg_yld_line = lines[iline+14].split()
            region_yield.tot_yield = bkg_yld_line[3]
            region_yield.tot_error = bkg_yld_line[5]
            region_yield.rel_error = float(region_yield.tot_error) / float(region_yield.tot_yield)

            # s over b
            # total signal
            total_sig_line = lines[iline+8].split()
            total_signal = total_sig_line[1]
            deltaS = total_sig_line[3]

            region_yield.s_over_b = float(total_signal) / sqrt( float(region_yield.tot_yield)**2 + float(region_yield.tot_error)**2) 


            # significance for this region
            significance_line = lines[iline+16].split()
            region_yield.significance = float(significance_line[2])

            ######################################
            # get the process yields

            # ttbar
            ttbar = BkgCount("ttbar")
            proc_line = lines[iline+4]
            ttbar.tot_yield = proc_line.split()[1]
            ttbar.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(ttbar)

            # single-top
            st    = BkgCount("st")
            proc_line = lines[iline+5]
            st.tot_yield = proc_line.split()[1]
            st.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(st)

            # ww
            ww    = BkgCount("ww")
            proc_line = lines[iline+6]
            ww.tot_yield = proc_line.split()[1]
            ww.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(ww)

            # wz
            wz    = BkgCount("wz")
            proc_line = lines[iline+7]
            wz.tot_yield = proc_line.split()[1]
            wz.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(wz)

            # signal
            susy  = BkgCount("(250,160)")
            proc_line = lines[iline+8]
            susy.tot_yield = proc_line.split()[1]
            susy.tot_error = proc_line.split()[3]
            region_yield.bkgyields.append(susy)

            ######################################
            # store this regions information
            region_yields_fas.append(region_yield)

    region_yields_fas = sorted(region_yields_fas, key = lambda x: int(x.number))

    ##############################################
    ## make tables

    # header line
    headers = ['region ID']
    headers.append('scan point')
    for region in region_yields[:1] :
        for process in region.bkgyields :
            headers.append(process.name)
    headers.append("Total SM")
    headers.append("deltaB/B (%%)")
    headers.append("S/sqrt(B^2 + deltaB^2)")
    headers.append("Significance (Zn)") 

    # rows
    table = []
    region_yields = sorted(region_yields, key = lambda x: int(x.number))
    for iregion, region in enumerate(region_yields) :
        line = [iregion]

        id_tag = "(%s,%s,%s,%s)"%(scan_map[iregion]['r2'], scan_map[iregion]['mt2'], scan_map[iregion]['x'], scan_map[iregion]['y'])
        line.append(id_tag)

        ## add the bkg-process yields
        for process in region.bkgyields :
            process_yield = "%.2f +/- %.2f"%(float(process.tot_yield), float(process.tot_error))
            line.append(process_yield)

        ## add the total SM count
        total_SM = "%.2f +/- %.2f"%(float(region.tot_yield), float(region.tot_error))
        line.append(total_SM)

        ## add the relative error on the total bkg count
        total_SM_err = "%.2f"%(float(region.rel_error) * 100.)
        line.append(total_SM_err)

        ## add the S/B
        s_over_b = "%.2f"%(float(region.s_over_b))
        line.append(s_over_b)

        ## add the significane
        sign = "%.2f"%(float(region.significance))
        line.append(sign)

        ## add the line to the table
        table.append(line)

    print tabulate(table, headers, tablefmt="rst", numalign="right", stralign="left")


#    ##############################################
#    ## make nice plots
#
#    ##
#    ###### plot comparing Zn to FAsimov
#    ##
#
#    #can = pu.basic_canvas(width=600, height=400)
#    can = pu.ratio_canvas("ratio")
#    can.canvas.SetCanvasSize(800, 400)
#    can.canvas.cd()
#
#    # go to the upper pad
#    can.upper_pad.cd()
#
#    frame = pu.th1f("zn_fasimov_comparison", "", 180, 0, 180, "", "")
#    frame.GetXaxis().SetLabelOffset(-999)
#    frame.GetYaxis().SetLabelOffset(-999)
#    frame.Draw("axis")
#    can.canvas.Update()
#
#    # sig histo for Zn
#    h_zn = pu.th1f("zn", "", 180, 0, 180, "", "Significance")
#    h_fas = pu.th1f("fas", "", 180, 0, 180, "", "Significance")
#
#    maxy =  []
#    for region in region_yields :
#        h_zn.SetBinContent(int(region.number)+1, region.significance)
#        h_zn.GetXaxis().SetTitle("Region ID")
#        h_zn.GetXaxis().SetBinLabel(int(region.number)+1,str(region.number))
#        h_zn.GetXaxis().SetLabelSize(0.5 * h_zn.GetXaxis().GetLabelSize())
#        h_zn.GetXaxis().CenterLabels()
#        h_zn.SetFillColor(0)
#        h_zn.SetLineColor(r.TColor.GetColor("#FC0D1B"))
#        h_zn.SetLineWidth(2)
#        maxy.append(h_zn.GetMaximum())
#    for region in region_yields_fas :
#        h_fas.SetBinContent(int(region.number)+1, region.significance)
#        h_fas.SetFillColor(0)
#        h_fas.SetLineColor(r.TColor.GetColor("#41C1FC"))
#        h_fas.SetLineWidth(2)
#        maxy.append(h_fas.GetMaximum())
#
#    maxy_ = 1.2*max(maxy)
#    h_zn.SetMaximum(maxy_)
#    h_fas.SetMaximum(maxy_)
#    h_zn.Draw("hist")
#    h_zn.GetYaxis().SetTitleSize(1.5*h_zn.GetYaxis().GetTitleSize())
#    h_zn.GetYaxis().SetTitleOffset(0.5*h_zn.GetYaxis().GetTitleOffset())
#    h_fas.Draw("hist same")
#    can.canvas.Update()
#
#    # draw a line at the exclusion significance
#    pu.draw_line(0.0, 1.64, 180, 1.64, color=r.kRed,style=2, width=1)
#
#
#    can.canvas.Update()
#
#    # legend
#    leg = pu.default_legend(xl=0.2,yl=0.72,xh=0.47,yh=0.90)
#    leg.AddEntry(h_zn, "ZBinomial", "l")
#    leg.AddEntry(h_fas, "FAsimov", "l")
#    leg.Draw()
#    can.canvas.Update()
#
#    ### move the lower pad
#    can.lower_pad.cd()
#
#    low_frame = frame.Clone("lowerframe")
#    low_frame.GetYaxis().SetNdivisions(5)
#    low_frame.Draw("axis")    
#
#    h_ratio = h_fas.Clone('ratio')
#    h_ratio.Divide(h_zn)
#    h_ratio.SetLineColor(r.kBlue)
#    h_ratio.SetMinimum(1.0)
#    h_ratio.SetMaximum(1.5)
#    h_ratio.GetXaxis().SetLabelFont(42)
#    h_ratio.GetYaxis().SetLabelFont(42)
#    h_ratio.GetXaxis().SetLabelOffset(1.4*h_ratio.GetXaxis().GetLabelOffset())
#    h_ratio.GetXaxis().SetLabelSize(3*h_ratio.GetXaxis().GetLabelSize())
#    h_ratio.GetXaxis().SetTitle("Region ID")
#    h_ratio.GetXaxis().SetTitleOffset(1.3*h_ratio.GetXaxis().GetTitleOffset())
#    h_ratio.GetXaxis().SetTitleSize(3*h_ratio.GetXaxis().GetTitleSize())
#    h_ratio.GetYaxis().SetLabelOffset(1.4*h_ratio.GetYaxis().GetLabelOffset())
#    h_ratio.GetYaxis().SetLabelSize(2.5*h_ratio.GetYaxis().GetLabelSize())
#    h_ratio.GetYaxis().SetTitle("#frac{FAsimov}{ZBinomial}")
#    h_ratio.GetYaxis().SetTitleFont(42)
#    h_ratio.GetYaxis().SetTitleSize(3*h_ratio.GetYaxis().GetTitleSize())
#    h_ratio.GetYaxis().SetTitleOffset(0.3*h_ratio.GetYaxis().GetTitleOffset())
#
#    h_ratio.GetYaxis().SetNdivisions(5)
#    h_ratio.Draw("hist")
#    h_ratio.GetYaxis().SetNdivisions(5)
#    can.canvas.Update()
#
#    can.lower_pad.Draw()
#    
#
#    can.canvas.SaveAs('test.eps')
#
#    
#
#     
#    
