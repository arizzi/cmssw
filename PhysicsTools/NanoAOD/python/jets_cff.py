import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Modifier_run2_miniAOD_80XLegacy_cff import run2_miniAOD_80XLegacy
from Configuration.Eras.Modifier_run2_nanoAOD_92X_cff import run2_nanoAOD_92X

from  PhysicsTools.NanoAOD.common_cff import *



##################### User floats producers, selectors ##########################
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets

chsForSATkJets = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string('charge()!=0 && pvAssociationQuality()>=5 && vertexRef().key()==0'))
softActivityJets = ak4PFJets.clone(src = 'chsForSATkJets', doAreaFastjet = False, jetPtMin=1) 
softActivityJets10 = cms.EDFilter("CandPtrSelector", src = cms.InputTag("chsForSATkJets"), cut = cms.string('pt>10'))
softActivityJets5 = cms.EDFilter("CandPtrSelector", src = cms.InputTag("chsForSATkJets"), cut = cms.string('pt>5'))
softActivityJets2 = cms.EDFilter("CandPtrSelector", src = cms.InputTag("chsForSATkJets"), cut = cms.string('pt>2'))

looseJetId = cms.EDProducer("PatJetIDValueMapProducer",
			  filterParams=cms.PSet(
			    version = cms.string('WINTER16'),
			    quality = cms.string('LOOSE'),
			  ),
                          src = cms.InputTag("slimmedJets")
)
tightJetId = cms.EDProducer("PatJetIDValueMapProducer",
			  filterParams=cms.PSet(
			    version = cms.string('WINTER17'),
			    quality = cms.string('TIGHT'),
			  ),
                          src = cms.InputTag("slimmedJets")
)
run2_miniAOD_80XLegacy.toModify( tightJetId.filterParams, version = "WINTER16" )

tightJetIdLepVeto = cms.EDProducer("PatJetIDValueMapProducer",
			  filterParams=cms.PSet(
			    version = cms.string('WINTER17'),
			    quality = cms.string('TIGHTLEPVETO'),
			  ),
                          src = cms.InputTag("slimmedJets")
)

looseJetIdAK8 = cms.EDProducer("PatJetIDValueMapProducer",
			  filterParams=cms.PSet(
			    version = cms.string('WINTER16'),
			    quality = cms.string('LOOSE'),
			  ),
                          src = cms.InputTag("slimmedJetsAK8")
)
tightJetIdAK8 = cms.EDProducer("PatJetIDValueMapProducer",
			  filterParams=cms.PSet(
			    version = cms.string('WINTER17'),
			    quality = cms.string('TIGHT'),
			  ),
                          src = cms.InputTag("slimmedJetsAK8")
)
run2_miniAOD_80XLegacy.toModify( tightJetIdAK8.filterParams, version = "WINTER16" )

tightJetIdLepVetoAK8 = cms.EDProducer("PatJetIDValueMapProducer",
			  filterParams=cms.PSet(
			    version = cms.string('WINTER17'),
			    quality = cms.string('TIGHTLEPVETO'),
			  ),
                          src = cms.InputTag("slimmedJetsAK8")
)

bJetVars = cms.EDProducer("JetRegressionVarProducer",
    pvsrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    src = cms.InputTag("slimmedJets"),    
    svsrc = cms.InputTag("slimmedSecondaryVertices"),
    gpsrc = cms.InputTag("prunedGenParticles"),
    #musrc = cms.InputTag("slimmedMuons"),
    #elesrc = cms.InputTag("slimmedElectrons")
)


slimmedJetsWithUserData = cms.EDProducer("PATJetUserDataEmbedder",
     src = cms.InputTag("slimmedJets"),
     userFloats = cms.PSet(
         leadTrackPt = cms.InputTag("bJetVars:leadTrackPt"),
         leptonPtRel = cms.InputTag("bJetVars:leptonPtRel"),
         leptonPtRatio = cms.InputTag("bJetVars:leptonPtRatio"),
         leptonPtRelInv = cms.InputTag("bJetVars:leptonPtRelInv"),
         leptonPtRelv0 = cms.InputTag("bJetVars:leptonPtRelv0"),
         leptonPtRatiov0 = cms.InputTag("bJetVars:leptonPtRatiov0"),
         leptonPtRelInvv0 = cms.InputTag("bJetVars:leptonPtRelInvv0"),
         leptonDeltaR = cms.InputTag("bJetVars:leptonDeltaR"),
         leptonPt = cms.InputTag("bJetVars:leptonPt"),
         vtxPt = cms.InputTag("bJetVars:vtxPt"),
         vtxMass = cms.InputTag("bJetVars:vtxMass"),
         vtx3dL = cms.InputTag("bJetVars:vtx3dL"),
         vtx3deL = cms.InputTag("bJetVars:vtx3deL"),
         ptD = cms.InputTag("bJetVars:ptD"),
         genPtwNu = cms.InputTag("bJetVars:genPtwNu"),
         
         ),
     userInts = cms.PSet(
        tightId = cms.InputTag("tightJetId"),
        tightIdLepVeto = cms.InputTag("tightJetIdLepVeto"),
        vtxNtrk = cms.InputTag("bJetVars:vtxNtrk"),
        leptonPdgId = cms.InputTag("bJetVars:leptonPdgId"),
     ),
)
run2_miniAOD_80XLegacy.toModify( slimmedJetsWithUserData.userInts, 
        looseId = cms.InputTag("looseJetId"),
        tightIdLepVeto = None,
)

