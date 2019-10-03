// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/global/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Common/interface/ValueMap.h"

//
// class declaration
//

class MuonFSRProducer : public edm::global::EDProducer<> {

public:
  
  explicit MuonFSRProducer(const edm::ParameterSet &iConfig):

    pfcands_ {consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("packedPFCandidates"))},
    electrons_ {consumes<pat::ElectronCollection>(iConfig.getParameter<edm::InputTag>("slimmedElectrons"))},
    muons_   {consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("slimmedMuons"))}{
      
      produces<edm::ValueMap<float>>("ptFSR");
      produces<edm::ValueMap<float>>("etaFSR");
      produces<edm::ValueMap<float>>("phiFSR");
      produces<edm::ValueMap<float>>("isoCHSFSR");
      produces<edm::ValueMap<float>>("isoFSR");
    }
  
  ~MuonFSRProducer() override {}
  
  //static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  
private:
  
  void produce(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;

  double photonPfIso03(const pat::PackedCandidate & pho,
                                  const pat::PackedCandidateCollection& pfcands) const;
  double computeRelativeIsolation(const pat::PackedCandidate & photon,
				  const pat::PackedCandidateCollection& pfcands,
				  const double & isoConeMax,
				  const double & isoConeMin, int fromPVCut) const;

  const edm::EDGetTokenT<pat::PackedCandidateCollection> pfcands_;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_;
  const edm::EDGetTokenT<pat::MuonCollection> muons_;


// ----------member data ---------------------------

  edm::EDGetTokenT<edm::ValueMap<float>> ptFSR_;
  edm::EDGetTokenT<edm::ValueMap<float>> etaFSR_;
  edm::EDGetTokenT<edm::ValueMap<float>> phiFSR_;
  edm::EDGetTokenT<edm::ValueMap<float>> isoCHS_;
  edm::EDGetTokenT<edm::ValueMap<float>> iso_;

  //typedef std::vector<pat::PackedCandidateCollection> PackedCandidateCollection;

  //  edm::EDGetTokenT<PackedCandidateCollection> pfcands_;
  //edm::EDGetTokenT<MuonCollection> muons_;

};

// //
// // constants, enums and typedefs
// //


