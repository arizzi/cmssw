#ifndef PhysicsTools_PFCandProducer_GEDPrimaryVertex_
#define PhysicsTools_PFCandProducer_GEDPrimaryVertex_

// system include files
#include <memory>
#include <string>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Association.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "CommonTools/ParticleFlow/interface/PFPrimaryVertexAssignment.h"
#include "CommonTools/ParticleFlow/interface/PFPrimaryVertexSorting.h"

/**\class GEDPrimaryVertex

*/




class GEDPrimaryVertex : public edm::stream::EDProducer<> {
 public:

  typedef edm::Association<reco::VertexCollection> PFCandToVertex;
  typedef edm::ValueMap<int> PFCandToVertexQuality;

  typedef std::vector< edm::FwdPtr<reco::PFCandidate> >  PFCollection;
  typedef edm::View<reco::PFCandidate>                   PFView;

  explicit GEDPrimaryVertex(const edm::ParameterSet&);

  ~GEDPrimaryVertex();

  virtual void produce(edm::Event&, const edm::EventSetup&) override;

 private:

  PFPrimaryVertexAssignment    assignmentAlgo_;
  PFPrimaryVertexSorting       sortingAlgo_;

  /// PFCandidates to be analyzed
  edm::EDGetTokenT<PFCollection>   tokenPFCandidates_;
  /// fall-back token
  edm::EDGetTokenT<PFView>   tokenPFCandidatesView_;

  /// vertices
  edm::EDGetTokenT<reco::VertexCollection>   tokenVertices_;
  edm::EDGetTokenT<edm::View<reco::Candidate> >   tokenJets_;

  bool produceOriginalMapping_;
  bool produceSortedVertices_;
  bool producePFPileUp_;
  bool producePFNoPileUp_;
  int  qualityCut_;
};

#endif
