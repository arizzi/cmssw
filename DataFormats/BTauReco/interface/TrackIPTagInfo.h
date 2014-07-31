#ifndef BTauReco_TrackIpTagInfo_h
#define BTauReco_TrackIpTagInfo_h

#include "DataFormats/BTauReco/interface/RefMacros.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/BTauReco/interface/JTATagInfo.h"
#include "DataFormats/BTauReco/interface/IPTagInfo.h"

namespace reco {

#ifdef HIDE_TrackIPTagInfo_TYPEDEF
namespace nw {
#endif
typedef reco::IPTagInfo<reco::TrackRefVector,reco::JTATagInfo> TrackIPTagInfo;

DECLARE_EDM_REFS( TrackIPTagInfo )

#ifdef HIDE_TrackIPTagInfo_TYPEDEF
}
#endif

}

#endif
