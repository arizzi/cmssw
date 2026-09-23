import FWCore.ParameterSet.Config as cms

# 1. Import slimming modules from PAT
from PhysicsTools.PatAlgos.slimming.genParticles_cff import (
    prunedGenParticlesWithStatusOne,
    prunedGenParticles,
    packedGenParticles,
)
from PhysicsTools.NanoAOD.genparticles_cff import finalGenParticles, genIso, genParticleTable
from PhysicsTools.PatAlgos.slimming.slimmedGenJets_cfi import slimmedGenJets, slimmedGenJetsAK8
from RecoJets.JetProducers.ak8GenJets_cfi import ak8GenJetsConstituents, ak8GenJetsSoftDrop

# 2. Import standard NanoAOD producers and tables
from PhysicsTools.NanoAOD.common_cff import PTVars
from PhysicsTools.NanoAOD.simpleSingletonCandidateFlatTableProducer_cfi import simpleSingletonCandidateFlatTableProducer
from PhysicsTools.NanoAOD.jetMC_cff import (
    jetMCTask,
    jetMCTable,
    fatJetMCTable,
    subjetMCTable,
    genJetFlavourAssociation,
)
from PhysicsTools.NanoAOD.taus_cff import (
    tauGenJetsForNano,
    tauGenJetsSelectorAllHadronsForNano,
    genVisTaus,
    genVisTauTable,
)
from PhysicsTools.NanoAOD.globals_cff import genTable
from PhysicsTools.NanoAOD.genWeightsTable_cfi import genWeightsTable
from PhysicsTools.NanoAOD.particlelevel_cff import lheInfoTable
from PhysicsTools.NanoAOD.particlelevel_cff import (
    particleLevel,
    genParticles2HepMC,
    genParticles2HepMCHiggsVtx,
    rivetProducerHTXS,
    rivetLeptonTable,
    rivetPhotonTable,
    HTXSCategoryTable,
    particleLevelTask,
    particleLevelTablesTask,
)


