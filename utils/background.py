import ROOT as r
import glob
import sys
sys.path.append('../..')

import supersusy.utils.systematic as systematic

r.TColor.__init__._creates = False
r.TEventList.__init__._creates = False

class Background :
    def __init__(self, name = "", displayname = "") :
        self.dbg = False
        self.dsid = ""
        self.treename = ""
        self.name = name
        self.displayname = displayname
        self.color = r.kRed
        self.line_style = 1
        self.fillStyle = 1001

        self.file = ""
        self.tree = None
        
        self.scale_factor = 1.0

        self.systList = []

        self.is_signal = False

    def setSignal(self) :
        self.is_signal = True
    def isSignal(self) :
        return self.is_signal
        

    def __eq__(self, other) :
        '''
        Equality method to compare to background samples to
        test if they are the same
        '''
        return (self.displayname==other.displayname)

    def __gt__(self, other, tcut) :
        '''
        Comparison operator to order background samples by
        their yields in a given region defined by tcut
        '''
        cut = r.TCut(tcut)
        sel = r.TCut("1")
        return ( self.tree.Draw("isMC", cut * sel, "goff") > other.tree.Draw("isMC", cut * sel, "goff") )

    def set_debug(self) :
        self.dbg = True
    def set_file(self, file) :
        self.file = file
    def set_treename(self, name) :
        '''
        This is if you are looking inside of a merged root tree
        where the tree name cannot be deduced from the input filename
        (i.e. is not of the form 'id_XXXXXX')
        '''
        self.treename = name

    def set_color(self, color) :
        self.color = color

    def set_fillStyle(self, style) :
        '''
        Override the default fill style
        '''
        self.fillStyle = style

    def setLineStyle(self, style) :
        '''
        Override the default line style
        '''
        self.line_style = style

    def set_scale_factor(self, sf) :
        '''
        Set the scale factor for this background
        '''
        self.scale_factor = sf

    def set_dsid_from_file(self, file) :
        dsid = ""
        if "CENTRAL" in file :
            dsid = file[file.find('CENTRAL_')+8 : self.file.find('.root')]
        else :
            print "Background.dsid_from_file ERROR    File format for background sample is unexpected. Exitting."
            sys.exit()
        self.dsid = dsid

    def set_tree(self) :
        tree_name = ""
        if "CENTRAL" in self.file :
            tree_name = "id_" + str(self.dsid)
        else :
            print "Background.set_tree ERROR    File format for signal sample is unexpected. Exitting."
            sys.exit()
        infile = r.TFile.Open(self.file)
        chain = r.TChain(tree_name)
        chain.Add(self.file)
        self.treename = tree_name
        self.tree = chain

    def set_merged_tree(self, name) :
        if self.file == "" :
            print 'Background.set_merged_tree ERROR   You must set the file for the sample before calling this function. Exitting.'
            sys.exit()
        infile = r.TFile.Open(self.file)
        chain = r.TChain(name)
        chain.Add(self.file)
        self.tree = chain

    def set_central_tree_from_merged(self) :
        tree_name = self.treename + "_CENTRAL"
        infile = r.TFile.Open(self.file)
        chain = r.TChain(tree_name)
        chain.Add(self.file)
        self.tree = chain

    def set_chain_from_list(self, list, directory, dsid_ = "") :
        '''
        Provide the filelist for the background process
        you would like the chain for. Will look in 
        'directory' for all of the root files

        Typically, when running over a singla sample for plotting
        we want only one DSID (corresponding to one grid point) but
        put all grid points in one filelist. Use the dsid_ to
        grab the desired signal point. You must call "setSignal()"
        on the background process before calling this.
        '''
        dsids = []
        lines = open(list).readlines()
        for line in lines :
             dsids.append(line[line.find('mc15_13TeV.')+11 : line.find('mc15_13TeV.')+17])
        rawdir_files = glob.glob(directory + "*.root")
        bkg_files = []
        for dataset_id in dsids :
            if self.isSignal() and not (dsid_ == dataset_id) : continue
            for f in rawdir_files :
                if 'entrylist' in f : continue
                if dataset_id in f :
                    bkg_files.append(f)
                    break
        chain = r.TChain('superNt')
        for file in bkg_files :
            chain.Add(file)
        self.tree = chain

    def set_chain_from_list_CONDOR(self, clist_dir, raw_directory, dsid_ = "") :
        '''
        Provide the directory that contains the .txt files
        of the condor filelists for the given sample

        Typically, when running over a singla sample for plotting
        we want only one DSID (corresponding to one grid point) but
        put all grid points in one filelist. Use the dsid_ to
        grab the desired signal point. You must call "setSignal()"
        on the background process before calling this.
        '''
        dsids = []
        if not clist_dir.endswith("/") :
            clist_dir = clist_dir + "/"
        con_files = glob.glob(clist_dir + "*.txt")
        for con in con_files :
            dsids.append(con[con.find('mc15_13TeV.')+11 : con.find('mc15_13TeV.')+17])
        rawdir_files = glob.glob(raw_directory + "*.root")
        bkg_files = []
        for dataset_id in dsids :
            if self.isSignal() and not (dsid_ == dataset_id) : continue
            for f in rawdir_files :
                if 'entrylist' in f : continue
                if dataset_id in f :
                    bkg_files.append(f)
                    break
        chain = r.TChain('superNt')
        for file in bkg_files :
            chain.Add(file)
        self.tree = chain


    def addSys(self, syst=None) :
        '''
        Add a systematic to this background
        '''
        this_syst = systematic.Systematic(syst.name, syst.up_name, syst.down_name)
        if syst.isWeightSys() :
            this_syst.setWeightSys()
            this_syst.tree = self.tree

        elif syst.isKinSys() :
            this_syst.setKinSys()
            file = self.file
            up_tree_name = self.name + "_" + syst.name + syst.up_name
            down_tree_name = self.name + "_" + syst.name + syst.down_name

            upchain = r.TChain(up_tree_name)
            downchain = r.TChain(down_tree_name)

            upchain.Add(self.file)
            downchain.Add(self.file)
            syst.tree_up = upchain
            syst.tree_down = downchain

        self.systList.append(this_syst)
        
    def Print(self) :
        print 'Background "%s" (tree %s from: %s)'%(self.displayname,self.treename, self.file)