slimmedJetsAK8WithUserData = cms.EDProducer("PATJetUserDataEmbedder",
     src = cms.InputTag("slimmedJetsAK8"),
     userFloats = cms.PSet(),
     userInts = cms.PSet(
        tightId = cms.InputTag("tightJetIdAK8"),
        tightIdLepVeto = cms.InputTag("tightJetIdLepVetoAK8"),
     ),
)
run2_miniAOD_80XLegacy.toModify( slimmedJetsAK8WithUserData.userInts, 
        looseId = cms.InputTag("looseJetIdAK8"),
        tightIdLepVeto = None,
)

from  PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
# Note: Safe to always add 'L2L3Residual' as MC contains dummy L2L3Residual corrections (always set to 1)
#      (cf. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CMSSW_7_6_4_and_above )
jetCorrFactors = patJetCorrFactors.clone(src='slimmedJetsWithUserData',
    levels = cms.vstring('L1FastJet',
        'L2Relative',
        'L3Absolute',
	'L2L3Residual'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
jetCorrFactorsAK8 = patJetCorrFactors.clone(src='slimmedJetsAK8WithUserData',
    levels = cms.vstring('L1FastJet',
        'L2Relative',
        'L3Absolute',
	'L2L3Residual'),
    payload = cms.string('AK8PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

from  PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import *
updatedJets = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsWithUserData',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactors") ),
)

finalJets = cms.EDFilter("PATJetRefSelector",
    src = cms.InputTag("updatedJets"),
    cut = cms.string("pt > 15")
)

updatedJetsAK8 = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsAK8WithUserData',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorsAK8") ),
)

finalJetsAK8 = cms.EDFilter("PATJetRefSelector",
    src = cms.InputTag("updatedJetsAK8"),
    cut = cms.string("pt > 170")
)





##################### Tables for final output and docs ##########################



jetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("linkedObjects","jets"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name = cms.string("Jet"),
    doc  = cms.string("slimmedJets, i.e. ak4 PFJets CHS with JECs applied, after basic selection (" + finalJets.cut.value()+")"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    externalVariables = cms.PSet(
        bReg = ExtVar(cms.InputTag("bjetMVA"),float, doc="pt corrected with b-jet regression",precision=14),
        bRegNN= ExtVar(cms.InputTag("bjetNN:corrNNnoJEC"),float, doc="pt corrected with b-jet regression",precision=14),
        bRegNN2 = ExtVar(cms.InputTag("bjetNN2:corr"),float, doc="pt corrected with b-jet regression",precision=14),
        bRegNN2res = ExtVar(cms.InputTag("bjetNN2:res"),float, doc="res on pt corrected with b-jet regression",precision=14),
    ),
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        nMuons = Var("?hasOverlaps('muons')?overlaps('muons').size():0", int, doc="number of muons in the jet"),
        muonIdx1 = Var("?overlaps('muons').size()>0?overlaps('muons')[0].key():-1", int, doc="index of first matching muon"),
        muonIdx2 = Var("?overlaps('muons').size()>1?overlaps('muons')[1].key():-1", int, doc="index of second matching muon"),
        electronIdx1 = Var("?overlaps('electrons').size()>0?overlaps('electrons')[0].key():-1", int, doc="index of first matching electron"),
        electronIdx2 = Var("?overlaps('electrons').size()>1?overlaps('electrons')[1].key():-1", int, doc="index of second matching electron"),
        nElectrons = Var("?hasOverlaps('electrons')?overlaps('electrons').size():0", int, doc="number of electrons in the jet"),
        btagCMVA = Var("bDiscriminator('pfCombinedMVAV2BJetTags')",float,doc="CMVA V2 btag discriminator",precision=10),
        btagDeepB = Var("bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')",float,doc="DeepCSV b+bb tag discriminator",precision=10),
        btagCSVV2 = Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",float,doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)",precision=10),
        btagDeepC = Var("bDiscriminator('pfDeepCSVJetTags:probc')",float,doc="DeepCSV charm btag discriminator",precision=10),
        #puIdDisc = Var("userFloat('pileupJetId:fullDiscriminant')",float,doc="Pilup ID discriminant",precision=10),
        puId = Var("userInt('pileupJetId:fullId')",int,doc="Pilup ID flags"),
        jetId = Var("userInt('tightId')*2+4*userInt('tightIdLepVeto')",int,doc="Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"),
        qgl = Var("userFloat('QGTagger:qgLikelihood')",float,doc="Quark vs Gluon likelihood discriminator",precision=10),
        nConstituents = Var("numberOfDaughters()",int,doc="Number of particles in the jet"),
        rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
        chHEF = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision= 6),
        neHEF = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision= 6),
        chEmEF = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision= 6),
        neEmEF = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision= 6),
        leadTrackPt = Var("userFloat('leadTrackPt')", float, doc="leading Track pT", precision= 10),
        leptonPtRel = Var("userFloat('leptonPtRel')", float, doc="leptonPtRel", precision= 10),
        leptonPtRelInv = Var("userFloat('leptonPtRelInv')", float, doc="leptonPtRelInv", precision= 10),
        leptonPtRatio = Var("userFloat('leptonPtRatio')", float, doc="leptonPtRatio", precision= 10),
        leptonPtRelv0 = Var("userFloat('leptonPtRelv0')", float, doc="leptonPtRel from heppy", precision= 10),
        leptonPtRelInvv0 = Var("userFloat('leptonPtRelInvv0')", float, doc="leptonPtRelInv from heppy", precision= 10),
        leptonPtRatiov0 = Var("userFloat('leptonPtRatiov0')", float, doc="leptonPtRatio from heppy", precision= 10),
        leptonPt = Var("userFloat('leptonPt')", float, doc="leptonPt", precision= 10),
        leptonDeltaR = Var("userFloat('leptonDeltaR')", float, doc="lepton dR", precision= 10),
        leptonPdgId = Var("userInt('leptonPdgId')", float, doc="leptonPdgId"),
        vtxPt = Var("userFloat('vtxPt')", float, doc="max SIP vtx pT", precision= 10),
        vtxMass = Var("userFloat('vtxMass')", float, doc="max SIP vtx mass", precision= 10),
        vtx3dL = Var("userFloat('vtx3dL')", float, doc="max SIP vtx 3d ip", precision= 10),
        vtx3deL = Var("userFloat('vtx3deL')", float, doc="max SIP vtx 3d iperr", precision= 10),
        vtxNtrk = Var("userInt('vtxNtrk')", float, doc="max SIP vtx ntracks"),
        ptD = Var("userFloat('ptD')",float,doc="qgl input ptD",precision=10),
        genPtwNu = Var("userFloat('genPtwNu')",float,doc="regression target",precision=10),
        JEC1 = Var("jecFactor('L1FastJet')",float,doc="jec..",precision=6),
        JEC2 = Var("jecFactor('L2Relative')",float,doc="jec..",precision=6),
        JEC3 = Var("jecFactor('L3Absolute')",float,doc="jec..",precision=6),
        ##ptD #JEC #leptonptrelinv, ptrel, 
    )
)

