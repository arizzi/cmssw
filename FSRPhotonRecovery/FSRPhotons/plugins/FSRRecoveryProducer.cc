// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "RecoParticleFlow/PFClusterTools/interface/PFEnergyResolution.h"

#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/PFParticle.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "TLorentzVector.h"

#include "TMVA/DataLoader.h"
#include "TMVA/Factory.h"
#include "TMVA/Reader.h"
#include "TMVA/Tools.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Common/interface/RefToPtr.h"

//----------------------------------------------------------------------//
// FSRPhotonRecovery, 15.3.2019, oliver.rieger@cern.ch                  //
//----------------------------------------------------------------------//

class FSRRecoveryProducer : public edm::EDProducer {
public:
  explicit FSRRecoveryProducer(const edm::ParameterSet &);
  ~FSRRecoveryProducer();

private:
  virtual void produce(edm::Event &, const edm::EventSetup &);

  double photonPfIso03(pat::PFParticle pho, edm::Handle<pat::PackedCandidateCollection> pfcands);
  std::vector<pat::PFParticle>  MakeHybridPhotons(const edm::Handle<pat::PhotonCollection> &patphotons, const edm::Handle<pat::PFParticleCollection> &pfphotons, bool modifyP4);
  void SetPhoMVAVars(const pat::PFParticle pho, pat::Muon mu, const edm::Handle<pat::PackedCandidateCollection> &pfcands);
  float getMVAValue();
  void initializeReader();

  // Load Collections
  edm::EDGetTokenT<pat::PackedCandidateCollection> pfcands_;
  edm::EDGetTokenT<edm::View<pat::Muon>> muons_;
  edm::EDGetTokenT<pat::ElectronCollection> electrons_;
  edm::EDGetTokenT<pat::PFParticleCollection> pfphotons_;
  edm::EDGetTokenT<pat::PhotonCollection> patphotons_;
  std::string weightsfile_;

  TMVA::Reader *tmvaReader;

  // MVA Variables:
  float_t dREtg;
  float_t Mgmu;
  float_t PhoIso;
  float_t MuPtSplit;
};

double FSRRecoveryProducer::photonPfIso03(pat::PFParticle pho, edm::Handle<pat::PackedCandidateCollection> pfcands) {
  double ptsum = 0.0;
  for (const pat::PackedCandidate &pfc : *pfcands) {
    double dr = deltaR(pho.p4(), pfc.p4());
    if (dr >= 0.3)
      continue;

    if (pfc.charge() != 0 && abs(pfc.pdgId()) == 211 && pfc.pt() > 0.2) {
      if (dr > 0.0001)
        ptsum += pfc.pt();
    } else if (pfc.charge() == 0 &&
               (abs(pfc.pdgId()) == 22 || abs(pfc.pdgId()) == 130) && pfc.pt() > 0.5) {
      if (dr > 0.01)
        ptsum += pfc.pt();
    }
  }
  return ptsum;
}

