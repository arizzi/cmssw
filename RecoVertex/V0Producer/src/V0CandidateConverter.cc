#include <string>
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/Candidate/interface/VertexCompositeCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Common/interface/RefToPtr.h"

class V0CandidateConverter : public edm::EDProducer {
        public:
            explicit V0CandidateConverter(const edm::ParameterSet&);
            ~V0CandidateConverter();

            virtual void produce(edm::Event&, const edm::EventSetup&);
        private:
            edm::EDGetTokenT<std::vector<reco::VertexCompositeCandidate> > src_;
            edm::EDGetTokenT<edm::View<reco::Candidate> > cands_;
    };

V0CandidateConverter::V0CandidateConverter(const edm::ParameterSet& iConfig) :
    src_(consumes<std::vector<reco::VertexCompositeCandidate> >(iConfig.getParameter<edm::InputTag>("src"))),
    cands_(consumes<edm::View<reco::Candidate> >(iConfig.getParameter<edm::InputTag>("cands")))
{
  produces< reco::VertexCompositePtrCandidateCollection >();
}

V0CandidateConverter::~V0CandidateConverter() {}

void V0CandidateConverter::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<std::vector<reco::VertexCompositeCandidate> > vertices;
    iEvent.getByToken(src_, vertices);
    std::auto_ptr<reco::VertexCompositePtrCandidateCollection > outPtr(new reco::VertexCompositePtrCandidateCollection);
 
    edm::Handle<edm::View<reco::Candidate> > cands;
    iEvent.getByToken(cands_,cands);


    outPtr->reserve(vertices->size());
    for (unsigned int i = 0, n = vertices->size(); i < n; ++i) { 
	    const reco::VertexCompositeCandidate &v = (*vertices)[i];
	    reco::VertexCompositeCandidate::CovarianceMatrix error;
	    v.fillVertexCovariance(error);
	    reco::CompositePtrCandidate::daughters d;	
	    for(unsigned j = 0; j < v.numberOfDaughters(); j++)  {
	    	    const reco::Track * track = v.daughter(j)->bestTrack();
		    for(unsigned k = 0; k < cands->size() ; k++)
		    {
			if(track==(*cands)[k].bestTrack()) {
				 d.push_back(cands->ptrAt(k));
				 break;
			}
		    }	
	    }
	    outPtr->push_back(reco::VertexCompositePtrCandidate(0,v.p4(),v.vertex(), error, v.vertexChi2(), v.vertexNdof(),d,v.pdgId()));
    }

    iEvent.put(outPtr);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(V0CandidateConverter);
