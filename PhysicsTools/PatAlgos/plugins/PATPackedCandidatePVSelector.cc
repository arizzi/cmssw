//
// $Id: PATPackedCandidatePVSelector.cc,v 1.1 2015/06/10 arizzi Exp $
//

/**
  \class    pat::PATPackedCandidatePVSelector 
  \brief    Filter PackedCandidates requiring fromPV wrt a different PV
            
  \author   Andrea Rizzi
*/

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Common/interface/RefToPtr.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"
#include "DataFormats/Provenance/interface/ProductID.h"

namespace pat {

  class PATPackedCandidatePVSelector : public edm::EDProducer {
    public:
      explicit PATPackedCandidatePVSelector(const edm::ParameterSet & iConfig);
      virtual ~PATPackedCandidatePVSelector() { }

      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);

    private:
      edm::EDGetTokenT<edm::ValueMap<float>> scores_;
      edm::EDGetTokenT<edm::View<pat::PackedCandidate> >  cands_;
      int threshold_;
  };

} // namespace


pat::PATPackedCandidatePVSelector::PATPackedCandidatePVSelector(const edm::ParameterSet & iConfig) :
    scores_(consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("vertexScores"))),
    cands_(consumes<edm::View<pat::PackedCandidate> >(iConfig.getParameter<edm::InputTag>("src"))),
    threshold_(iConfig.getParameter<int>("threshold"))
{
    produces<edm::PtrVector<reco::Candidate> >();
    produces<std::vector<reco::Vertex> >();
}

void 
pat::PATPackedCandidatePVSelector::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
    using namespace edm;
    using namespace std;

    Handle<View<pat::PackedCandidate> >      cands;
    iEvent.getByToken(cands_, cands);
    Handle<edm::ValueMap<float> > scores;
    iEvent.getByToken(scores_,scores);
	
    auto_ptr<edm::PtrVector<reco::Candidate> >  out(new edm::PtrVector<reco::Candidate>());
    auto_ptr<vector<reco::Vertex> >  outPV(new vector<reco::Vertex>());
    if(cands.product()->size()>0) {
	    //Find PV with highest score
	    int ivtx=0;
	    edm::ProductID pid = (*cands.product())[0].vertexRef().id();
  	    edm::ValueMap<float>::const_iterator itVM = scores->begin();
	    for(; itVM!= scores->end();++itVM) {
		    if(pid==itVM.id()) {
			    float score=-1;
			    edm::ValueMap<float>::container::const_iterator itVtx =  itVM.begin();
			    for(unsigned int i=0; itVtx!=itVM.end(); ++itVtx,i++){
				    if(*itVtx > score) {ivtx=i; score=*itVtx;}
//				    std::cout << " i,imax score,scoremax" << i << " " << ivtx << " " << *itVtx << " "<< score << std::endl;
			    }
		    }
//	    std::cout << "Selected " << ivtx << std::endl;
    	    outPV->push_back((*(*cands.product())[0].vertexRef().product())[ivtx]);
	    }
	    //Take only cands with fromPV >= thr relative to the found vertex
	    for (edm::View<pat::PackedCandidate>::const_iterator it = cands->begin(), ed = cands->end(); it != ed; ++it) {
		    if(it->fromPV(ivtx) >= threshold_ || it->charge() == 0 ){
			    out->push_back(cands->ptrAt(it-cands->begin()));
		    }
	    }
    }
    iEvent.put(out);
    iEvent.put(outPV);
}

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(PATPackedCandidatePVSelector);
