#! /usr/bin/env python
import ROOT
import PhysicsTools.HeppyCore.framework.config as cfg

# The content of the output tree is defined here
# the definitions of the NtupleObjects are located under PhysicsTools/Heppy/pythonanalyzers/objects/autophobj.py
 
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
#override defaults
from  nanoTypes import *
treeProducer= cfg.Analyzer(
	class_object=AutoFillTreeProducer, 
	verbose=False, 
	vectorTree = True,
        #here the list of simple event variables (floats, int) can be specified
        globalVariables = [
             NTupleVariable("rho",  lambda ev: ev.rho, float, help="jets rho"),
             NTupleVariable("rhoN",  lambda ev: ev.rhoN, float, help="rho with neutrals only"),
             NTupleVariable("nPU0", lambda ev : [bx.nPU() for bx in  ev.pileUpInfo if bx.getBunchCrossing()==0][0], help="nPU in BX=0",mcOnly=True),
             NTupleVariable("nPVs", lambda ev : len(ev.goodVertices), help="total number of good PVs"),
             NTupleVariable("bx",  lambda ev: ev.input.eventAuxiliary().bunchCrossing(), int, help="bunch crossing number"),
             NTupleVariable("met_sig",  lambda ev : ev.met.significance(), help="met significance from MET::significance() method"),
             NTupleVariable("met_covXX",  lambda ev : ev.met.getSignificanceMatrix().At(0,0), help="xx element of met covariance matrix"),
             NTupleVariable("met_covXY",  lambda ev : ev.met.getSignificanceMatrix().At(0,1), help="xy element of met covariance matrix"),
             NTupleVariable("met_covYY",  lambda ev : ev.met.getSignificanceMatrix().At(1,1), help="yy element of met covariance matrix"),
             NTupleVariable("met_rawpt",  lambda ev : ev.met.uncorPt(), help="raw met"),
             NTupleVariable("lhe_Nj",  lambda ev: ev.lheNj, float,mcOnly=True, help="number of jets at LHE level"),
             NTupleVariable("lhe_Nb",  lambda ev: ev.lheNb, float,mcOnly=True, help="number of b-jets at LHE level"),
             NTupleVariable("lhe_Nc",  lambda ev: ev.lheNc, float,mcOnly=True, help="number of c-jets at LHE level"),
             NTupleVariable("lhe_Ng",  lambda ev: ev.lheNg, float,mcOnly=True, help="number of gluon jets at LHE level"),
             NTupleVariable("lhe_Nl",  lambda ev: ev.lheNl, float,mcOnly=True, help="number of light(uds) jets at LHE level"),
             NTupleVariable("lhe_Vpt",  lambda ev: ev.lheV_pt, float,mcOnly=True, help="Vector pT at LHE level"),
             NTupleVariable("lhe_HT",  lambda ev: ev.lheHT, float,mcOnly=True, help="HT at LHE level"),


        ],
        #here one can specify compound objects 
        globalObjects = {
          "met"    : NTupleObject("met",     metType, help="PF E_{T}^{miss}, after default type 1 corrections"),

        },
	collections = {
 		#The following would just store the electrons and muons from miniaod without any selection or cleaning
                # only the basice particle information is saved
		#"slimmedMuons" : ( AutoHandle( ("slimmedMuons",), "std::vector<pat::Muon>" ),
                #           NTupleCollection("mu", particleType, 4, help="patMuons, directly from MINIAOD") ),
                #"slimmedElectron" : ( AutoHandle( ("slimmedElectrons",), "std::vector<pat::Electron>" ),
                #           NTupleCollection("ele", particleType, 4, help="patElectron, directly from MINIAOD") ),

		#standard dumping of objects
   	        "selectedLeptons" : NTupleCollection("Lepton", leptonType, 10, help="Leptons after the preselection"),
                "selectedTaus"    : NTupleCollection("Tau", tauType, 10, help="Taus after the preselection"),
                "selectedPhotons"    : NTupleCollection("Photon", photonType, 10, help="Taus after the preselection"),
	        "cleanJetsAll"       : NTupleCollection("Jet",     nanoJetType, 20, help="Cental jets after full selection and cleaning, sorted by b-tag"),
                "goodVertices"    : NTupleCollection("primaryVertices", primaryVertexType, 4, help="first four PVs"),

		#dump of gen objects
                "genJets"    : NTupleCollection("GenJet",   genJetType, 15, help="Generated jets with hadron matching, sorted by pt descending",filter=lambda x: x.pt() > 20,mcOnly=True),
                "gentopquarks"    : NTupleCollection("GenTop",     genParticleType, 10, help="Generated top quarks from hard scattering"),
                "genbquarks"      : NTupleCollection("GenBQuark",  genParticleType, 10, help="Generated bottom quarks from top quark decays"),
                "genwzquarks"     : NTupleCollection("GenQuark",   genParticleType, 20, help="Generated quarks from W/Z decays"),
                "genleps"         : NTupleCollection("GenLep",     genParticleType, 20, help="Generated leptons from W/Z decays"),
                "gentauleps"      : NTupleCollection("GenLepFromTau", genParticleType, 10, help="Generated leptons from decays of taus from W/Z/h decays"),
                "gennus"         : NTupleCollection("GenNu",     genParticleWithAncestryType, 6, help="Generated neutrino from W/Z decays",mcOnly=True),
                "gentaus"         : NTupleCollection("GenTaus",     genParticleWithAncestryType, 6, help="Generated taus",mcOnly=True),
               
	}
	)

