from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import itertools
import ROOT
class VHbbAnalyzer( Analyzer ):
    '''Analyze VH events
    '''

    def declareHandles(self):
        super(VHbbAnalyzer, self).declareHandles()
#        self.handles['pfCands'] =  AutoHandle( 'packedPFCandidates', 'std::vector<pat::PackedCandidate>' )

    def beginLoop(self):
        super(VHbbAnalyzer,self).beginLoop()
    
    def makeJets(self,event):
	inputs=ROOT.std.vector(ROOT.heppy.ReclusterJets.LorentzVector)()
	for pf in event.pfCands :
	     if pf.fromPV() :
		inputs.push_back(pf.p4())
	clusterizer=ROOT.heppy.ReclusterJets(inputs,-1,0.1)
	jets = clusterizer.getGrouping(30)
	#for j in list(jets)[0:3]:
	#	print j.pt(),
	#print " "
    def doFakeMET(self,event):
	#fake MET from Zmumu
	event.fakeMET = ROOT.reco.Particle.LorentzVector(0.,0.,0.,0.)
	event.fakeMET.sumet = 0
	if event.Vtype == 0 :
		event.fakeMET=event.met.p4() + event.V
                event.fakeMET.sumet = event.met.sumEt() - event.V.pt()

    def doHiggsHighCSV(self,event) :
        #leading csv interpretation
        event.hJetsCSV=sorted(event.cleanJets,key = lambda jet : jet.btag('combinedSecondaryVertexBJetTags'), reverse=True)[0:2]
        event.aJetsCSV = [x for x in event.cleanJets if x not in event.hJetsCSV]
        event.hjidxCSV=[event.cleanJets.index(x) for x in event.hJetsCSV ]
        event.ajidxCSV=[event.cleanJets.index(x) for x in event.aJetsCSV ]
        event.aJetsCSV+=event.cleanJetsFwd
        event.HCSV = event.hJetsCSV[0].p4()+event.hJetsCSV[1].p4()

    def doHiggsHighPt(self,event) :
        #highest pair interpretations
        event.hJets=list(max(itertools.combinations(event.cleanJets,2), key = lambda x : (x[0].p4()+x[1].p4()).pt() ))
        event.aJets = [x for x in event.cleanJets if x not in event.hJets]
        event.hjidx=[event.cleanJets.index(x) for x in event.hJets ]
        event.ajidx=[event.cleanJets.index(x) for x in event.aJets ]
        event.aJets+=event.cleanJetsFwd
        event.H = event.hJets[0].p4()+event.hJets[1].p4()

    def classifyMCEvent(self,event):
        if self.cfg_comp.isMC:
		event.VtypeSim = -1
		#event.bosons.

    def classifyEvent(self,event):
	#assign events to analysis (Vtype)
	#enum CandidateType{Zmumu, Zee, Wmun, Wen, Znn,  Zemu, Ztaumu, Ztaue, Wtaun, Ztautau, Zbb, UNKNOWN};
	event.Vtype=-1
        nLep=len(event.selectedLeptons)	
	event.vLeptons=[]
	#WH requires exactly one selected lepton
	wElectrons=[x for x in event.selectedElectrons if self.cfg_ana.wEleSelection(x) ]
	wMuons=[x for x in event.selectedMuons if self.cfg_ana.wMuSelection(x) ]
	zElectrons=[x for x in event.selectedElectrons if self.cfg_ana.zEleSelection(x) ]
	zMuons=[x for x in event.selectedMuons if self.cfg_ana.zMuSelection(x) ]


	if len(zMuons) >=  2 :
		    for i in xrange(1,len(zMuons)):
			if zMuons[0].charge()*zMuons[i].charge()<0 :
	                      event.Vtype = 0
			      event.vLeptons =[zMuons[0],zMuons[i]]
			      break
	elif len(zElectrons) >=  2 :
#	    for i in zElectrons[0].electronIDs()  :
#			print i.first,i.second
		    for i in xrange(1,len(zElectrons)):
			if zElectrons[0].charge()*zElectrons[i].charge()<0 :
	                      event.Vtype = 1
			      event.vLeptons =[zElectrons[0],zElectrons[i]]
			      break
	elif len(wElectrons) + len(wMuons) == 1: 
		if abs(event.selectedLeptons[0].pdgId())==13 :
			event.Vtype = 2
			event.vLeptons =event.selectedLeptons
		if abs(event.selectedLeptons[0].pdgId())==11 :
			event.Vtype = 3
			event.vLeptons =event.selectedLeptons
	else :
		event.Vtype = 4	
		#apply MET cut
		if  event.met.pt() < 50 :
			 return False


	event.V=sum(map(lambda x:x.p4(), event.vLeptons),ROOT.reco.Particle.LorentzVector(0.,0.,0.,0.))
	
	if event.Vtype > 1 :	
		event.V+=event.met.p4()

	event.aLeptons = [x for x in event.inclusiveLeptons if x not in event.vLeptons]

	return True

    def process(self, event):
        self.readCollections( event.input )
#	event.pfCands = self.handles['pfCands'].product()
# 	met = event.met
	
	#substructure threshold, make configurable
	ssTrheshold = 200.
	# filter events with less than 2 jets with pt 20
	if not   (len(event.cleanJets) >= 2 and event.cleanJets[1] > 20.) : # or(len(event.cleanJets) == 1 and event.cleanJets[0] > ssThreshold ) ) :
		return False

	if not self.classifyEvent(event) :
		return False
	self.doHiggsHighCSV(event)
	self.doHiggsHighPt(event)
	self.doFakeMET(event)


   	self.classifyMCEvent(event)
	
	#to implement
	#if some threshold: 
	#   self.computeSubStructuresStuff()  
   	
	#self.doIVFHiggs()
	#self.computePullAngle()
	#

	#perhaps in different producers:	
	# LHE weights
	# Trigger weights
	# gen level VH specific info
	# add soft jet info to jets
	# PU weights
	# SIM B hadrons information
	# MET corrections (in MET analyzer)
  	# trigger flags
		

	#self.makeJets(event)
        return True




