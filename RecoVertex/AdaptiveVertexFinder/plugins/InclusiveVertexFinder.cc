#include "RecoVertex/AdaptiveVertexFinder/plugins/InclusiveVertexFinder.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Common/interface/View.h"


typedef TemplatedInclusiveVertexFinder<reco::TrackCollection,reco::Vertex> InclusiveVertexFinder;
typedef TemplatedInclusiveVertexFinder<edm::View<reco::Candidate>,reco::VertexCompositePtrCandidate > InclusiveCandidateVertexFinder;
typedef TemplatedInclusiveVertexFinder<std::vector<reco::CandidatePtr> ,reco::VertexCompositePtrCandidate > InclusiveCandidatePtrVertexFinder;


DEFINE_FWK_MODULE(InclusiveCandidateVertexFinder);
DEFINE_FWK_MODULE(InclusiveCandidatePtrVertexFinder);
DEFINE_FWK_MODULE(InclusiveVertexFinder);