std::vector<pat::PFParticle> FSRRecoveryProducer::MakeHybridPhotons(
    const edm::Handle<pat::PhotonCollection> &patphotons,
    const edm::Handle<pat::PFParticleCollection> &pfphotons, bool modifyP4 = false) {
  
  std::vector<pat::PFParticle> result;
   
  for (unsigned int i = 0; i < pfphotons->size(); i++) {
    pat::PFParticle hybridpho = pfphotons->at(i);
    hybridpho.addUserFloat("photonMVAIdValue", -10);
    hybridpho.addUserFloat("photonPuppiIso", -10);
    hybridpho.addUserFloat("EleVeto", -10);
    hybridpho.addUserFloat("hasPixelSeed", -10);
    hybridpho.addUserFloat("correctedPt", -10);
    hybridpho.addUserFloat("correctedEta", -10);
    hybridpho.addUserFloat("correctedPhi", -10);
    
    for (unsigned int k = 0; k < patphotons->size(); k++) {
      pat::Photon patpho =  patphotons->at(k);
      
      // MATCHING PATPHOTON AND ASSOCIATION //
      double matching_dR = 0.05;
      int matching_index = -1;
      for(unsigned int m = 0; m < patpho.associatedPackedPFCandidates().size(); m++)
	{
	  if( patpho.associatedPackedPFCandidates().at(m)->pdgId()!=22 ) continue;
	  double phocandpt  =  patpho.associatedPackedPFCandidates().at(m)->pt();
	  double dR = deltaR(patpho.associatedPackedPFCandidates().at(m)->p4(), patpho.p4());
	    
	  if ( (abs(phocandpt - patpho.pt())/phocandpt) < 0.2 && dR < matching_dR)
	    { 
	      matching_dR = dR;
	      matching_index = m;
	    }
	}
   	
      // MATCHING ASSOCIATION AND PFPHOTON
      if(matching_index >= 0){
	pat::PackedCandidate associatedPhotonMatch = *(patpho.associatedPackedPFCandidates().at(matching_index));
	double dR = deltaR(hybridpho.p4(), associatedPhotonMatch.p4());
	if(abs(hybridpho.pt() - associatedPhotonMatch.pt()) < 1e-3 && dR < 0.05){
	  math::XYZTLorentzVector pho_corrP4 = patpho.p4() * patpho.userFloat("ecalEnergyPostCorr") / patpho.energy();
	  if(modifyP4){
	    hybridpho.setP4(pho_corrP4);
	  }
	  hybridpho.addUserFloat("photonMVAIdValue", patpho.userFloat("PhotonMVAEstimatorRunIIFall17v1p1Values"), true);
	  hybridpho.addUserFloat("photonPuppiIso", patpho.puppiPhotonIso(), true);
	  hybridpho.addUserFloat("EleVeto", patpho.passElectronVeto(), true);
	  hybridpho.addUserFloat("hasPixelSeed", patpho.hasPixelSeed(), true);
	  hybridpho.addUserFloat("correctedPt", pho_corrP4.Pt(), true);
	  hybridpho.addUserFloat("correctedEta", pho_corrP4.Eta(), true);
	  hybridpho.addUserFloat("correctedPhi", pho_corrP4.Phi(), true);
	}
      }
    }
    result.push_back(hybridpho);
  }
  
  return result;
}

void FSRRecoveryProducer::SetPhoMVAVars(
    const pat::PFParticle pho, pat::Muon mu,
    const edm::Handle<pat::PackedCandidateCollection> &pfcands) {

  TLorentzVector thisLep;
  thisLep.SetPtEtaPhiM(mu.pt(), mu.eta(), mu.phi(), mu.mass());
  double  zed = pho.energy()/mu.energy();

  dREtg = deltaR(mu.p4(), pho.p4())/pow(pho.pt(),2);
  PhoIso = photonPfIso03(pho, pfcands) / pho.pt();
  Mgmu = (pho.p4() + mu.p4()).M();
  MuPtSplit = (1/zed)*(1+pow((1-zed),2));
}

void FSRRecoveryProducer::initializeReader() {
  tmvaReader->AddVariable("dREtg", &dREtg);
  tmvaReader->AddVariable("PhoIso", &PhoIso);
  tmvaReader->AddVariable("Mgmu", &Mgmu);
  tmvaReader->AddVariable("MuPtSplit", &MuPtSplit);
  float_t spectator = 1; //arbitrarry
  tmvaReader->AddSpectator("nFSRPhoton", &spectator);
  tmvaReader->AddSpectator("evWeight", &spectator);
  //tmvaReader->BookMVA("BDTG", weightsfile_);
  tmvaReader->BookMVA("BDTG", edm::FileInPath(weightsfile_).fullPath());
}

float FSRRecoveryProducer::getMVAValue() {

  return tmvaReader->EvaluateMVA("BDTG");
}

FSRRecoveryProducer::FSRRecoveryProducer(const edm::ParameterSet &iConfig)
    : pfcands_(consumes<pat::PackedCandidateCollection>(
          iConfig.getParameter<edm::InputTag>("pfcands"))),
      muons_(consumes<edm::View<pat::Muon>>(
          iConfig.getParameter<edm::InputTag>("muons"))),
      electrons_(consumes<pat::ElectronCollection>(
          iConfig.getParameter<edm::InputTag>("electrons"))),
      pfphotons_(consumes<pat::PFParticleCollection>(
          iConfig.getParameter<edm::InputTag>("pfphotons"))),
      patphotons_(consumes<pat::PhotonCollection>(
          iConfig.getParameter<edm::InputTag>("patphotons"))),
      weightsfile_(iConfig.getParameter<std::string>("weights")) {
  tmvaReader = new TMVA::Reader("!Color:!Silent:Error");
  initializeReader();
  produces<pat::PFParticleCollection>("selectedFSRphotons").setBranchAlias("selectedFSRphotons");
}

