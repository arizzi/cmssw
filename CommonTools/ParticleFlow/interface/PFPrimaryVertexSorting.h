#ifndef CommonTools_PFCandProducer_PFPrimaryVertexSorting_
#define CommonTools_PFCandProducer_PFPrimaryVertexSorting_

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "CommonTools/ParticleFlow/interface/PFPrimaryVertexAssignment.h"

class PFPrimaryVertexSorting {
 public:
  enum Quality {UsedInFit=0,PrimaryDz,BTrack,OtherDz,NotReconstructedPrimary,Unassigned=99};
 
  PFPrimaryVertexSorting(const edm::ParameterSet& iConfig)
   //minJetPt_(iConfig.getParameter<double>("minJetPt")),
  {}

  ~PFPrimaryVertexSorting(){}
  float score(const reco::Vertex & pv, std::vector<std::pair<const reco::PFCandidate &,PFPrimaryVertexAssignment::Quality> > ) const ;




 private  :
};

#endif
