#include "CommonTools/ParticleFlow/interface/PFPrimaryVertexSorting.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
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


float PFPrimaryVertexSorting::score(const reco::Vertex & pv, std::vector<std::pair<const reco::PFCandidate &,PFPrimaryVertexAssignment::Quality> > pfCands ) const {
  typedef math::XYZTLorentzVector LorentzVector;
 float sumPt2=0;
 float sumEt=0;
 LorentzVector met;
/* for(auto const & pf  : pfCands) {
      sumPt2+=pf.first.pt()*pf.first.pt();
  }
*/

  std::vector<fastjet::PseudoJet> fjInputs_;  
  fjInputs_.clear();
  for (auto const &o : pfCands) {
      int absId=abs(o.first.pdgId());
      if(absId==13 or absId == 11) {
           sumPt2+=o.first.pt()*o.first.pt();
           met+=o.first.p4();
           sumEt+=o.first.pt();
      } else {
         fjInputs_.push_back(fastjet::PseudoJet(o.first.px(),o.first.py(),o.first.pz(),o.first.p4().E()));
      }
  }
  fastjet::ClusterSequence sequence( fjInputs_, JetDefinition(antikt_algorithm, 0.4));
  auto jets = fastjet::sorted_by_pt(sequence.inclusive_jets(0));
  for (const auto & pj : jets) {
    auto p4 = LorentzVector( pj.px(), pj.py(), pj.pz(), pj.e() ) ;
     sumPt2+=p4.pt()*p4.pt()*0.8*0.8;
     met+=p4;
     sumEt+=p4.pt();
  }

 return sumPt2;
}


