#ifndef CommonTools_RecoAlgos_PrimaryVertexSorting_
#define CommonTools_RecoAlgos_PrimaryVertexSorting_

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "CommonTools/RecoAlgos/interface/PrimaryVertexAssignment.h"



class PrimaryVertexSorting {
 public:
 
  PrimaryVertexSorting(const edm::ParameterSet& iConfig):
   useMet_(iConfig.getParameter<bool>("useMet")),
   jetWeight_(iConfig.getParameter<double>("jetWeight")),
   metSubtractionFactor_(iConfig.getParameter<double>("metSubtractionFactor")),
   ptErrorSubtractionFactor_(iConfig.getParameter<double>("ptErrorSubtractionFactor"))
  {}

  ~PrimaryVertexSorting(){}
  float score(const reco::Vertex & pv, const std::vector<const reco::Candidate *> & candidates ) const ;

 private  :
  bool useMet_;
  double jetWeight_;
  double metSubtractionFactor_;
  double ptErrorSubtractionFactor_;
};

#endif
