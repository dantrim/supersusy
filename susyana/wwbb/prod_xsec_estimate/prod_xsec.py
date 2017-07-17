#!/usr/bin/env python

from optparse import OptionParser
import sys

import glob
from math import sqrt

from operator import itemgetter

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

class ProdXsec :
    def __init__(self, mass = 0) :
        self.mass = mass
        self.ee = -1.0
        self.mm = -1.0
        self.em = -1.0
        self.all = -1.0


class VisibleSignal :
    def __init__(self, mass = 0) :
        self.mass = mass

        self.n_ee = 0.0
        self.n_mm = 0.0
        self.n_em = 0.0
        self.n_all = 0.0

class Background :
    def __init__(self, mass = 0) :
        self.mass = mass
        self.ee_yield = 0.0
        self.mm_yield = 0.0
        self.em_yield = 0.0
        self.all_yield = 0.0

        self.ee_error = 0.0
        self.mm_error = 0.0
        self.em_error = 0.0
        self.all_error = 0.0

class Efficiency :
    def __init__(self, mass = 0) :
        self.mass = mass
        self.ee_eff = 0.0
        self.mm_eff = 0.0
        self.em_eff = 0.0
        self.all_eff = 0.0

class Acceptance :
    def __init__(self, mass = 0) :
        self.mass = mass

        self.ee = 0.0
        self.mm = 0.0
        self.em = 0.0
        self.all = 0.0

        self.ee_num = 0.0
        self.mm_num = 0.0
        self.em_num = 0.0
        self.all_num = 0.0

        self.ee_den = 0.0
        self.mm_den = 0.0
        self.em_den = 0.0
        self.all_den = 0.0

        self.ee_yield = 0.0
        self.mm_yield = 0.0
        self.em_yield = 0.0
        self.all_yield = 0.0

    def yield_at_lumi(self, ch, lumi = 100.) :
        lumi = (lumi / 100.)
        if ch.lower() == "ee" :
            return self.ee_yield * lumi
        elif ch.lower() == "mm" :
            return self.mm_yield * lumi
        elif ch.lower() == "em" :
            return self.em_yield * lumi
        elif ch.lower() == "all" :
            return self.all_yield * lumi

    def acceptance(self, ch) :

        hbb = 0.57
        hww = 0.21
        br = 0.57 * 0.21 

        if ch.lower() == "ee" :
            return self.ee * br
        elif ch.lower() == "mm" :
            return self.mm * br
        elif ch.lower() == "em" :
            return self.em * br
        elif ch.lower() == "all" :
            return self.all * br

    #def acceptance(self, ch) :
    #    if ch.lower() == "ee" :
    #        return self.ee_num / self.ee_den
    #    elif ch.lower() == "mm" :
    #        return self.mm_num / self.mm_den
    #    elif ch.lower() == "em" :
    #        return self.em_num / self.em_den
    #    elif ch.lower() == "all" :
    #        return self.all_num / self.all_den
    #    else :
    #        print "Invalid channel '%s', exiting"%ch
    #        sys.exit()

def get_acceptance(accs, mass) :
    for a in accs :
        if a.mass == mass :
            return a

def get_acceptance_info(infile) :

    lines = open(infile).readlines()
    for iline, line in enumerate(lines) :
        line = line.strip()
        if "COUNTS" not in line : continue
        mass = int(lines[iline+1].split()[1])
        a = Acceptance(mass)

        # ee
        ee_acc = float(lines[iline+5].split()[4])
        ee_yield = float(lines[iline+4].split()[5])

        # mm
        mm_acc = float(lines[iline+9].split()[4])
        mm_yield = float(lines[iline+8].split()[5])

        # em
        em_acc = float(lines[iline+13].split()[4])
        em_yield = float(lines[iline+12].split()[5])

        # all
        all_acc = float(lines[iline+17].split()[4])
        all_yield = float(lines[iline+16].split()[4])

        a.ee = ee_acc
        a.mm = mm_acc
        a.em = em_acc
        a.all = all_acc

        a.ee_yield = ee_yield
        a.mm_yield = mm_yield
        a.em_yield = em_yield
        a.all_yield = all_yield

        return a

def calculate_signal_acceptance(select_mass, select_chan) :

    data_files = glob.glob("./truth_acc/*.txt")
    acceptances = []
    for f in data_files :
        ac = get_acceptance_info(f)
        if select_mass != "" :
            if ac.mass == int(select_mass) :
                acceptances.append(ac)
        else :
            acceptances.append(ac)
    return acceptances