def _customizeNanoAodGEN(process, isFromGEN=True):
    genTask = cms.Task()

    # ----------------------------------------------------
    # 1. GenParticles + Isolation (GenPart_iso)
    # ----------------------------------------------------
    if isFromGEN:
        # Standard PAT slimming to produce packedGenParticles from genParticles
        process.prunedGenParticlesWithStatusOne = prunedGenParticlesWithStatusOne.clone()
        process.prunedGenParticles = prunedGenParticles.clone(src = "prunedGenParticlesWithStatusOne")
        process.packedGenParticles = packedGenParticles.clone(
            inputCollection = "prunedGenParticlesWithStatusOne",
            map = "prunedGenParticles",
            inputOriginal = "genParticles",
        )
        process.finalGenParticles = finalGenParticles.clone(src = "prunedGenParticles")

        # Produce generator isolation
        process.genIso = genIso.clone(
            genPart = "finalGenParticles",
            packedGenPart = "packedGenParticles",
        )
        genTask.add(
            process.prunedGenParticlesWithStatusOne,
            process.prunedGenParticles,
            process.packedGenParticles,
            process.finalGenParticles,
            process.genIso,
        )
    else:
        # On MiniAOD, prunedGenParticles and packedGenParticles are already present
        if not hasattr(process, "finalGenParticles"):
            process.finalGenParticles = finalGenParticles.clone(src = "prunedGenParticles")
        process.genIso = genIso.clone(
            genPart = "finalGenParticles",
            packedGenPart = "packedGenParticles",
        )
        genTask.add(process.finalGenParticles, process.genIso)

    # genParticleTable keeps externalVariables.iso -> writes GenPart_iso
    process.genParticleTable = genParticleTable.clone(src = "finalGenParticles")
    genTask.add(process.genParticleTable)

    # ----------------------------------------------------
    # 2. GenJets (AK4, AK8, TrackGenJets & Soft Activity)
    # ----------------------------------------------------
    if isFromGEN:
        # ak4GenJetsNoNu and ak8GenJetsNoNu already exist (from pgen or step_gen.root)
        process.slimmedGenJets = slimmedGenJets.clone(src = "ak4GenJetsNoNu", cut = "pt > 8")
        process.slimmedGenJetsAK8 = slimmedGenJetsAK8.clone(src = "ak8GenJetsNoNu", cut = "pt > 100")
        process.ak8GenJetsNoNuConstituents = ak8GenJetsConstituents.clone(src = "ak8GenJetsNoNu")
        process.ak8GenJetsNoNuSoftDrop = ak8GenJetsSoftDrop.clone(
            src = cms.InputTag("ak8GenJetsNoNuConstituents", "constituents")
        )
        genTask.add(
            process.slimmedGenJets,
            process.slimmedGenJetsAK8,
            process.ak8GenJetsNoNuConstituents,
            process.ak8GenJetsNoNuSoftDrop,
        )

        # In pure GEN, wire flavour clustering & subjets directly (instead of reading from MiniAOD)
        process.genJetFlavourTable.jetFlavourInfos = cms.InputTag("genJetFlavourAssociation")
        process.genSubJetAK8Table.src = cms.InputTag("ak8GenJetsNoNuSoftDrop", "SubJets")

    # Clone the entire jetMCTask from jetMC_cff and drop only the RECO extension tables
    pureGenJetTask = jetMCTask.copy()
    pureGenJetTask.remove(jetMCTable)
    pureGenJetTask.remove(fatJetMCTable)
    pureGenJetTask.remove(subjetMCTable)
    pureGenJetTask.add(genJetFlavourAssociation)

    genTask.add(pureGenJetTask)

    # ----------------------------------------------------
    # 3. GenMET (reco::GenMET -> GenMET table)
    # ----------------------------------------------------
    process.genMetTable = simpleSingletonCandidateFlatTableProducer.clone(
        src = cms.InputTag("genMetTrue"),
        name = cms.string("GenMET"),
        doc = cms.string("Gen MET"),
        variables = cms.PSet(PTVars),
    )
    genTask.add(process.genMetTable)

    # ----------------------------------------------------
    # 4. Visible GenTaus (GenVisTau)
    # ----------------------------------------------------
    tauSrc = "prunedGenParticles" if isFromGEN else "finalGenParticles"

    process.tauGenJetsForNano = tauGenJetsForNano.clone(
        GenParticles = cms.InputTag(tauSrc)
    )
    process.tauGenJetsSelectorAllHadronsForNano = tauGenJetsSelectorAllHadronsForNano.clone(
        src = cms.InputTag("tauGenJetsForNano")
    )
    process.genVisTaus = genVisTaus.clone(
        src = cms.InputTag("tauGenJetsSelectorAllHadronsForNano"),
        srcGenParticles = cms.InputTag("finalGenParticles"),
    )
    process.genVisTauTable = genVisTauTable.clone(
        src = cms.InputTag("genVisTaus")
    )

    genTask.add(
        process.tauGenJetsForNano,
        process.tauGenJetsSelectorAllHadronsForNano,
        process.genVisTaus,
        process.genVisTauTable,
    )

    # ----------------------------------------------------
    # 5. Event Weights & LHE Info
    # ----------------------------------------------------
    process.genTable = genTable.clone()
    process.genWeightsTable = genWeightsTable.clone()
    process.lheInfoTable = lheInfoTable.clone()

    genTask.add(
        process.genTable,
        process.genWeightsTable,
        process.lheInfoTable,
    )

    # ----------------------------------------------------
    # 6. ParticleLevel (GenDressedLepton, GenIsolatedPhoton, HTXS)
    # ----------------------------------------------------
    if isFromGEN:
        # In pure GEN, feed raw genParticles directly to the HepMC converters
        process.genParticles2HepMC = genParticles2HepMC.clone(
            genParticles = cms.InputTag("genParticles")
        )
        process.genParticles2HepMCHiggsVtx = genParticles2HepMCHiggsVtx.clone(
            genParticles = cms.InputTag("genParticles")
        )
        process.particleLevel = particleLevel.clone(
            src = cms.InputTag("genParticles2HepMC:unsmeared")
        )
        process.rivetProducerHTXS = rivetProducerHTXS.clone(
            HepMCCollection = cms.InputTag("genParticles2HepMCHiggsVtx:unsmeared")
        )
        process.rivetLeptonTable = rivetLeptonTable.clone()
        process.rivetPhotonTable = rivetPhotonTable.clone()
        process.HTXSCategoryTable = HTXSCategoryTable.clone()

        genTask.add(
            process.genParticles2HepMC,
            process.genParticles2HepMCHiggsVtx,
            process.particleLevel,
            process.rivetProducerHTXS,
            process.rivetLeptonTable,
            process.rivetPhotonTable,
            process.HTXSCategoryTable,
        )
    else:
        # On MiniAOD, use the standard particleLevel tasks
        genTask.add(particleLevelTask, particleLevelTablesTask)

    # ----------------------------------------------------
    # 7. Bind Task to nanogenSequence and clean outputs
    # ----------------------------------------------------
    process.nanogenTask = genTask
    process.nanogenSequence = cms.Sequence(process.nanogenTask)

    if hasattr(process, "nanoAOD_step"):
        process.nanoAOD_step.associate(genTask)

    for outName in ["NANOEDMAODSIMoutput", "NANOAODSIMoutput"]:
        if hasattr(process, outName):
            getattr(process, outName).outputCommands.append("drop edmTriggerResults_*_*_*")

    return process


def customizeNanoAodGEN(process):
    return _customizeNanoAodGEN(process, isFromGEN=True)


def customizeNanoAodGENFromMini(process):
    return _customizeNanoAodGEN(process, isFromGEN=False)
