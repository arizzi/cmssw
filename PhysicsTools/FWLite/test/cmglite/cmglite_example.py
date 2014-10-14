#! /usr/bin/env python
from PhysicsTools.FWLite.core.BasicTreeProducer  import * 
from PhysicsTools.FWLite.core.Looper import * 
class Bunch(dict):
    def __init__(self, **kw):
	dict.__init__(self,kw)
        self.__dict__ = self

def particlePrint(self):
        tmp = '{className} : {pdgId:>3}, pt = {pt:5.1f}, eta = {eta:5.2f}, phi = {phi:5.2f}, mass = {mass:5.2f}'
        return tmp.format( className = self.__class__.__name__,
                           pdgId = self.pdgId(),
                           pt = self.pt(),
                           eta = self.eta(),
                           phi = self.phi(),
                           mass = self.mass() 
			 )
setattr(ROOT.pat.Jet,"__str__",particlePrint)
setattr(ROOT.pat.Muon,"__str__",particlePrint)




treeProducer= Bunch(
	type=BasicTreeProducer, 
	verbose=False, 
	vectorTree = True,
	collections = {
		"slimmedMuons" : ( AutoHandle( ("slimmedMuons",), "std::vector<pat::Muon>" ),
                           NTupleCollection("mu", particleType, 4, help="patMuons, directly from MINIAOD") )

	}
	)

sequence = [treeProducer]
sample = Bunch(files = "../../../../../../CMSSW_7_0_9/src/test04.root", name="ATEST", isMC=False,isEmbed=False)
looper = Looper( 'Loop', sample,sequence, nPrint = 5)
looper.loop()
looper.write()