// //
// // static data member definitions
// //
void MuonFSRProducer::produce(edm::StreamID streamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {

  using namespace std;

  //edm::Handle<PackedCandidateCollection> pfcands;
  edm::Handle<pat::PackedCandidateCollection> pfcands;
  iEvent.getByToken(pfcands_, pfcands);
  edm::Handle<pat::MuonCollection> muons;
  iEvent.getByToken(muons_, muons);
  edm::Handle<pat::ElectronCollection> electrons;
  iEvent.getByToken(electrons_, electrons);

  float photon_pt = 0.;
  float photon_eta = 0.;
  float photon_phi = 0.;
  float photon_iso = 0.;
  float photon_isoCHS =0.;
  std::vector<float> ptFSR;
  std::vector<float> etaFSR;
  std::vector<float> phiFSR;
  std::vector<float> isoCHS;
  std::vector<float> iso;

  // loop over all muons
  for (auto muon = muons->begin(); muon != muons->end(); ++muon){

    photon_pt = 0.;
    photon_eta = 0.;
    photon_phi = 0.;
   
    int photonPosition = -1;
    double distance_metric_min = -1;

    // for each muon, loop over all pf cadidates
    for(auto iter_pf = pfcands->begin(); iter_pf != pfcands->end(); iter_pf++){
      pat::PackedCandidate pc = *iter_pf;

      // minimum muon pT
      if (muon->pt() < 5) continue;
      
      // maximum muon eta
      if (fabs(muon->eta() > 2.4)) continue;
      
      // consider only photons
      if (abs(pc.pdgId()) != 22) continue;

      // 0.0001 < DeltaR(photon,muon) < 0.5 requirement
      if(deltaR(muon->eta(),muon->phi(),pc.eta(),pc.phi()) < 0.0001) continue;
      if(deltaR(muon->eta(),muon->phi(),pc.eta(),pc.phi()) > 0.5) continue;
	 
      // eta requirements
      if (fabs(pc.eta()) > 1.4442 and (fabs(pc.eta()) < 1.566)) continue;
      if (fabs(pc.eta()) > 2.4) continue;

      // minimum pT cut
      if (pc.pt() < 2.) continue;

      // Check that is not in footprint of an electron
      bool skipPhoton = false;
      pat::PackedCandidateRef pfcandRef = pat::PackedCandidateRef(pfcands,iter_pf - pfcands->begin());
      //      for (std::vector<pat::Electron>::const_iterator electrons_iter = electrons->begin(); electrons_iter != electrons->end(); ++electrons_iter) {
      for (auto electrons_iter = electrons->begin(); electrons_iter != electrons->end(); ++electrons_iter){
	for(auto itr = electrons_iter->associatedPackedPFCandidates().begin(); itr != electrons_iter->associatedPackedPFCandidates().end(); ++itr){
	  if(itr->key() == pfcandRef.key()){
	    skipPhoton = true;
	  }
	}
      }
      if(skipPhoton) continue;
      //cout<<"Bremsstrhalung pass! "<< pc.pt() << endl;

      // Isolation request
      double relisoCHS = computeRelativeIsolation(pc,*pfcands,0.3,0.0001,1);
      double reliso = photonPfIso03(pc,*pfcands)/pc.pt();
      //if(reliso > 0.8 and relisoCHS > 0.8) continue;
      if( relisoCHS > 0.8) continue;
      //cout<<"Rel Iso pass!"<<endl;

      // ISR photon defined as the one with minimum value of DeltaR
      double metric = deltaR(muon->eta(),muon->phi(),pc.eta(),pc.phi())/(pc.pt()*pc.pt());
      //cout << metric << " " << pc.pt() << endl;
      if(photonPosition == -1){
	distance_metric_min = metric;
	photonPosition = iter_pf - pfcands->begin();
      }
      else if(photonPosition != -1 and metric < distance_metric_min){
	distance_metric_min = metric;
	photonPosition = iter_pf-pfcands->begin();
      } 
      else {continue ; } //this is not the best photon
      if(photonPosition == -1) continue;

      //cout<<"Final distance = "<<distance_metric_min<< " " << photonPosition << endl;

      if (distance_metric_min > 0.019) continue;

      //cout<<"Minimum DeltaR!"<<endl;

      // Now, save the FSR photon pT, eta, and phi
      //      cont = cont + 1;
      photon_pt  = pc.pt();
      photon_eta = pc.eta();
      photon_phi = pc.phi();
      photon_iso = reliso;
      photon_isoCHS = relisoCHS;

    }
    ptFSR.push_back(photon_pt);
    etaFSR.push_back(photon_eta);
    phiFSR.push_back(photon_phi);
    iso.push_back(photon_iso);
    isoCHS.push_back(photon_isoCHS);
 
    //std::cout<<"Photon pT: "<<photon_pt<<std::endl;
  }
  
  std::unique_ptr<edm::ValueMap<float>> ptFSRV(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler fillerptFSR(*ptFSRV);
  fillerptFSR.insert(muons, ptFSR.begin(), ptFSR.end());
  fillerptFSR.fill();
  iEvent.put(std::move(ptFSRV),"ptFSR");

  std::unique_ptr<edm::ValueMap<float>> etaFSRV(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filleretaFSR(*etaFSRV);
  filleretaFSR.insert(muons, etaFSR.begin(), etaFSR.end());
  filleretaFSR.fill();
  iEvent.put(std::move(etaFSRV),"etaFSR");

  std::unique_ptr<edm::ValueMap<float>> phiFSRV(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler fillerphiFSR(*phiFSRV);
  fillerphiFSR.insert(muons, phiFSR.begin(), phiFSR.end());
  fillerphiFSR.fill();
  iEvent.put(std::move(phiFSRV),"phiFSR");

  std::unique_ptr<edm::ValueMap<float>> isoFSRV(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler fillerisoFSR(*isoFSRV);
  fillerisoFSR.insert(muons, iso.begin(), iso.end());
  fillerisoFSR.fill();
  iEvent.put(std::move(isoFSRV),"isoFSR");

  std::unique_ptr<edm::ValueMap<float>> isoCHSFSRV(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler fillerisoCHSFSR(*isoCHSFSRV);
  fillerisoCHSFSR.insert(muons, isoCHS.begin(), isoCHS.end());
  fillerisoCHSFSR.fill();
  iEvent.put(std::move(isoCHSFSRV),"isoCHSFSR");
}

double MuonFSRProducer::photonPfIso03(const pat::PackedCandidate & pho,
                                  const pat::PackedCandidateCollection& pfcands) const {
  double ptsum = 0.0;
  for (const auto  &pfc : pfcands) {
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


double MuonFSRProducer::computeRelativeIsolation(const pat::PackedCandidate & photon,
						 const pat::PackedCandidateCollection& pfcands,
						 const double & isoConeMax,
						 const double & isoConeMin, int fromPVcut) const{

  double isoval_charged = 0;
  double isoval_neutral = 0;
  double isoval_gamma = 0;

  for(auto pfcand : pfcands){
    // Isolation cone requirement
    if(deltaR(photon.eta(),photon.phi(),pfcand.eta(),pfcand.phi()) > isoConeMax) continue;
    // footprint removal
    if(deltaR(photon.eta(),photon.phi(),pfcand.eta(),pfcand.phi()) < isoConeMin) continue;
    // Electrons and muons are not included cause we are looking for FSR photons not included in electrons footprints
    if(pfcand.vertexRef().isNonnull()){
      if(abs(pfcand.pdgId()) == 211){ // charged hadrons
	if (pfcand.fromPV(0) <= fromPVcut) continue;
	isoval_charged += pfcand.pt();
      }
      else if(abs(pfcand.pdgId()) == 22){ // photons
	isoval_gamma += pfcand.pt();
      }
      else if(abs(pfcand.pdgId()) != 11 and abs(pfcand.pdgId()) != 13 and abs(pfcand.pdgId()) != 15 and abs(pfcand.pdgId()) != 24){ 
	isoval_neutral += pfcand.pt();
      }
    }
  }
  
  return (isoval_charged+isoval_gamma+isoval_neutral)/photon.pt();
}


//define this as a plug-in
DEFINE_FWK_MODULE(MuonFSRProducer);
