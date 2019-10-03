import os, sys, re
import FWCore.ParameterSet.Config as cms
import FWCore.PythonUtilities.LumiList as LumiList
from FWCore.ParameterSet.VarParsing import VarParsing
from Configuration.AlCa.GlobalTag import GlobalTag

## SET OPTIONS

options = VarParsing('analysis')

options.register ('runOnData', False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "runOnData (True/False)")

options.register ('PhotonMVA', "FSRPhotonRecovery/FSRPhotons/data/PhotonMVAv9_BDTG800TreesDY.weights.xml", VarParsing.multiplicity.singleton, VarParsing.varType.string, "datapath")

options.parseArguments()

process = cms.Process("SKIM")

# Load the standard set of configuration modules
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(500))
process.options  = cms.untracked.PSet(wantSummary = cms.untracked.bool(True), allowUnscheduled = cms.untracked.bool(True))

if (options.runOnData):  process.GlobalTag.globaltag = '94X_dataRun2_v11' 
else:                    process.GlobalTag.globaltag = '94X_mc2017_realistic_v17' 

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(
        'file:/pnfs/desy.de/cms/tier2/store/mc/RunIIFall17MiniAODv2/GluGluHToMuMu_M125_13TeV_amcatnloFXFX_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/20000/426AEBB4-9042-E811-95DD-1866DAED2E80.root'))
        ##'file:/pnfs/desy.de/cms/tier2/store/data/Run2017B/SingleMuon/MINIAOD/31Mar2018-v1/100000/3C53DB23-5E38-E811-BD21-0025905B855E.root'),)
    
from FSRPhotonRecovery.FSRPhotons.FSRphotonSequence_cff import addFSRphotonSequence
addFSRphotonSequence(process, 'slimmedMuons', options.PhotonMVA)

process.OutputModule = cms.OutputModule("PoolOutputModule",
                                        fileName = cms.untracked.string(options.outputFile),
                                        compressionLevel = cms.untracked.int32(2),
                                        outputCommands = cms.untracked.vstring('drop *',
                                                                               'keep *_FSRRecovery_*_*'
                                                                               ),
                                        SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("ObjectSelection")),
                                        dataset = cms.untracked.PSet(filterName = cms.untracked.string('')),
                                        )

process.ObjectSelection = cms.Path(process.FSRphotonSequence)
    
process.e = cms.EndPath(process.OutputModule)


