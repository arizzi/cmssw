#include "CommonTools/RecoAlgos/interface/PrimaryVertexSorting.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include <fastjet/internal/base.hh>
#include "fastjet/PseudoJet.hh"
#include "fastjet/JetDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/Selector.hh"
#include "fastjet/PseudoJet.hh"

using namespace fastjet;
using namespace std;


float PrimaryVertexSorting::score(const reco::Vertex & pv,const  std::vector<const reco::Candidate *> & cands ) const {
  typedef math::XYZTLorentzVector LorentzVector;
  float sumPt2=0;
  float sumEt=0;
  LorentzVector met;
  std::vector<fastjet::PseudoJet> fjInputs_;  
  fjInputs_.clear();
  for (size_t i = 0 ; i < cands.size(); i++) {
    const reco::Candidate * c= cands[i];
    int absId=abs(c->pdgId());
    if(absId==13 or absId == 11) {
      sumPt2+=c->pt()*c->pt();
      met+=c->p4();
      sumEt+=c->pt();
    } else {
      fjInputs_.push_back(fastjet::PseudoJet(c->px(),c->py(),c->pz(),c->p4().E()));
      fjInputs_.back().set_user_index(i);
    }
  }
  fastjet::ClusterSequence sequence( fjInputs_, JetDefinition(antikt_algorithm, 0.4));
  auto jets = fastjet::sorted_by_pt(sequence.inclusive_jets(0));
  for (const auto & pj : jets) {
    auto p4 = LorentzVector( pj.px(), pj.py(), pj.pz(), pj.e() ) ;
    float wpt=p4.pt();
    if(pj.constituents().size()>1) wpt*=jetWeight_;
    float totalErrorSq=0;
    for(const auto & co : pj.constituents() ){
       const reco::Track * tr = cands[co.user_index()]->bestTrack();
       if(tr!=0) totalErrorSq+=(ptErrorSubtractionFactor_*tr->ptError())*(ptErrorSubtractionFactor_*tr->ptError());
    }
    wpt*=wpt;
    wpt-=totalErrorSq;
    if (wpt> 0) sumPt2+=wpt;
    met+=p4;
    sumEt+=p4.pt();
  }
  float metAbove = met.pt() - metSubtractionFactor_*sqrt(sumEt);
  if(metAbove > 0 and useMet_) {
    sumPt2+=metAbove*metAbove;
  }
  return sumPt2;
}