#jets are not as precise as muons
jetTable.variables.pt.precision=10

### Era dependent customization
run2_miniAOD_80XLegacy.toModify( slimmedJetsWithUserData, userFloats=cms.PSet(qgl=cms.InputTag('qgtagger80x:qgLikelihood')))
run2_miniAOD_80XLegacy.toModify( jetTable.variables.qgl, expr="userFloat('qgl')" )
run2_miniAOD_80XLegacy.toModify( jetTable.variables, jetId = Var("userInt('tightId')*2+userInt('looseId')",int,doc="Jet ID flags bit1 is loose, bit2 is tight"))

bjetMVA= cms.EDProducer("BJetEnergyRegressionMVA",
    backend = cms.string("TMVA"),
    src = cms.InputTag("linkedObjects","jets"),
    pvsrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    svsrc = cms.InputTag("slimmedSecondaryVertices"),
    rhosrc = cms.InputTag("fixedGridRhoFastjetAll"),
    weightFile =  cms.FileInPath("PhysicsTools/NanoAOD/data/bjet-regression.xml"),
    name = cms.string("JetReg"),
    isClassifier = cms.bool(False),
    variablesOrder = cms.vstring(["Jet_pt","nPVs","Jet_eta","Jet_mt","Jet_leadTrackPt","Jet_leptonPtRel","Jet_leptonPt","Jet_leptonDeltaR","Jet_neHEF","Jet_neEmEF","Jet_vtxPt","Jet_vtxMass","Jet_vtx3dL","Jet_vtxNtrk","Jet_vtx3deL"]),
    variables = cms.PSet(
	Jet_pt = cms.string("pt"),
	Jet_eta = cms.string("eta"),
	Jet_mt = cms.string("mt"),
    Jet_leadTrackPt = cms.string("userFloat('leadTrackPt')"),
    Jet_vtxNtrk = cms.string("userInt('vtxNtrk')"),
    Jet_vtxMass = cms.string("userFloat('vtxMass')"),
    Jet_vtx3dL = cms.string("userFloat('vtx3dL')"),
    Jet_vtx3deL = cms.string("userFloat('vtx3deL')"),
    Jet_vtxPt = cms.string("userFloat('vtxPt')"),
    Jet_leptonPtRel = cms.string("userFloat('leptonPtRelv0')"),
	Jet_leptonPt = cms.string("?overlaps('muons').size()>0?overlaps('muons')[0].pt():(?overlaps('electrons').size()>0?overlaps('electrons')[0].pt():0)"),
	Jet_neHEF = cms.string("neutralHadronEnergy()/energy()"),
	Jet_neEmEF = cms.string("neutralEmEnergy()/energy()"),
	Jet_leptonDeltaR = cms.string('''?overlaps('muons').size()>0?deltaR(eta,phi,overlaps('muons')[0].eta,overlaps('muons')[0].phi):
				(?overlaps('electrons').size()>0?deltaR(eta,phi,overlaps('electrons')[0].eta,overlaps('electrons')[0].phi):
				0)'''),
    )

)