def calculate_signal_efficiencies(select_mass, select_chan, acceptances) :

    data_file = "./reco_yields/reco_yields_100fb.txt"
    efficiencies = []
    idxs = {}
    lines = open(data_file).readlines()
    for iline, line in enumerate(lines) :
        if " X " not in line : continue
        splits = line.split()
        index = 0
        for isp, sp in enumerate(splits) :
            if sp == "X" :
                mass = int(splits[isp+1])
                idxs[index] = int(mass)
                index += 1

    sig_yields_ee = {}
    sig_yields_mm = {}
    sig_yields_em = {}
    sig_yields_all = {}
    for iline, line in enumerate(lines) :
        if "WWBB" not in line : continue
        if "region" in line : continue
        line = line.strip()

        index = 0
        if "EE" in line :
            splits = line.split()
            for isp, sp in enumerate(splits) :
                if sp == "\pm" :
                    yld = splits[isp-1]
                    sig_yields_ee[index] = float(yld)
                    index += 1

        elif "MM" in line :
            splits = line.split()
            for isp, sp in enumerate(splits) :
                if sp == "\pm" :
                    yld = splits[isp-1]
                    sig_yields_mm[index] = float(yld)
                    index += 1
        elif "EM" in line :
            splits = line.split()
            for isp, sp in enumerate(splits) :
                if sp == "\pm" :
                    yld = splits[isp-1]
                    sig_yields_em[index] = float(yld)
                    index += 1
        elif "ALL" in line :
            splits = line.split()
            for isp, sp in enumerate(splits) :
                if sp == "\pm" :
                    yld = splits[isp-1]
                    sig_yields_all[index] = float(yld)
                    index += 1

    reco_yields = {}
    for idx, mass in idxs.iteritems() :
        ee_yield = sig_yields_ee[idx]
        mm_yield = sig_yields_mm[idx]
        em_yield = sig_yields_em[idx]
        all_yield = sig_yields_all[idx]

        if select_mass != "" :
            if int(mass) != int(select_mass) : continue

        e = Efficiency(int(mass))
        a = get_acceptance(acceptances, int(mass))

        truth_yield_ee = a.yield_at_lumi("ee")
        truth_yield_mm = a.yield_at_lumi("mm")
        truth_yield_em = a.yield_at_lumi("em")
        truth_yield_all = a.yield_at_lumi("all")

        if truth_yield_ee > 0.0 :
            e.ee_eff = ee_yield / truth_yield_ee
        else :
            e.ee_eff = -1
        if truth_yield_mm > 0.0 :
            e.mm_eff = mm_yield / truth_yield_mm
        else :
            e.mm_eff = -1
        if truth_yield_em > 0.0 :
            e.em_eff = em_yield / truth_yield_em
        else :
            e.em_eff = -1
        if truth_yield_all > 0.0 :
            e.all_eff = all_yield / truth_yield_all
        else :
            e.all_eff = -1

        efficiencies.append(e)

    return efficiencies

def get_efficiency(mass, effs) :
    for e in effs :
        if int(e.mass) == int(mass) :
            return e

def get_background_yields(select_mass, select_chan) :

    backgrounds = []

    data_file = "./reco_yields/hh_bkg_yields_100fb.txt"
    lines = open(data_file).readlines()

    ylds_ee = {}
    ylds_mm = {}
    ylds_em = {}
    ylds_all = {}

    masses = []

    for iline, line in enumerate(lines) :
        if "WWBB" not in line : continue
        if "\pm" not in line : continue
        line = line.strip()
        line = line.split()

        reg = line[0].replace("WWBBOPT","").split("_")[0]
        mass = int(line[0].split("_")[1])

        masses.append(mass)

        total_yield = float(line[10])
        total_error = float(line[12])

        ylds = [total_yield, total_error] 
        if reg == "EE" :
            ylds_ee[mass] = ylds
        elif reg == "MM" :
            ylds_mm[mass] = ylds
        elif reg == "EM" :
            ylds_em[mass] = ylds
        elif reg == "ALL" :
            ylds_all[mass] = ylds

    for m in masses :
        if select_mass != "" :
            if int(select_mass) != m : continue
        b = Background(m)
        if len(ylds_ee) :
            b.ee_yield = ylds_ee[m][0]
            b.ee_error = ylds_ee[m][1]
        if len(ylds_mm) :
            b.mm_yield = ylds_mm[m][0]
            b.mm_error = ylds_mm[m][1]
        if len(ylds_em) :
            b.em_yield = ylds_em[m][0]
            b.em_error = ylds_em[m][1]
        if len(ylds_all) :
            b.all_yield = ylds_all[m][0]
            b.all_error = ylds_all[m][1]
        backgrounds.append(b)

    return backgrounds

def get_background(mass, backgrounds) :
    for b in backgrounds :
        if int(b.mass) == int(mass) :
            return b

def zdistance(input_value, from_value) :
    return abs(input_value - from_value)

def get_n_sig(bkg, bkg_stat_err, significance = 1.64) :

    sig_init = 10. * bkg
    sig = 0.1
    zn_test = 0.0
    zn_vals = []
    sig_vals = []

    if float(bkg) == 0.0 :
        return -1
    rel_stat = float(bkg_stat_err) / float(bkg)
    total_err = 0.3*0.3 + rel_stat*rel_stat 
    total_err = 0.3
    #total_err = sqrt(total_err)
    
    while zn_test < 5.0 :
        zn_test = r.RooStats.NumberCountingUtils.BinomialExpZ(sig, bkg, total_err)
        sig_vals.append(sig)
        zn_vals.append(zn_test)
        sig += 0.5

    distances = []

    for i, x in enumerate(sig_vals) :
        distances.append(zdistance(zn_vals[i], significance))
    idx, dist = min(enumerate(distances), key = itemgetter(1))
    n_sig = sig_vals[idx]
    return n_sig

