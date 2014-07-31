#define HIDE_SVTagInfo_TYPEDEF
#include <utility>
#include <vector>
#include "DataFormats/Common/interface/Wrapper.h"
#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/Common/interface/RefProd.h" 
#include "DataFormats/Common/interface/RefToBase.h"
#include "DataFormats/Common/interface/FwdRef.h"
#include "DataFormats/Common/interface/FwdPtr.h"

/*#include "Rtypes.h" 
#include "Math/Cartesian3D.h" 
#include "Math/CylindricalEta3D.h" 
#include "Math/Polar3D.h" 
#include "Math/PxPyPzE4D.h" 
#include "DataFormats/Common/interface/OwnVector.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h" 
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"  
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/EgammaReco/interface/BasicCluster.h"
#include "DataFormats/EgammaReco/interface/BasicClusterFwd.h" 
#include "DataFormats/BTauReco/interface/JetCrystalsAssociation.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/BTauReco/interface/TaggingVariable.h"
#include "DataFormats/BTauReco/interface/TrackCountingTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackProbabilityTagInfo.h"
#include "DataFormats/BTauReco/interface/IsolatedTauTagInfo.h"
#include "DataFormats/BTauReco/interface/EMIsolatedTauTagInfo.h"
#include "DataFormats/BTauReco/interface/CombinedTauTagInfo.h"*/
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
/*#include "DataFormats/BTauReco/interface/CandSecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/SoftLeptonTagInfo.h"
#include "DataFormats/BTauReco/interface/TauImpactParameterInfo.h"
#include "DataFormats/BTauReco/interface/TauMassTagInfo.h"
#include "DataFormats/BTauReco/interface/JetEisolAssociation.h"
#include "DataFormats/BTauReco/interface/CandIPTagInfo.h"
#include "DataFormats/BTauReco/interface/BaseTagInfo.h"
#include "DataFormats/BTauReco/interface/JTATagInfo.h"
#include "DataFormats/BTauReco/interface/JetTagInfo.h"
*/
namespace reco {

}

namespace DataFormats_BTauReco {
  struct dictionary {

    reco::btag::TrackData                                               sv_td;
    reco::nw::SecondaryVertexTagInfo::VertexData                            rbsv;
    std::vector<reco::nw::SecondaryVertexTagInfo::VertexData>               sv_vdv;
    reco::btag::IndexedTrackData                                        sv_itd;
    std::vector<reco::btag::IndexedTrackData>                           sv_itdv;

    reco::nw::SecondaryVertexTagInfo                                        sv;
    reco::nw::SecondaryVertexTagInfoCollection                              sv_c;
    reco::nw::SecondaryVertexTagInfoRef                                     sv_r;
    reco::nw::SecondaryVertexTagInfoFwdRef                                  sv_fr;
    reco::nw::SecondaryVertexTagInfoRefProd                                 sv_rp;
    reco::nw::SecondaryVertexTagInfoRefVector                               sv_rv;
    edm::Wrapper<reco::nw::SecondaryVertexTagInfoCollection>                sv_wc;

    edm::reftobase::Holder<reco::BaseTagInfo, reco::nw::SecondaryVertexTagInfoRef>  rb_sv;
    edm::reftobase::RefHolder<reco::nw::SecondaryVertexTagInfoRef>                  rbh_sv;
    edm::reftobase::Holder<reco::BaseTagInfo, reco::nw::SecondaryVertexTagInfoFwdRef>  rb_svf;
    edm::reftobase::RefHolder<reco::nw::SecondaryVertexTagInfoFwdRef>                  rbh_svf;
    // Dictionaries for SVTagInfoProxy
    edm::helpers::KeyVal<edm::RefProd<std::vector<reco::nw::SecondaryVertexTagInfo> >, edm::RefProd<std::vector<reco::Vertex> > >  dummy03;
    edm::AssociationMap<edm::OneToMany<reco::nw::SecondaryVertexTagInfoCollection, reco::VertexCollection> > dummy05;
    edm::Wrapper<edm::helpers::KeyVal<edm::RefProd<std::vector<reco::nw::SecondaryVertexTagInfo> >, edm::RefProd<std::vector<reco::Vertex> > > > dummy04;
    edm::Wrapper<edm::AssociationMap<edm::OneToMany<std::vector<reco::nw::SecondaryVertexTagInfo>, std::vector<reco::Vertex>, unsigned int > > > dummy06;

  };
}

