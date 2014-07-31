#define HIDE_TrackIPTagInfo_TYPEDEF

#include <utility>
#include <vector>

#include "Rtypes.h" 
#include "Math/Cartesian3D.h" 
#include "Math/CylindricalEta3D.h" 
#include "Math/Polar3D.h" 
#include "Math/PxPyPzE4D.h" 
#include "DataFormats/Common/interface/Wrapper.h"
#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/Common/interface/RefProd.h" 
#include "DataFormats/Common/interface/RefToBase.h"
#include "DataFormats/Common/interface/FwdRef.h"
#include "DataFormats/Common/interface/FwdPtr.h"
#include "DataFormats/Common/interface/OwnVector.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"

// Need a dictionary for class which was removed
class TrackIPTagInfo {};
// Make it easy to distinguish old and new class using the same name
namespace reco {namespace old { typedef ::reco::TrackIPTagInfo TrackIPTagInfo; } }

namespace DataFormats_BTauReco {
  struct dictionarytrackiptaginfo {

    reco::old::TrackIPTagInfo                                           otcip;
    reco::old::TrackIPTagInfoCollection                                 otcip_c;
    reco::old::TrackIPTagInfoRef                                        otcip_r;
    reco::old::TrackIPTagInfoFwdRef                                     otcip_fr;
    reco::old::TrackIPTagInfoRefProd                                    otcip_rp;
    reco::old::TrackIPTagInfoRefVector                                  otcip_rv;

    edm::Wrapper<reco::old::TrackIPTagInfoCollection>                   otcip_wc;

    reco::nw::TrackIPTagInfo                                            ntcip;
    reco::nw::TrackIPTagInfoCollection                                  ntcip_c;
    reco::nw::TrackIPTagInfoRef                                         ntcip_r;
    reco::nw::TrackIPTagInfoFwdRef                                      ntcip_fr;
    reco::nw::TrackIPTagInfoRefProd                                     ntcip_rp;
    reco::nw::TrackIPTagInfoRefVector                                   ntcip_rv;

    edm::Wrapper<reco::nw::TrackIPTagInfoCollection>                    ntcip_wc;

    edm::reftobase::Holder<reco::BaseTagInfo, reco::old::TrackIPTagInfoRef>          rb_otcip;
    edm::reftobase::RefHolder<reco::old::TrackIPTagInfoRef>                          rbh_otcip;
    edm::reftobase::Holder<reco::BaseTagInfo, reco::nw::TrackIPTagInfoRef>           rb_ntcip;
    edm::reftobase::RefHolder<reco::nw::TrackIPTagInfoRef>                           rbh_ntcip;

    edm::reftobase::Holder<reco::BaseTagInfo, reco::old::TrackIPTagInfoFwdRef>       rb_otcipf;
    edm::reftobase::RefHolder<reco::old::TrackIPTagInfoFwdRef>                       rbh_otcipf;
    edm::reftobase::Holder<reco::BaseTagInfo, reco::nw::TrackIPTagInfoFwdRef>        rb_ntcipf;
    edm::reftobase::RefHolder<reco::nw::TrackIPTagInfoFwdRef>                        rbh_ntcipf;

  };
}