# Import standard analyzers and take their default config
from PhysicsTools.Heppy.analyzers.objects.LeptonAnalyzer import LeptonAnalyzer
LepAna = LeptonAnalyzer.defaultConfig
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
VertexAna = VertexAnalyzer.defaultConfig
from PhysicsTools.Heppy.analyzers.objects.PhotonAnalyzer import PhotonAnalyzer
PhoAna = PhotonAnalyzer.defaultConfig
from PhysicsTools.Heppy.analyzers.objects.TauAnalyzer import TauAnalyzer
TauAna = TauAnalyzer.defaultConfig
from PhysicsTools.Heppy.analyzers.objects.JetAnalyzer import JetAnalyzer
JetAna = JetAnalyzer.defaultConfig
JetAna.jetLepArbitration =  lambda jet,lepton: (jet,lepton)
JetAna.jetPt = 10
JetAna.cleanSelectedLeptons = False
JetAna.minLepPt = 3
JetAna.doPuId = True
JetAna.doQG= True
from PhysicsTools.Heppy.analyzers.gen.LHEAnalyzer import LHEAnalyzer 
LHEAna = LHEAnalyzer.defaultConfig
from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer import GeneratorAnalyzer 
GenAna = GeneratorAnalyzer.defaultConfig
from PhysicsTools.Heppy.analyzers.objects.METAnalyzer import METAnalyzer
METAna = METAnalyzer.defaultConfig
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
PUAna = PileUpAnalyzer.defaultConfig
from PhysicsTools.Heppy.analyzers.core.TriggerBitAnalyzer import TriggerBitAnalyzer
FlagsAna = TriggerBitAnalyzer.defaultEventFlagsConfig

# Configure trigger bit analyzer
from PhysicsTools.Heppy.analyzers.core.TriggerBitAnalyzer import TriggerBitAnalyzer
TrigAna= cfg.Analyzer(
    verbose=False,
    class_object=TriggerBitAnalyzer,
    #grouping several paths into a single flag
    # v* can be used to ignore the version of a path
    triggerBits={
    'ELE':["HLT_Ele*","HLT_Ele32_eta2p1_WP85_Gsf_v*","HLT_Ele32_eta2p1_WP85_Gsf_v*"],
    'MU': ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*","HLT_IsoTkMu24_eta2p1_IterTrk02_v*","HLT_IsoTkMu24_IterTrk02_v*"],
    },
#   processName='HLT',
#   outprefix='HLT'
    #setting 'unrollbits' to true will not only store the OR for each set of trigger bits but also the individual bits
    #caveat: this does not unroll the version numbers
    unrollbits=True 
    )



#replace some parameters
LepAna.loose_muon_pt = 10

from NanoAnalyzer import *
Nano = cfg.Analyzer(
    verbose = False,
    class_object = NanoAnalyzer
)

sequence = [LHEAna,FlagsAna, GenAna, PUAna,TrigAna,VertexAna,LepAna,TauAna,PhoAna,JetAna,METAna,Nano,treeProducer]

#use tfile service to provide a single TFile to all modules where they
#can write any root object. If the name is 'outputfile' or the one specified in treeProducer
#also the treeProducer uses this file
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService 
output_service = cfg.Service(
      TFileService,
      'outputfile',
      name="outputfile",
      fname='tree.root',
      option='recreate'
    )

testfiles=['02656FC1-B0B5-E611-B2F9-44A842CFCA27.root']
#testfiles=['28CA6CC9-FEC2-E611-BF37-008CFA5D2758.root']

sample = cfg.MCComponent(
#specify the file you want to run on
    # files = ["/scratch/arizzi/Hbb/CMSSW_7_2_2_patch2/src/VHbbAnalysis/Heppy/test/ZLL-8A345C56-6665-E411-9C25-1CC1DE04DF20.root"],
    files = testfiles,
    name="SingleSample", isMC=True,isEmbed=False
    )

# the following is declared in case this cfg is used in input to the heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
selectedComponents = [sample]
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [output_service],  
                     events_class = Events)

# and the following runs the process directly if running as with python filename.py  
if __name__ == '__main__':
    from PhysicsTools.HeppyCore.framework.looper import Looper 
    looper = Looper( 'Loop', config, nPrint = 5,nEvents=35000) 
    looper.loop()
    looper.write()
