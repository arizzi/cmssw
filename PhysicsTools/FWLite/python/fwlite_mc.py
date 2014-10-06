#! /usr/bin/env python
import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *

from PhysicsTools.FWLite.TreeNumpy import TreeNumpy 
from PhysicsTools.FWLite.ntupleObjects import * 
#rom PhysicsTools.FWLite.ntupleTypes import * 

events = Events (["../../../../../CMSSW_7_0_9/src/test04.root"])

jetLabel =  ('slimmedJets', '', 'PAT')
jetHandle = Handle("vector<pat::Jet> ")


myVars = {
   NTupleVariable("htJet25", lambda ev : ev.ht, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
 }



file = ROOT.TFile( "test.root", 'recreate')
tree = TreeNumpy("test","test")
for v in myVars :
	v.makeBranch(tree,False)	

# loop over events
count= 0
for event in events:
    count+=1
    print count
    if count > 1000 : break
    event.getByLabel (jetLabel, jetHandle)
    event.slimmedJets = jetHandle.product()
    event.ht = 0
    event.m_jets = []
    i=0
    for j in event.jets :
	event.ht+=j.pt()
	event.m_jets.append(j)
	event.m_jets[-1].pippo =7
	print event.m_jets[-1].pippo
	event.jets[i].pippo = 7
	print event.jets[i]
	i+=1

#fill all declared vals
    for v in myVars :
	v.fillBranch(tree,event,False)	
    tree.tree.Fill()		

file.cd()
tree.tree.Write()
file.Write()	