norms={u'Jet_chHEF': {u'scale': u'5.3589148912', u'offset': u'-0.570554520102'}, u'Jet_vtxPt': {u'scale': u'0.0512038544596', u'offset': u'-17.3379903923'}, u'Jet_vtxNtrk': {u'scale': u'0.491718281889', u'offset': u'-2.34592626061'}, u'Jet_vtx3deL': {u'scale': u'0.0436824436176', u'offset': u'-16.271010024'}, u'Jet_mt': {u'scale': u'0.0192136466589', u'offset': u'-79.5289027235'}, u'Jet_pt': {u'scale': u'0.0193607564269', u'offset': u'-78.5768487322'}, u'Jet_chEmEF': {u'scale': u'9.5492257452', u'offset': u'-0.0388051523025'}, u'Jet_leptonPtRelInv': {u'scale': u'0.287916371059', u'offset': u'-1.52232979489'}, u'Jet_leptonPt': {u'scale': u'0.0833792294794', u'offset': u'-5.3682820854'}, u'nPVs': {u'scale': u'0.138597756712', u'offset': u'-19.1268252508'}, u'Jet_neHEF': {u'scale': u'10.1788027231', u'offset': u'-0.0823817629694'}, u'Jet_leadTrackPt': {u'scale': u'0.0754859677842', u'offset': u'-16.1239589574'}, u'Jet_eta': {u'scale': u'0.88415389899', u'offset': u'-0.000656532933447'}, u'Jet_mass': {u'scale': u'0.13977195521', u'offset': u'-11.8468109055'}, u'Jet_vtxMass': {u'scale': u'0.881275866253', u'offset': u'-1.19430690076'}, u'Jet_neEmEF': {u'scale': u'6.54513832092', u'offset': u'-0.273723323526'}, u'Jet_leptonDeltaR': {u'scale': u'26.6190777888', u'offset': u'-0.0199096893219'}, u'Jet_leptonPtRel': {u'scale': u'1.37953633485', u'offset': u'-0.306057605907'}, u'Jet_vtx3dL': {u'scale': u'0.951663423918', u'offset': u'-0.700124323902'}, u'Jet_leptonPdgId': {u'scale': u'1.44580953594', u'offset': u'0.59152841422'}, u'Jet_ptd': {u'scale': u'1.16819217799', u'offset': u'-0.369127101198'}} 

bjetNN= cms.EDProducer("BJetEnergyRegressionMVA",
    backend = cms.string("TF"),
    src = cms.InputTag("linkedObjects","jets"),
    pvsrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    svsrc = cms.InputTag("slimmedSecondaryVertices"),
    rhosrc = cms.InputTag("fixedGridRhoFastjetAll"),
    weightFile =  cms.FileInPath("PhysicsTools/NanoAOD/data/model_noJec.pb"),
    name = cms.string("JetRegNN"),
    isClassifier = cms.bool(False),
    variablesOrder = cms.vstring(["Jet_pt", "Jet_mt", "Jet_eta", "Jet_mass", "Jet_ptd", "Jet_chHEF", "Jet_neHEF", "Jet_chEmEF", "Jet_neEmEF", "Jet_leadTrackPt", "nPVs", "Jet_vtxNtrk", "Jet_vtxMass", "Jet_vtx3dL", "Jet_vtx3deL", "Jet_vtxPt", "Jet_leptonPt", "Jet_leptonPtRel", "Jet_leptonPtRelInv", "Jet_leptonDeltaR", "Jet_leptonPdgId"]),
    variables = cms.PSet(
    Jet_pt = cms.string("pt"),
    Jet_mt = cms.string("mt"),
    Jet_eta = cms.string("eta"),
    Jet_mass = cms.string("mass"),
    Jet_ptd = cms.string("userFloat('ptD')"),
    Jet_leadTrackPt = cms.string("userFloat('leadTrackPt')"),
    Jet_vtxNtrk = cms.string("userInt('vtxNtrk')"),
    Jet_vtxMass = cms.string("userFloat('vtxMass')"),
    Jet_vtx3dL = cms.string("userFloat('vtx3dL')"),
    Jet_vtx3deL = cms.string("userFloat('vtx3deL')"),
    Jet_vtxPt = cms.string("userFloat('vtxPt')"),
    Jet_leptonPt = cms.string("userFloat('leptonPt')"),
    Jet_leptonPtRel = cms.string("userFloat('leptonPtRelv0')"),
    Jet_leptonPtRelInv = cms.string("userFloat('leptonPtRelInvv0')"),
    Jet_leptonDeltaR = cms.string("userFloat('leptonDeltaR')"),
    Jet_leptonPdgId = cms.string("userInt('leptonPdgId')"),
    Jet_neHEF = cms.string("neutralHadronEnergy()/energy()"),
    Jet_neEmEF = cms.string("neutralEmEnergy()/energy()"),
    Jet_chHEF = cms.string("chargedHadronEnergy()/energy()"),
    Jet_chEmEF = cms.string("chargedEmEnergy()/energy()"),

    ),
     inputTensorName = cms.string("dense_1_input"),
     outputTensorName = cms.string("output_node0"),
     outputNames = cms.vstring(["corrNNnoJEC"]),
     outputFormulas = cms.vstring(["at(0)"]),
     nThreads = cms.uint32(1),
     singleThreadPool = cms.string("no_threads"),
)

