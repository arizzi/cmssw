# The following comments couldn't be translated into the new config version:

#! /bin/env cmsRun

import FWCore.ParameterSet.Config as cms

process = cms.Process("rereco2")

#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#process.options = cms.untracked.PSet(multiProcesses=cms.untracked.PSet(
#         maxChildProcesses=cms.untracked.int32(40),
#         maxSequentialEventsPerChild=cms.untracked.uint32(100)))



# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

#parallel processing

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(),
    secondaryFileNames = cms.untracked.vstring()
)

process.GlobalTag.globaltag = 'PRE_STA71_V3::All'

process.reco = cms.Sequence(process.MeasurementTrackerEvent* process.siPixelClusterShapeCache+process.siPixelRecHits+process.siStripMatchedRecHits+process.ckftracks_wodEdX+process.offlinePrimaryVertices+process.ak5JetTracksAssociatorAtVertex*process.btagging)


process.p = cms.Path(process.reco)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('trkonly.root'),
)
process.endpath= cms.EndPath(process.out)


#process.PoolSource.secondaryFileNames =[
aa =[
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/04F8F8A0-3AD1-E311-9EF4-003048679188.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/34AED71C-3BD1-E311-BEF8-0025905A60EE.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/428E5CD4-7ED1-E311-A2E0-0025905A60D0.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/588BE153-49D1-E311-B731-0025905A605E.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/72BABEA5-3AD1-E311-A53D-00261894396F.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/80BE433C-49D1-E311-9EC7-0025905A6056.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/8899FFED-52D1-E311-A087-0025905A6134.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/A8F1F8E6-7ED1-E311-BD60-002590596490.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/BAEB8FF8-7ED1-E311-AA90-0025905A60B8.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_STA71_V3-v1/00000/E27E91C8-88D1-E311-B2C5-002590593878.root"
]
process.PoolSource.fileNames =[
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-RECO/PRE_STA71_V3-v1/00000/887DEA5B-5CD1-E311-BB97-002618943923.root",
"/store/relval/CMSSW_7_1_0_pre7/RelValTTbar/GEN-SIM-RECO/PRE_STA71_V3-v1/00000/8EEC0F1F-9FD1-E311-966F-003048FFD76E.root"
]
