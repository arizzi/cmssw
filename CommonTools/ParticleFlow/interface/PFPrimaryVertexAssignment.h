#ifndef CommonTools_PFCandProducer_PFPrimaryVertexAssignment_
#define CommonTools_PFCandProducer_PFPrimaryVertexAssignment_

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

class PFPrimaryVertexAssignment {
 public:
  enum Quality {UsedInFit=0,PrimaryDz,BTrack,OtherDz,NotReconstructedPrimary,Unassigned=99};
 
  PFPrimaryVertexAssignment(const edm::ParameterSet& iConfig):
   maxDzSigForPrimaryAssignment_(iConfig.getParameter<double>("maxDzSigForPrimaryAssignment")),
   maxDzForPrimaryAssignment_(iConfig.getParameter<double>("maxDzForPrimaryAssignment")),
   maxJetDeltaR_(iConfig.getParameter<double>("maxJetDeltaR")),
   minJetPt_(iConfig.getParameter<double>("minJetPt")),
   maxDistanceToJetAxis_(iConfig.getParameter<double>("maxDistanceToJetAxis")),
   maxDzForJetAxisAssigment_(iConfig.getParameter<double>("maxDzForJetAxisAssigment")),
   maxDxyForJetAxisAssigment_(iConfig.getParameter<double>("maxDxyForJetAxisAssigment")),
   maxDxySigForNotReconstructedPrimary_(iConfig.getParameter<double>("maxDxySigForNotReconstructedPrimary")),
   maxDxyForNotReconstructedPrimary_(iConfig.getParameter<double>("maxDxyForNotReconstructedPrimary"))
  {}

  ~PFPrimaryVertexAssignment(){}

  std::pair<int,PFPrimaryVertexAssignment::Quality> chargedHadronVertex(const reco::VertexCollection& vertices, 
               const reco::PFCandidate& pfcand,
               const edm::View<reco::Candidate> & jets,
              const TransientTrackBuilder & builder) const;



 private  :
    double    maxDzSigForPrimaryAssignment_;
    double    maxDzForPrimaryAssignment_;
    double    maxJetDeltaR_;
    double    minJetPt_;
    double    maxDistanceToJetAxis_;
    double    maxDzForJetAxisAssigment_;
    double    maxDxyForJetAxisAssigment_;
    double    maxDxySigForNotReconstructedPrimary_;
    double    maxDxyForNotReconstructedPrimary_;
};

#endif
