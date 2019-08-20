#ifndef DataFormats_HGCalReco_TICLCandidate_h
#define DataFormats_HGCalReco_TICLCandidate_h

#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/HGCalReco/interface/Trackster.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

// A TICLCandidate is a lightweight physics object made from one or multiple Tracksters.

namespace ticl {
class TICLCandidate : public reco::LeafCandidate {
 public:
  TICLCandidate(Charge q, const LorentzVector& p4) : LeafCandidate(q, p4), time_(0.f), timeError_(-1.f), rawEnergy_(0.f) {
  }

  TICLCandidate() : LeafCandidate(), time_(0.f), timeError_(-1.f) {
  }

  inline float time() const { return time_; }
  inline float timeError() const { return timeError_; }

  void setTime(float time) { time_ = time; };
  void setTimeError(float timeError) { timeError_ = timeError; }

  // inline const reco::TrackRef trackRef() const { return trackRef_; }
  // void setTrackRef(const reco::TrackRef& trackRef);

  inline const edm::Ptr<reco::Track> trackPtr() const { return trackPtr_; }
  void setTrackPtr(const edm::Ptr<reco::Track>& trackPtr) {
    trackPtr_ = trackPtr;
  }

  inline float rawEnergy() const { return rawEnergy_;}
  void setRawEnergy(float rawEnergy) { rawEnergy_ = rawEnergy;}

  inline const std::vector<edm::Ptr<Trackster> > tracksters() const {
    return tracksters_;
  };

  void setTracksters(const std::vector<edm::Ptr<Trackster> >& tracksters) {
    tracksters_ = tracksters;
  }
  void addTrackster(const edm::Ptr<Trackster>& trackster) {
    tracksters_.push_back(trackster);
  }

  // convenience methods to return certain id probabilities
  inline float photonProbability() const { return idProbabilities_[0]; }
  inline float electronProbability() const { return idProbabilities_[1]; }
  inline float muonProbability() const { return idProbabilities_[2]; }
  inline float chargedHadronProbability() const { return idProbabilities_[3]; }
  inline float neutralHadronProbability() const { return idProbabilities_[4]; }
  inline float ambiguousProbability() const { return idProbabilities_[5]; }
  inline float unknownProbability() const { return idProbabilities_[6]; }

  void setIdProbabilities(const std::array<float, 7>& idProbs) {
    idProbabilities_ = idProbs;
  }

 private:
  float time_;
  float timeError_;
  edm::Ptr<reco::Track> trackPtr_;

  float rawEnergy_;

  // vector of Ptr so Tracksters can come from different collections
  // and there can be derived classes
  std::vector<edm::Ptr<Trackster> > tracksters_;

  // Since it contains multiple tracksters, duplicate the probability interface
  std::array<float, 7> idProbabilities_;
};
}  // namespace ticl
#endif
