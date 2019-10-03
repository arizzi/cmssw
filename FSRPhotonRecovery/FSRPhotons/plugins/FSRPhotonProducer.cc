// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include <DataFormats/MuonReco/interface/Muon.h>
#include "DataFormats/PatCandidates/interface/Muon.h"
#include <DataFormats/GsfTrackReco/interface/GsfTrack.h>

//-------------------------------------------------------------------------------------------------------------------//
//   Taken from: https://github.com/VBF-HZZ/UFHZZAnalysisRun2/blob/94X/FSRPhotons/plugins/FSRPhotonProducer.cc       //
//   Edited: Oliver Rieger, 4.3.2019, oliver.rieger@cern.ch                                                          //
//-------------------------------------------------------------------------------------------------------------------//

class FSRPhotonProducer : public edm::EDProducer 
{
public:
  explicit FSRPhotonProducer(const edm::ParameterSet&);
  ~FSRPhotonProducer();
  
private:
  virtual void produce(edm::Event&, const edm::EventSetup&);
  
  edm::EDGetTokenT<reco::CandidateView> srcCands_;
  double ptThresh_;
  bool   extractMuonFSR_;
};

FSRPhotonProducer::FSRPhotonProducer(const edm::ParameterSet& iConfig):
  srcCands_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("srcCands"))),
  ptThresh_( iConfig.getParameter<double>("ptThresh") )
{
  produces<reco::PFCandidateCollection>(); 
}

FSRPhotonProducer::~FSRPhotonProducer(){}

void FSRPhotonProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::unique_ptr<reco::PFCandidateCollection> comp( new reco::PFCandidateCollection );
  
  edm::Handle<reco::CandidateView> cands;
  iEvent.getByToken(srcCands_, cands);
  
  for( reco::CandidateView::const_iterator c = cands->begin(); c != cands->end(); ++c ) 
  {
    if (c->charge()==0 && c->pdgId() == 22 && c->pt() > ptThresh_)  
      {
      comp->push_back( reco::PFCandidate(0, c->p4(), reco::PFCandidate::gamma));
      comp->back().setStatus(0);
    }
  }
  
  iEvent.put( std::move(comp) );
}

DEFINE_FWK_MODULE(FSRPhotonProducer);
