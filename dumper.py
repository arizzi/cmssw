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
    input = cms.untracked.int32(10000)
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

process.PoolSource.secondaryFileNames =[
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_LS171_V7-v1/00000/044129A0-AED0-E311-8463-02163E00E87F.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_LS171_V7-v1/00000/1C3550F0-ADD0-E311-897A-02163E00EAAE.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_LS171_V7-v1/00000/2689DCE2-ADD0-E311-BC2D-00304896B908.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_LS171_V7-v1/00000/3EEB2741-ADD0-E311-92C6-02163E00EA17.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_LS171_V7-v1/00000/6892CAFF-ACD0-E311-9BBE-02163E00BB52.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_LS171_V7-v1/00000/7273361F-C8D0-E311-8F0D-02163E00BA16.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_LS171_V7-v1/00000/72809857-ADD0-E311-8757-02163E00E89D.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_LS171_V7-v1/00000/BE5FB211-B3D0-E311-A898-02163E00EA53.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_LS171_V7-v1/00000/DCA244FB-ADD0-E311-8E60-02163E00E84E.root"
]

process.PoolSource.fileNames = [
"/store/relval/CMSSW_7_1_0_pre7/RelValQCD_Pt_600_800_13/GEN-SIM-RECO/PRE_LS171_V7-v1/00000/0E2F833B-D0D0-E311-84E8-02163E00C85A.root"
]