for k in norms:
 try:
  var=getattr(bjetNN.variables,k)
  val=var.value()
  updatedString="(%s+(%s))*%s"%(val,norms[k]["offset"],norms[k]["scale"])
  var.setValue(updatedString.encode("utf8"))
  #print k, var.value()
 except:
  pass

bjetNN2= cms.EDProducer("BJetEnergyRegressionMVA",
    backend = cms.string("TF"),
    src = cms.InputTag("linkedObjects","jets"),
    pvsrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    svsrc = cms.InputTag("slimmedSecondaryVertices"),
    rhosrc = cms.InputTag("fixedGridRhoFastjetAll"),

    weightFile =  cms.FileInPath("PhysicsTools/NanoAOD/data/breg_training_2017.pb"),
    name = cms.string("JetRegNN"),
    isClassifier = cms.bool(False),
    variablesOrder = cms.vstring(["Jet_pt","Jet_eta","rho","Jet_mt","Jet_leadTrackPt","Jet_leptonPtRel","Jet_leptonDeltaR","Jet_neHEF","Jet_neEmEF","Jet_vtxPt","Jet_vtxMass","Jet_vtx3dL","Jet_vtxNtrk","Jet_vtx3deL","Jet_numDaughters_pt03","Jet_energyRing_dR0_em_Jet_rawEnergy","Jet_energyRing_dR1_em_Jet_rawEnergy","Jet_energyRing_dR2_em_Jet_rawEnergy","Jet_energyRing_dR3_em_Jet_rawEnergy","Jet_energyRing_dR4_em_Jet_rawEnergy","Jet_energyRing_dR0_neut_Jet_rawEnergy","Jet_energyRing_dR1_neut_Jet_rawEnergy","Jet_energyRing_dR2_neut_Jet_rawEnergy","Jet_energyRing_dR3_neut_Jet_rawEnergy","Jet_energyRing_dR4_neut_Jet_rawEnergy","Jet_energyRing_dR0_ch_Jet_rawEnergy","Jet_energyRing_dR1_ch_Jet_rawEnergy","Jet_energyRing_dR2_ch_Jet_rawEnergy","Jet_energyRing_dR3_ch_Jet_rawEnergy","Jet_energyRing_dR4_ch_Jet_rawEnergy","Jet_energyRing_dR0_mu_Jet_rawEnergy","Jet_energyRing_dR1_mu_Jet_rawEnergy","Jet_energyRing_dR2_mu_Jet_rawEnergy","Jet_energyRing_dR3_mu_Jet_rawEnergy","Jet_energyRing_dR4_mu_Jet_rawEnergy","Jet_chHEF","Jet_chEmEF","Jet_leptonPtRelInv","isEle","isMu","isOther","Jet_mass","Jet_ptd"]),
    variables = cms.PSet(
    Jet_pt = cms.string("pt*jecFactor('Uncorrected')"),
    Jet_mt = cms.string("mt*jecFactor('Uncorrected')"),
    Jet_eta = cms.string("eta"),
    Jet_mass = cms.string("mass*jecFactor('Uncorrected')"),
    Jet_ptd = cms.string("userFloat('ptD')"),
    Jet_leadTrackPt = cms.string("userFloat('leadTrackPt')"),
    Jet_vtxNtrk = cms.string("userInt('vtxNtrk')"),
    Jet_vtxMass = cms.string("userFloat('vtxMass')"),
    Jet_vtx3dL = cms.string("userFloat('vtx3dL')"),
    Jet_vtx3deL = cms.string("userFloat('vtx3deL')"),
    Jet_vtxPt = cms.string("userFloat('vtxPt')"),
    #Jet_leptonPt = cms.string("userFloat('leptonPt')"),
    Jet_leptonPtRel = cms.string("userFloat('leptonPtRelv0')"),
    Jet_leptonPtRelInv = cms.string("userFloat('leptonPtRelInvv0')*jecFactor('Uncorrected')"),
    Jet_leptonDeltaR = cms.string("userFloat('leptonDeltaR')"),
    #Jet_leptonPdgId = cms.string("userInt('leptonPdgId')"),
    Jet_neHEF = cms.string("neutralHadronEnergy()/energy()"),
    Jet_neEmEF = cms.string("neutralEmEnergy()/energy()"),
    Jet_chHEF = cms.string("chargedHadronEnergy()/energy()"),
    Jet_chEmEF = cms.string("chargedEmEnergy()/energy()"),

    ),
     inputTensorName = cms.string("ffwd_inp"),
     outputTensorName = cms.string("ffwd_out/BiasAdd"),
     outputNames = cms.vstring(["corr","res"]),
     outputFormulas = cms.vstring(["at(0)*0.39077115058898926+1.0610932111740112","0.5*(at(2)-at(1))*0.39077115058898926"]),
     nThreads = cms.uint32(1),
     singleThreadPool = cms.string("no_threads"),
)