class Data :
    def __init__(self) :
        self.dbg = False
        self.treename = ""
        self.name = "Data"
        self.displayname = "Data"
        self.color = r.kBlack

        self.file = ""
        self.tree = None

    def __eq__(self, other) :
        return (self.displayname == other.displayname)

    def set_debug(self) :
        self.dbg = True
    def set_file(self, file) :
        self.file = file
    def set_treename(self, name) :
        '''
        This is if you are looking inside of a merged root tere
        where the tree name cannot be deduced from the input filename
        (this is typical of Data samples)
        '''
        self.treename = name

    def set_color(self, color) :
        '''
        Override the default Data color
        '''
        self.color = color

    def set_tree(self) :
        if self.treename == "" :
            print "Data.set_tree ERROR    You must specify the treename first, it is currently empty. Exitting."
            sys.exit()
        chain = r.TChain(self.treename)
        chain.Add(self.file)
        self.tree = chain

    def set_merged_tree(self, name) :
        if self.file == "" :
            print 'Background.set_merged_tree ERROR   You must set the file for the sample before calling this function. Exitting.'
            sys.exit()
        infile = r.TFile.Open(self.file)
        chain = r.TChain(name)
        chain.Add(self.file)
        self.tree = chain

    def set_chain_from_list(self, list, directory) :
        '''
        Provide the filelist for the background process
        you would like the chain for. Will look in 
        'directory' for all of the root files
        '''
        dsids = []
        lines = open(list).readlines()
        for line in lines :
             dsids.append(line[line.find('data15_13TeV.00')+15 : line.find('data15_13TeV.')+21])
        rawdir_files = glob.glob(directory + "*.root")
        bkg_files = []
        for dataset_id in dsids :
            for f in rawdir_files :
                if 'entrylist' in f : continue
                if dataset_id in f :
                    bkg_files.append(f)
                    break
        chain = r.TChain('superNt')
        for file in bkg_files :
            chain.Add(file)
        self.tree = chain

    def set_chain_from_list_CONDOR(self, clist_dir, raw_directory) :
        '''
        Provide the directory that contains the .txt files
        of the condor filelists for the given sample
        '''
        dsids = []
        con_files = glob.glob(clist_dir + "*.txt")
        for con in con_files :
            dsids.append(con[con.find('data15_13TeV.00')+15 : con.find('data15_13TeV.')+21])
        rawdir_files = glob.glob(raw_directory + "*.root")
        bkg_files = []
        for dataset_id in dsids :
            for f in rawdir_files :
                if 'entrylist' in f : continue
                if dataset_id in f :
                    bkg_files.append(f)
                    break
        chain = r.TChain('superNt')
        for file in bkg_files :
            chain.Add(file)
        self.tree = chain

    def Print(self) :
        print 'Data sample "%s" (tree %s from: %s)'%(self.displayname, self.treename, self.file)


