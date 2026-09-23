import FWCore.ParameterSet.Config as cms

def customiseNanoGenMinimal(process):
    # 1. Load and configure prunedGenParticles
    process.load('PhysicsTools.PatAlgos.slimming.prunedGenParticles_cfi')
    process.prunedGenParticles.src = cms.InputTag('genParticles')

    # 2. Insert producers into the nanogen sequence
    # Note: Inserting at 0 in reverse order puts prunedGenParticles first, then finalGenParticles
    process.nanogenSequence.insert(0, process.finalGenParticles)
    process.nanogenSequence.insert(0, process.prunedGenParticles)

    # 3. Update genParticleTable input
    process.genParticleTable.src = cms.InputTag('finalGenParticles')

    # 4. Remove 'iso' external variable if present
    if hasattr(process.genParticleTable, 'externalVariables'):
        if hasattr(process.genParticleTable.externalVariables, 'iso'):
            delattr(process.genParticleTable.externalVariables, 'iso')

    # 5. Drop trigger results from output modules if they exist
    for output_module_name in ['NANOEDMAODSIMoutput', 'NANOAODSIMoutput']:
        if hasattr(process, output_module_name):
            getattr(process, output_module_name).outputCommands.append('drop edmTriggerResults_*_*_*')

    return process