def get_vs(mass, vss) :
    for v in vss :
        if int(mass) == int(v.mass) :
            return v


def get_visible_signal_yields(select_mass, select_chan, backgrounds) :

    masses = []
    if select_mass != "" :
        masses.append(int(select_mass))
    else :
        for b in backgrounds :
            masses.append(int(b.mass))

    signal_yields = []

    channels = ["ALL"]
    for m in masses :
        b = get_background(m, backgrounds)
        vs = VisibleSignal(m)

        for ch in channels :
            yld = 0.0
            err = 0.0
            if ch == "EE" :
                yld = b.ee_yield
                err = b.ee_error
                n_sig = get_n_sig(yld, err) 
                vs.n_ee = n_sig
            elif ch == "MM" :
                yld = b.mm_yield
                err = b.mm_error
                n_sig = get_n_sig(yld, err)
                vs.n_mm = n_sig
            elif ch == "EM" :
                yld = b.em_yield
                err = b.em_error
                n_sig = get_n_sig(yld, err)
                vs.n_em = n_sig
            elif ch == "ALL" :
                yld = b.all_yield
                err = b.all_error
                n_sig = get_n_sig(yld, err)
                vs.n_all = n_sig

        signal_yields.append(vs)

    return signal_yields

def get_visible_xsec(select_mass, select_chan, vss, effs, accs) :
    masses = []

    if select_mass != "" :
        masses.append(int(select_mass))
    else :
        for b in vss :
            masses.append(int(b.mass))

    lumi = 100.

    channels = ["ALL"]
    prod_xsecs = []
    for m in masses :
        eff = get_efficiency(m, effs)
        acc = get_acceptance(accs, m)
        vs = get_vs(m, vss)

        px = ProdXsec(m)

        for ch in channels :
            if ch == "EE" :
                e = eff.ee_eff
                a = acc.acceptance("ee")
                n = vs.n_ee
                x = n / lumi # divide by lumi
                x = x / 1000. # convert to pb
                den = float(e) * float(a)
                if den > 0.0 :
                    vis_xsec = float(x) / den 
                    px.ee = vis_xsec
            elif ch == "MM" :
                e = eff.mm_eff
                a = acc.acceptance("mm")
                n = vs.n_mm
                x = n / lumi # divide by lumi
                x = x / 1000. # convert to pb
                den = float(e) * float(a)
                if den > 0.0 :
                    vis_xsec = float(x) / den 
                    px.mm = vis_xsec
            elif ch == "EM" :
                e = eff.em_eff
                a = acc.acceptance("em")
                n = vs.n_em
                x = n / lumi # divide by lumi
                x = x / 1000. # convert to pb
                den = float(e) * float(a)
                if den > 0.0 :
                    vis_xsec = float(x) / den 
                    px.em = vis_xsec
            elif ch == "ALL" :
                e = eff.all_eff
                a = acc.acceptance("all")
                n = vs.n_all
                x = n / lumi # divide by lumi
                x = x / 1000. # convert to pb
                den = float(e) * float(a)
                if den > 0.0 :
                    print "MASS %d : e = %.5f a = %.5f x = %.5f vis = %.5f"%(m, e, a, x, x / den)
                    vis_xsec = float(x) / den
                    px.all = vis_xsec

        prod_xsecs.append(px)
    return prod_xsecs

def get_xsec(mass, xss) :
    for x in xss :
        if int(x.mass) == int(mass) :
            return x

def main() :
    print "estimate production cross sections"

    parser = OptionParser()
    parser.add_option("-x", default="", help="Select a specific resonance mass to use")
    parser.add_option("-c", default="", help="Select a specific dilepton channel [ee,mm,em,all]")
    (options, args) = parser.parse_args()
    select_mass = options.x
    select_chan = options.c

    acceptances = calculate_signal_acceptance(select_mass, select_chan)
    efficiencies = calculate_signal_efficiencies(select_mass, select_chan, acceptances)
    backgrounds = get_background_yields(select_mass, select_chan)
    visible_signals = get_visible_signal_yields(select_mass, select_chan, backgrounds)

    xsecs = get_visible_xsec(select_mass, select_chan, visible_signals, efficiencies, acceptances)

    masses = []
    if select_mass != "" :
        masses.append(int(select_mass))
    else :
        for x in backgrounds :
            masses.append(int(x.mass))
    masses = sorted(masses)

    print 55*"-"
    channels = ["ALL"]
    for ch in channels :
        print "  > CHANNEL %s"%ch
        print 32*"- " 
        for m in masses :
            xs = get_xsec(m, xsecs)
            if not xs : continue
            val = -1
            if ch == "EE" :
                val = xs.ee
            elif ch == "MM" :
                val = xs.mm
            elif ch == "EM" :
                val = xs.em 
            elif ch == "ALL" :
                val = xs.all
            print "mass %30d  :  %.4f"%(m, val)
    print 55*"-"
        

#____________________________________
if __name__ == "__main__" :
    main()
