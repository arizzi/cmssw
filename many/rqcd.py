# The following comments couldn't be translated into the new config version:

#! /bin/env cmsRun

import FWCore.ParameterSet.Config as cms

process = cms.Process("rereco2")

#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(multiProcesses=cms.untracked.PSet(
         maxChildProcesses=cms.untracked.int32(10),
         maxSequentialEventsPerChild=cms.untracked.uint32(1000)))



# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

#parallel processing

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(),
    secondaryFileNames = cms.untracked.vstring()
)

process.GlobalTag.globaltag = 'PRE_STA71_V3::All'

#process.reco = cms.Sequence(process.siPixelRecHits+process.siStripMatchedRecHits+process.ckftracks_wodEdX+process.offlinePrimaryVertices+process.ak5JetTracksAssociatorAtVertex*process.btagging)
process.reco = cms.Sequence(process.MeasurementTrackerEvent* process.siPixelClusterShapeCache+process.siPixelRecHits+process.siStripMatchedRecHits+process.ckftracks_wodEdX+process.offlinePrimaryVertices+process.ak5JetTracksAssociatorAtVertex*process.btagging)


process.p = cms.Path(process.reco)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('trk.root'),
)
process.endpath= cms.EndPath(process.out)

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
