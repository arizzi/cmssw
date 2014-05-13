import FWCore.ParameterSet.Config as cms

process = cms.Process("dumper")

#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.TFileService = cms.Service("TFileService", 
      fileName = cms.string("tree.root"),
      closeFileFast = cms.untracked.bool(True)
  )

# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("SimTracker.TrackAssociation.TrackAssociatorByHits_cfi")
#parallel processing

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.source = cms.Source("PoolSource",
secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring()
)

process.GlobalTag.globaltag = 'PRE_LS171_V7::All'

process.load("SimGeneral.TrackingAnalysis.simHitTPAssociation_cfi")
process.load("SimTracker.TrackAssociation.quickTrackAssociatorByHits_cfi")
process.quickTrackAssociatorByHits.useClusterTPAssociation = cms.bool(True)
#process.load("SimTracker.TrackerHitAssociation.clusterTpAssociationProducer_cfi")


process.dump = cms.EDProducer("LightTrackNtuple",
    simG4 = cms.InputTag("g4SimHits"),
    trackingTruth = cms.untracked.InputTag("mix","MergedTrackTruth"),
    trackInputTag = cms.untracked.InputTag("generalTracks"),
    allSim = cms.untracked.bool(False)
)

process.p = cms.Path(process.simHitTPAssocProducer*process.dump)


process.PoolSource.fileNames = [
"file:trk.root"
]