EnergyRingsTable = cms.EDProducer("EnergyRingsTableProducer",
    name = cms.string("Jet"),
   # src = cms.InputTag("slimmedJets"),
    src = cms.InputTag("linkedObjects","jets"),
)

##### Soft Activity tables
saJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("softActivityJets"),
    cut = cms.string(""),
    maxLen = cms.uint32(6),
    name = cms.string("SoftActivityJet"),
    doc  = cms.string("jets clustered from charged candidates compatible with primary vertex (" + chsForSATkJets.cut.value()+")"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P3Vars,
  )
)

saJetTable.variables.pt.precision=10
saJetTable.variables.eta.precision=8
saJetTable.variables.phi.precision=8

saTable = cms.EDProducer("GlobalVariablesTableProducer",
    variables = cms.PSet(
        SoftActivityJetHT = ExtVar( cms.InputTag("softActivityJets"), "candidatescalarsum", doc = "scalar sum of soft activity jet pt, pt>1" ),
        SoftActivityJetHT10 = ExtVar( cms.InputTag("softActivityJets10"), "candidatescalarsum", doc = "scalar sum of soft activity jet pt , pt >10"  ),
        SoftActivityJetHT5 = ExtVar( cms.InputTag("softActivityJets5"), "candidatescalarsum", doc = "scalar sum of soft activity jet pt, pt>5"  ),
        SoftActivityJetHT2 = ExtVar( cms.InputTag("softActivityJets2"), "candidatescalarsum", doc = "scalar sum of soft activity jet pt, pt >2"  ),
        SoftActivityJetNjets10 = ExtVar( cms.InputTag("softActivityJets10"), "candidatesize", doc = "number of soft activity jet pt, pt >2"  ),
        SoftActivityJetNjets5 = ExtVar( cms.InputTag("softActivityJets5"), "candidatesize", doc = "number of soft activity jet pt, pt >5"  ),
        SoftActivityJetNjets2 = ExtVar( cms.InputTag("softActivityJets2"), "candidatesize", doc = "number of soft activity jet pt, pt >10"  ),

    )
)



## BOOSTED STUFF #################
fatJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("finalJetsAK8"),
    cut = cms.string(" pt > 170"), #probably already applied in miniaod
    name = cms.string("FatJet"),
    doc  = cms.string("slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        jetId = Var("userInt('tightId')*2+4*userInt('tightIdLepVeto')",int,doc="Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"),
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        tau1 = Var("userFloat('NjettinessAK8Puppi:tau1')",float, doc="Nsubjettiness (1 axis)",precision=10),
        tau2 = Var("userFloat('NjettinessAK8Puppi:tau2')",float, doc="Nsubjettiness (2 axis)",precision=10),
        tau3 = Var("userFloat('NjettinessAK8Puppi:tau3')",float, doc="Nsubjettiness (3 axis)",precision=10),
        tau4 = Var("userFloat('NjettinessAK8Puppi:tau4')",float, doc="Nsubjettiness (4 axis)",precision=10),
        n2b1 = Var("userFloat('ak8PFJetsPuppiSoftDropValueMap:nb1AK8PuppiSoftDropN2')", float, doc="N2 with beta=1", precision=10),
        n3b1 = Var("userFloat('ak8PFJetsPuppiSoftDropValueMap:nb1AK8PuppiSoftDropN3')", float, doc="N3 with beta=1", precision=10),
        msoftdrop = Var("groomedMass('SoftDropPuppi')",float, doc="Corrected soft drop mass with PUPPI",precision=10),
        btagCMVA = Var("bDiscriminator('pfCombinedMVAV2BJetTags')",float,doc="CMVA V2 btag discriminator",precision=10),
        btagDeepB = Var("bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')",float,doc="DeepCSV b+bb tag discriminator",precision=10),
        btagCSVV2 = Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",float,doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)",precision=10),
        btagHbb = Var("bDiscriminator('pfBoostedDoubleSecondaryVertexAK8BJetTags')",float,doc="Higgs to BB tagger discriminator",precision=10),
        subJetIdx1 = Var("?numberOfSourceCandidatePtrs()>0 && sourceCandidatePtr(0).numberOfSourceCandidatePtrs()>0?sourceCandidatePtr(0).key():-1", int,
		     doc="index of first subjet"),
        subJetIdx2 = Var("?numberOfSourceCandidatePtrs()>1 && sourceCandidatePtr(1).numberOfSourceCandidatePtrs()>0?sourceCandidatePtr(1).key():-1", int,
		     doc="index of second subjet"),
	
