#! /usr/bin/env python
import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *

from PhysicsTools.FWLite.core.TreeNumpy import TreeNumpy 
from PhysicsTools.FWLite.core.ntupleObjects import * 
#from PhysicsTools.FWLite.ntupleTypes import * 
import copy

def prova(self) :
	print "ciao"


events = Events (["../../../../../../CMSSW_7_0_9/src/test04.root"])

jetLabel =  ('slimmedJets', '', 'PAT')
jetHandle = Handle("vector<pat::Jet> ")


myVars = {
   NTupleVariable("htJet25", lambda ev : ev.ht, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
 }



file = ROOT.TFile( "test.root", 'recreate')
tree = TreeNumpy("test","test")
for v in myVars :
	v.makeBranch(tree,False)	

setattr(ROOT.pat.Jet,prova.__name__,prova) 


# loop over events
count= 0
for event in events:
    count+=1
    print count
    if count > 1 : break
    event.getByLabel (jetLabel, jetHandle)
    event.slimmedJets = jetHandle.product()
    event.ht = 0
    event.m_jets = []
    a=0
    for j in event.slimmedJets:
	a=ROOT.pat.Jet(j)
	event.m_jets.append(a) #copy.deepcopy(j))
	j.setP4(j.p4()*10)
	print j.p4().pt()
    for j in event.m_jets :
	print j.p4().pt()

#fill all declared vals
    for v in myVars :
	v.fillBranch(tree,event,False)	
    tree.tree.Fill()		

file.cd()
tree.tree.Write()
file.Write()	
