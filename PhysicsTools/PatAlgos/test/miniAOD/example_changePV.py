import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process("USER")

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#        '/store/mc/RunIISpring15DR74/WprimeToMuNu_M-5600_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/Asympt50ns_MCRUN2_74_V9A-v1/00000/40B7ADFF-3AFD-E411-AEB1-0025B3E05DD6.root'
        'file:/tmp/arizzi/40B7ADFF-3AFD-E411-AEB1-0025B3E05DD6.root'
    )
)

## Output file
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.OUT = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('test.root'),
    outputCommands = cms.untracked.vstring(['keep *','drop *_*_*_USER','keep patJets_selectedPatJets_*_*','keep recoVertexs_pfCHS_*_*'])
)
process.endpath= cms.EndPath(process.OUT)

#################################################
## Remake jets
#################################################

## Filter out neutrinos from packed GenParticles
process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"))
## Define GenJets
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
process.ak4GenJetsNoNu = ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNu')

## Select charged hadron subtracted packed PF candidates
process.pfCHSforIso = cms.EDProducer("PATPackedCandidatePVSelector", src = cms.InputTag("packedPFCandidates"), vertexScores = cms.InputTag("offlineSlimmedPrimaryVertices"), threshold=cms.int32(2))
process.pfCHS = cms.EDProducer("PATPackedCandidatePVSelector", src = cms.InputTag("packedPFCandidates"), vertexScores = cms.InputTag("offlineSlimmedPrimaryVertices"), threshold=cms.int32(0))
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
## Define PFJetsCHS
process.ak4PFJetsCHS = ak4PFJets.clone(src = 'pfCHS', doAreaFastjet = True)


#################################################
## Remake PAT jets
#################################################

## b-tag discriminators
bTagDiscriminators = [
    'pfCombinedInclusiveSecondaryVertexV2BJetTags'
]

from PhysicsTools.PatAlgos.tools.jetTools import *
## Add PAT jet collection based on the above-defined ak5PFJetsCHS
addJetCollection(
    process,
    labelName = '',
    jetSource = cms.InputTag('ak4PFJetsCHS'),
    pvSource = cms.InputTag('pfCHS'),
    pfCandidates = cms.InputTag('packedPFCandidates'),
# cannot reuse SV because they depend on PV
#    svSource = cms.InputTag('slimmedSecondaryVertices'),
    btagDiscriminators = bTagDiscriminators,
    jetCorrections = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    genJetCollection = cms.InputTag('ak4GenJetsNoNu'),
    genParticles = cms.InputTag('prunedGenParticles'),
    algo = 'AK',
    rParam = 0.4
)

getattr(process,'selectedPatJets').cut = cms.string('pt > 10')

#not needed in unscheduled
#process.p = cms.Path(process.selectedPatJets)

## Load IVF
# use packed cands instead of AOD particleFlow
# the PV is changed by the adaptPV call below
process.load("RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff")
process.inclusiveCandidateVertexFinder.tracks='packedPFCandidates'
process.candidateVertexArbitrator.tracks='packedPFCandidates'

from PhysicsTools.PatAlgos.tools.pfTools import *
## Adapt primary vertex collection
adaptPVs(process, pvCollection=cms.InputTag('pfCHS'))


process.options = cms.untracked.PSet( 
        wantSummary = cms.untracked.bool(True), # while the timing of this is not reliable in unscheduled mode, it still helps understanding what was actually run 
        allowUnscheduled = cms.untracked.bool(True)
)
