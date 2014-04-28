import FWCore.ParameterSet.Config as cms

slimmedElectrons = cms.EDProducer("PATElectronSlimmer",
   src = cms.InputTag("selectedPatElectrons"),
   dropSuperCluster = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropBasicClusters = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropPFlowClusters = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropPreshowerClusters = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropSeedCluster = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropRecHits = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropCorrections = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropIsolations = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropShapes = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropExtrapolations  = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   dropClassifications  = cms.string("0"), # you can put a cut to slim selectively, e.g. pt < 10
   linkToPackedPFCandidates = cms.bool(True),
   recoToPFMap = cms.InputTag("reducedEgamma","reducedGsfElectronPfCandMap"),
   packedPFCandidates = cms.InputTag("packedPFCandidates"), 
   saveNonZSClusterShapes = cms.string(""), # save additional user floats: (sigmaIetaIeta,sigmaIphiIphi,sigmaIetaIphi,r9,e1x5_over_e5x5)_NoZS 
)

