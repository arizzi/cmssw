import FWCore.ParameterSet.Config as cms
process = cms.Process("PV")
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.StandardSequences.Geometry_cff") #old one, to use for old releases
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.GlobalTag.globaltag = 'POSTLS172_V4::All'


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    'file:/scratch/arizzi/pvchoice/CMSSW_7_2_2_patch2/src/CommonTools/ParticleFlow/test/many/ZH_HToBB_ZToNuNu_M-125_13TeV_powheg-herwigpp-PU40bx25_PHYS14_25_V1-v1-40778748-2072-E411-8840-00266CFEFE1C.root'
    )
)


process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule(
    "PoolOutputModule",
    process.AODSIMEventContent,
    fileName = cms.untracked.string('AOD.root'),
    )
process.out.outputCommands.extend(
    [
      'keep *'
    ])
process.load("CommonTools.RecoAlgos.sortedPrimaryVertices_cfi")
process.load("CommonTools.RecoAlgos.sortedPFPrimaryVertices_cfi")

process.sortedPrimaryVertices.particles="trackRefsForJetsBeforeSorting"
process.sortedPrimaryVertices.jets = "ak4CaloJets"
process.sortedPFPrimaryVerticesNoMET = process.sortedPFPrimaryVertices.clone()
process.sortedPFPrimaryVerticesNoMET.sorting.useMet = False
process.sortedPrimaryVerticesNoMET = process.sortedPrimaryVertices.clone(jets="ak4CaloJets")
process.sortedPrimaryVerticesNoMET.sorting.useMet = False

process.p = cms.Path(
        process.trackWithVertexRefSelectorBeforeSorting*
        process.trackRefsForJetsBeforeSorting*
        process.sortedPFPrimaryVertices*process.sortedPrimaryVertices*process.sortedPFPrimaryVerticesNoMET*process.sortedPrimaryVerticesNoMET)

process.endpath = cms.EndPath(
    process.out
    )



