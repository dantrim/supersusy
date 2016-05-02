
import os
import sys
sys.path.append(os.environ['SUSYDIR'])


import ROOT as r

class ZnSignal :
    def __init__(self, dsid_ = -1, mx_ = -1, my_ = -1, mz_ = -1) :
        self.name = "DSID %d (%.1f,%.1f,%.1f)"%(dsid_, mx_, my_, mz_)
        self.dsid = dsid_
        self.mx = mx_
        self.my = my_
        self.mz = mz_

        self.file = ""
        self.file_set = False
        self.tree = None

        self.scale_factor = 1.0

        self.yields = {} # { "region" : yield }
        self.significance_dict = {} # { "region" : significance }


    def setFile(self, file_ = "") :
        self.file = file_
        if file_ == "" :
            print "ZnSignal::setFile    ERROR Provided file is \"\"!"
            sys.exit()
        if not os.path.isfile(file_) :
            print "ZnSignal::setFile    ERROR Provided file ('%s') is not found"%file_
            sys.exit()
        if str(self.dsid) not in file_ :
            print "ZnSignal::setFile    ERROR DSID (%d) is not contained in the filename!"%self.dsid
            print "ZnSignal::setFile    ERROR Expect filename of form 'CENTRAL_XXXXXX.root'"
            sys.exit()

        self.file_set = True

    def getFile(self) :
        return self.file


    def setTree(self) :
        if self.file == "" or not self.file_set :
            print "ZnSignal::setTree    ERROR File has not been set yet. You must set file before getting tree!"
            sys.exit()

        treename = "superNt"

        chain = r.TChain(treename)
        chain.Add(self.file)
        self.tree = chain

        if not chain.GetEntries() > 0 :
            print "ZnSignal::setTree    ERROR Provided tree for DSID %d (%.1f,%.1f,%.1f) does not have any entries!"%(self.dsid, self.mx, self.my, self.mz)
            print "ZnSignal::setTree    ERROR File used to look for tree: %s"%self.file

    def getTree(self) :
        if self.tree == None :
            print "ZnSignal::getTree    ERROR Tree object is None for DSID %d (%.1f,%.1f,%.1f)"%(self.dsid, self.mx, self.my, self.mz)
            sys.exit()

        return self.tree

    def getName(self) :
        return self.name