#        btagDeepC = Var("bDiscriminator('pfDeepCSVJetTags:probc')",float,doc="CMVA V2 btag discriminator",precision=10),
#puIdDisc = Var("userFloat('pileupJetId:fullDiscriminant')",float,doc="Pilup ID discriminant",precision=10),
#        nConstituents = Var("numberOfDaughters()",int,doc="Number of particles in the jet"),
#        rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
    )
)
### Era dependent customization
run2_miniAOD_80XLegacy.toModify( fatJetTable.variables, msoftdrop_chs = Var("userFloat('ak8PFJetsCHSSoftDropMass')",float, doc="Legacy uncorrected soft drop mass with CHS",precision=10))
run2_miniAOD_80XLegacy.toModify( fatJetTable.variables.tau1, expr = cms.string("userFloat(\'ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau1\')"),)
run2_miniAOD_80XLegacy.toModify( fatJetTable.variables.tau2, expr = cms.string("userFloat(\'ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau2\')"),)
run2_miniAOD_80XLegacy.toModify( fatJetTable.variables.tau3, expr = cms.string("userFloat(\'ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau3\')"),)
run2_miniAOD_80XLegacy.toModify( fatJetTable.variables.tau4, expr = cms.string("-1"),)
run2_miniAOD_80XLegacy.toModify( fatJetTable.variables.n2b1, expr = cms.string("-1"),)
run2_miniAOD_80XLegacy.toModify( fatJetTable.variables.n3b1, expr = cms.string("-1"),)
run2_miniAOD_80XLegacy.toModify( fatJetTable.variables, jetId = Var("userInt('tightId')*2+userInt('looseId')",int,doc="Jet ID flags bit1 is loose, bit2 is tight"))

run2_nanoAOD_92X.toModify( fatJetTable.variables.tau4, expr = cms.string("-1"),)
run2_nanoAOD_92X.toModify( fatJetTable.variables.n2b1, expr = cms.string("-1"),)
run2_nanoAOD_92X.toModify( fatJetTable.variables.n3b1, expr = cms.string("-1"),)



subJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("slimmedJetsAK8PFPuppiSoftDropPacked","SubJets"),
    cut = cms.string(""), #probably already applied in miniaod
    name = cms.string("SubJet"),
    doc  = cms.string("slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        btagCMVA = Var("bDiscriminator('pfCombinedMVAV2BJetTags')",float,doc="CMVA V2 btag discriminator",precision=10),
        btagDeepB = Var("bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')",float,doc="DeepCSV b+bb tag discriminator",precision=10),
        btagCSVV2 = Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",float,doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)",precision=10),
        tau1 = Var("userFloat('NjettinessAK8Subjets:tau1')",float, doc="Nsubjettiness (1 axis)",precision=10),
        tau2 = Var("userFloat('NjettinessAK8Subjets:tau2')",float, doc="Nsubjettiness (2 axis)",precision=10),
        tau3 = Var("userFloat('NjettinessAK8Subjets:tau3')",float, doc="Nsubjettiness (3 axis)",precision=10),
        tau4 = Var("userFloat('NjettinessAK8Subjets:tau4')",float, doc="Nsubjettiness (4 axis)",precision=10),
        n2b1 = Var("userFloat('nb1AK8PuppiSoftDropSubjets:ecfN2')", float, doc="N2 with beta=1", precision=10),
        n3b1 = Var("userFloat('nb1AK8PuppiSoftDropSubjets:ecfN3')", float, doc="N3 with beta=1", precision=10),
    )
)

#jets are not as precise as muons
fatJetTable.variables.pt.precision=10
subJetTable.variables.pt.precision=10

run2_miniAOD_80XLegacy.toModify( subJetTable.variables.tau1, expr = cms.string("-1"),)
run2_miniAOD_80XLegacy.toModify( subJetTable.variables.tau2, expr = cms.string("-1"),)
run2_miniAOD_80XLegacy.toModify( subJetTable.variables.tau3, expr = cms.string("-1"),)
run2_miniAOD_80XLegacy.toModify( subJetTable.variables.tau4, expr = cms.string("-1"),)
run2_miniAOD_80XLegacy.toModify( subJetTable.variables.n2b1, expr = cms.string("-1"),)
run2_miniAOD_80XLegacy.toModify( subJetTable.variables.n3b1, expr = cms.string("-1"),)

run2_nanoAOD_92X.toModify( subJetTable.variables.tau4, expr = cms.string("-1"),)
run2_nanoAOD_92X.toModify( subJetTable.variables.n2b1, expr = cms.string("-1"),)
run2_nanoAOD_92X.toModify( subJetTable.variables.n3b1, expr = cms.string("-1"),)





