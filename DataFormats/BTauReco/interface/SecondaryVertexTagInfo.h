#ifndef DataFormats_BTauReco_SecondaryVertexTagInfo_h
#define DataFormats_BTauReco_SecondaryVertexTagInfo_h

#include "DataFormats/BTauReco/interface/RefMacros.h"
#include "DataFormats/BTauReco/interface/TemplatedSecondaryVertexTagInfo.h"

namespace reco {
#ifdef HIDE_SVTagInfo_TYPEDEF
namespace nw {
#endif

typedef reco::TemplatedSecondaryVertexTagInfo<reco::TrackIPTagInfo,reco::Vertex> SecondaryVertexTagInfo;


DECLARE_EDM_REFS(SecondaryVertexTagInfo)
#ifdef HIDE_SVTagInfo_TYPEDEF
}
#endif

}
#endif // DataFormats_BTauReco_SecondaryVertexTagInfo_h
