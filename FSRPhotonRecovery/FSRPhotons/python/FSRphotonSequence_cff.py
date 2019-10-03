import FWCore.ParameterSet.Config as cms
import os

def addFSRphotonSequence(process, MuonFSRCollection, FSRphotonMVAweightfile):

    process.extractPhotons = cms.EDProducer("FSRPhotonProducer",
                                            srcCands = cms.InputTag("packedPFCandidates"),
                                            ptThresh = cms.double(1.0) ## will tighten to 2 at analysis level
                                            )

    import PhysicsTools.PatAlgos.producersLayer1.pfParticleProducer_cfi 
    process.slimmedPFPhotons = PhysicsTools.PatAlgos.producersLayer1.pfParticleProducer_cfi.patPFParticles.clone(
        pfCandidateSource = 'extractPhotons'
        )

    process.FSRRecovery = cms.EDProducer("FSRRecoveryProducer",
                                         pfcands = cms.InputTag("packedPFCandidates"),
                                         muons = cms.InputTag(MuonFSRCollection), 
                                         electrons = cms.InputTag("slimmedElectrons"),
                                         pfphotons = cms.InputTag("slimmedPFPhotons"),
                                         patphotons = cms.InputTag("slimmedPhotons"),
                                         weights = cms.string(FSRphotonMVAweightfile)
                                         )

    process.FSRphotonSequence = cms.Sequence(process.extractPhotons
                                             *process.slimmedPFPhotons
                                             *process.FSRRecovery
                                             ) 