## MC STUFF ######################
jetMCTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("linkedObjects","jets"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name = cms.string("Jet"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(True), # this is an extension  table for the jets
    variables = cms.PSet(
        partonFlavour = Var("partonFlavour()", int, doc="flavour from parton matching"),
        hadronFlavour = Var("hadronFlavour()", int, doc="flavour from hadron ghost clustering"),
        genJetIdx = Var("?genJetFwdRef().backRef().isNonnull()?genJetFwdRef().backRef().key():-1", int, doc="index of matched gen jet"),
    )
)
genJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("slimmedGenJets"),
    cut = cms.string("pt > 10"),
    name = cms.string("GenJet"),
    doc  = cms.string("slimmedGenJets, i.e. ak4 Jets made with visible genparticles"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the genjets
    variables = cms.PSet(P4Vars,
	#anything else?
    )
)
patJetPartons = cms.EDProducer('HadronAndPartonSelector',
    src = cms.InputTag("generator"),
    particles = cms.InputTag("prunedGenParticles"),
    partonMode = cms.string("Auto"),
    fullChainPhysPartons = cms.bool(True)
)
genJetFlavourAssociation = cms.EDProducer("JetFlavourClustering",
    jets = genJetTable.src,
    bHadrons = cms.InputTag("patJetPartons","bHadrons"),
    cHadrons = cms.InputTag("patJetPartons","cHadrons"),
    partons = cms.InputTag("patJetPartons","physicsPartons"),
    leptons = cms.InputTag("patJetPartons","leptons"),
    jetAlgorithm = cms.string("AntiKt"),
    rParam = cms.double(0.4),
    ghostRescaling = cms.double(1e-18),
    hadronFlavourHasPriority = cms.bool(False)
)
genJetFlavourTable = cms.EDProducer("GenJetFlavourTableProducer",
    name = genJetTable.name,
    src = genJetTable.src,
    cut = genJetTable.cut,
    deltaR = cms.double(0.1),
    jetFlavourInfos = cms.InputTag("slimmedGenJetsFlavourInfos"),
)

genJetAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("slimmedGenJetsAK8"),
    cut = cms.string("pt > 100."),
    name = cms.string("GenJetAK8"),
    doc  = cms.string("slimmedGenJetsAK8SoftDropSubJets, i.e. subjets of ak8 Jets made with visible genparticles"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the genjets
    variables = cms.PSet(P4Vars,
	#anything else?
    )
)
genJetAK8FlavourAssociation = cms.EDProducer("JetFlavourClustering",
    jets = genJetAK8Table.src,
    bHadrons = cms.InputTag("patJetPartons","bHadrons"),
    cHadrons = cms.InputTag("patJetPartons","cHadrons"),
    partons = cms.InputTag("patJetPartons","physicsPartons"),
    leptons = cms.InputTag("patJetPartons","leptons"),
    jetAlgorithm = cms.string("AntiKt"),
    rParam = cms.double(0.8),
    ghostRescaling = cms.double(1e-18),
    hadronFlavourHasPriority = cms.bool(False)
)
genJetAK8FlavourTable = cms.EDProducer("GenJetFlavourTableProducer",
    name = genJetAK8Table.name,
    src = genJetAK8Table.src,
    cut = genJetAK8Table.cut,
    deltaR = cms.double(0.1),
    jetFlavourInfos = cms.InputTag("genJetAK8FlavourAssociation"),
)
genSubJetAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("slimmedGenJetsAK8SoftDropSubJets"),
    cut = cms.string(""),  ## These don't get a pt cut, but in miniAOD only subjets from fat jets with pt > 100 are kept
    name = cms.string("SubGenJetAK8"),
    doc  = cms.string("slimmedGenJetsAK8SoftDropSubJets, i.e. subjets of ak8 Jets made with visible genparticles"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the genjets
    variables = cms.PSet(P4Vars,
	#anything else?
    )
)
### Era dependent customization
run2_miniAOD_80XLegacy.toModify( genJetFlavourTable, jetFlavourInfos = cms.InputTag("genJetFlavourAssociation"),)
run2_nanoAOD_92X.toModify( genJetFlavourTable, jetFlavourInfos = cms.InputTag("genJetFlavourAssociation"),)

#before cross linking
jetSequence = cms.Sequence(tightJetId+tightJetIdLepVeto+bJetVars+slimmedJetsWithUserData+jetCorrFactors+updatedJets+tightJetIdAK8+tightJetIdLepVetoAK8+slimmedJetsAK8WithUserData+jetCorrFactorsAK8+updatedJetsAK8+chsForSATkJets+softActivityJets+softActivityJets2+softActivityJets5+softActivityJets10+finalJets+finalJetsAK8)


from RecoJets.JetProducers.QGTagger_cfi import  QGTagger
qgtagger80x=QGTagger.clone(srcJets="slimmedJets",srcVertexCollection="offlineSlimmedPrimaryVertices")

_jetSequence_80X = jetSequence.copy()
_jetSequence_80X.replace(tightJetIdLepVeto, looseJetId)
_jetSequence_80X.replace(tightJetIdLepVetoAK8, looseJetIdAK8)
_jetSequence_80X.insert(1,qgtagger80x)
run2_miniAOD_80XLegacy.toReplaceWith(jetSequence, _jetSequence_80X)

#after cross linkining
jetTables = cms.Sequence(bjetMVA+bjetNN+bjetNN2+jetTable+EnergyRingsTable+fatJetTable+subJetTable+saJetTable+saTable)

#MC only producers and tables
jetMC = cms.Sequence(jetMCTable+genJetTable+patJetPartons+genJetFlavourTable+genJetAK8Table+genJetAK8FlavourAssociation+genJetAK8FlavourTable+genSubJetAK8Table)
_jetMC_pre94X = jetMC.copy()
_jetMC_pre94X.insert(_jetMC_pre94X.index(genJetFlavourTable),genJetFlavourAssociation)
_jetMC_pre94X.remove(genSubJetAK8Table)
run2_miniAOD_80XLegacy.toReplaceWith(jetMC, _jetMC_pre94X)
run2_nanoAOD_92X.toReplaceWith(jetMC, _jetMC_pre94X)


