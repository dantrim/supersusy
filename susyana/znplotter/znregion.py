
import os
import sys
sys.path.append(os.environ['SUSYDIR'])

import collections

class ZnRegion :
    def __init__(self, name_ = "", displayname_ = "", id_ = -1) :
        self.name = name_
        self.displayname = displayname_
        self.Id = id_
        self.is_parent = False
        self.parent_name = ""
        self.tcut = ""

        self.orthogonal_subregions = []

        self.debug = False

    def Print(self) :
        print " -------------------------------- "
        print "  ZnRegion Print "
        print "      name        : %s"%self.name
        print "      displayname : %s"%self.displayname
        print "      id          : %s"%self.Id
        print "      is parent   : %s"%self.is_parent
        print "      parent name : %s"%self.parent_name
        print "      tcut        : %s"%self.tcut
        print " -------------------------------- "
        for ch in self.orthogonal_subregions :
            ch.Print()


    def add_orthogonal_subregion(self, region_) :
        if region_.isParent() :
            print "ZnRegion::add_orthogonal_subregion    ERROR Attempting to add as child a parent region '%s' to region '%s'"%(region_.name, self.name)
            sys.exit()
        if region_.tcut == "" :
            print "ZnRegion::add_orthogonal_subregion    ERROR Attempting to add a child region ('%s') to parent region '%s'"%(region_.name, self.name)
            print "ZnRegion::add_orthogonal_subregion    ERROR that does not have a defined tcut!" 
            sys.exit()
        if region_.getName() == "" or region_.getDisplayName() == "" :
            print "ZnRegion::add_orthogonal_subregion    ERROR Attempting to add a child region that does not have a name to"
            print "ZnRegion::add_orthogonal_subregion    ERROR parent region '%s'"%self.name
            sys.exit()

        region_.setParentName(self.name)

        self.orthogonal_subregions.append(region_)
        if self.dbg() :
            print "ZnRegion::add_orthogonal_subregion    %s added subregion %s"%(self.name, region_.name)

    def getTcut(self) :
        return self.tcut
    def setTcut(self, cut_ = "") :
        self.tcut = cut_

    def isParent(self) :
        return self.is_parent
    def setParent(self, isParent_ = True) :
        self.is_parent = isParent_

    def setParentName(self, name_ = "" ) :
        if self.isParent() :
            print "ZnRegion::setParentName    ERROR Attempting to set parent name ('%s') for parent region ('%s')!"%(self.name_, self.name)
            sys.exit()
        self.parent_name = name_
    def getParentName(self) :
        if self.isParent() :
            print "ZnRegion::getParentName    WARNING Attempting to retrieve parent name from parent region ('%s')"%self.name
            print "ZnRegion::getParentName    WARNING Returning \"\""
            return ""
        else :
            return self.parent_name
        

    def getId(self) :
        return self.Id
    def setId(self, id_ = -1) :
        if id_ < 0 :
            print "ZnRegion::setId    WARNING Provided Id is negative for region '%s'"%self.name
        self.Id = id_
        return id_

    def setName(self, name_ = "", displayname_ = "") :
        self.name = name_
        self.displayname = displayname_ 
    def getName(self) :
        return self.name
    def getDisplayName(self) :
        return self.displayname

    def setDebug(self, dbg_ = True) :
        self.debug = dbg_
    def dbg(self) :
        return self.debug
