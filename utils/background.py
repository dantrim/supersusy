import ROOT as r
import glob
import sys
sys.path.append('../..')

r.TColor.__init__._creates = False
r.TEventList.__init__._creates = False

class Background :
    def __init__(self, displayname = "") :
        self.dbg = False
        self.treename = ""
        self.displayname = displayname
        self.color = r.kRed
        self.fillStyle = 1001

        self.file = ""
        self.tree = None
        
        self.scale_factor = 1.0
        

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

    def Print(self) :
        print 'Background "%s" (tree %s from: %s)'%(self.displayname,self.treename, self.file)


class Data :
    def __init__(self) :
        self.dbg = False
        self.treename = ""
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

    def Print(self) :
        print 'Data sample "%s" (tree %s from: %s)'%(self.displayname, self.treename, self.file)