FSRRecoveryProducer::~FSRRecoveryProducer() {}

void FSRRecoveryProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {

  edm::Handle<pat::PackedCandidateCollection> pfcands;
  iEvent.getByToken(pfcands_, pfcands);

  edm::Handle<edm::View<pat::Muon>> muons;
  iEvent.getByToken(muons_, muons);

  edm::Handle<pat::ElectronCollection> electrons;
  iEvent.getByToken(electrons_, electrons);

  edm::Handle<pat::PhotonCollection> patphotons;
  iEvent.getByToken(patphotons_, patphotons);

  edm::Handle<pat::PFParticleCollection> pfphotons;
  iEvent.getByToken(pfphotons_, pfphotons);

  pat::PFParticleCollection hybridphotons = MakeHybridPhotons(patphotons, pfphotons);

  std::unique_ptr<pat::PFParticleCollection> hybridphotonsCopy(
      new pat::PFParticleCollection(hybridphotons));

  std::unique_ptr<pat::PFParticleCollection> output(
      new pat::PFParticleCollection());

  for (edm::View<pat::Muon>::const_iterator mu = muons->begin(); mu != muons->end(); ++mu) {

    TLorentzVector thisLep;
    thisLep.SetPtEtaPhiM(mu->pt(), mu->eta(), mu->phi(), mu->mass());

    for (std::vector<pat::PFParticle>::iterator phot = hybridphotonsCopy->begin(); phot != hybridphotonsCopy->end(); ++phot) {

      if (fabs(phot->eta()) > 2.4 || (fabs(phot->eta()) > 1.4 && fabs(phot->eta()) < 1.6) || phot->pt() < 2.0) continue;

      // CLOSESEST TO MUON IN CONE //
      double dRPhoMu = deltaR(thisLep.Eta(), thisLep.Phi(), phot->eta(), phot->phi());

      if (dRPhoMu > 0.5) continue;

      bool matched = false;
      bool closest = true;

      for (edm::View<pat::Muon>::const_iterator extmu = muons->begin(); extmu != muons->end(); ++extmu) {
        
	TLorentzVector otherLep;
        otherLep.SetPtEtaPhiM(extmu->pt(), extmu->eta(), extmu->phi(), extmu->mass());

        double dRPhoMuOther = deltaR(otherLep.Eta(), otherLep.Phi(), phot->eta(), phot->phi());
        if (dRPhoMuOther < dRPhoMu) closest = false;

        for (std::vector<pat::Electron>::const_iterator ele = electrons->begin(); ele != electrons->end(); ++ele) {

          for (size_t nele = 0;
               nele < ele->associatedPackedPFCandidates().size(); nele++) {
            double ecandpt = ele->associatedPackedPFCandidates().at(nele)->pt();
            double ecandeta =
                ele->associatedPackedPFCandidates().at(nele)->eta();
            double ecandphi =
                ele->associatedPackedPFCandidates().at(nele)->phi();
            if (abs(ecandpt - phot->pt()) < 1e-10 &&
                abs(ecandeta - phot->eta()) < 1e-10 &&
                abs(ecandphi - phot->phi()) < 1e-10)
              matched = true;
          }
        }
      }

      if (matched)
        continue;

      if (!closest)
        continue;

      const reco::CandidatePtr associatedMuon(muons, mu - muons->begin());

      double PFphotonIso03 = FSRRecoveryProducer::photonPfIso03(*phot, pfcands) / phot->pt();
      double dREtg = dRPhoMu / pow(phot->pt(), 2);
      
      FSRRecoveryProducer::SetPhoMVAVars(*phot, muons->at(mu - muons->begin()), pfcands);
      phot->addUserFloat("FSRphotonMVAValue", getMVAValue());
      phot->addUserFloat("PFphotonIso03", PFphotonIso03);
      phot->addUserFloat("ETgammadeltaR", dREtg);
      phot->addUserCand("associatedMuon", associatedMuon);

      output->push_back(*phot);
    }
  }

  iEvent.put(std::move(output), "selectedFSRphotons");
}

// define this as a plug-in
DEFINE_FWK_MODULE(FSRRecoveryProducer);
