import FWCore.ParameterSet.Config as cms

packedPFCandidates = cms.EDProducer("PATPackedCandidateProducer",
    inputCollection = cms.InputTag("particleFlow"),
    inputVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    originalVertices = cms.InputTag("offlinePrimaryVertices"),
    originalTracks = cms.InputTag("generalTracks"),
    PuppiWeight = cms.InputTag("puppi","PuppiWeights"),
    vertexAssociator = cms.InputTag("primaryVertexAssociation","original"),
    minPtForTrackProperties = cms.double(0.95)
)
