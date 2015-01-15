#include "CommonTools/ParticleFlow/plugins/GEDPrimaryVertex.h"

#include "DataFormats/ParticleFlowCandidate/interface/PileUpPFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PileUpPFCandidateFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "FWCore/Framework/interface/ESHandle.h"

// #include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/EventSetup.h"


using namespace std;
using namespace edm;
using namespace reco;

GEDPrimaryVertex::GEDPrimaryVertex(const edm::ParameterSet& iConfig) :
  assignmentAlgo_(iConfig.getParameterSet("assignment")),
  sortingAlgo_(iConfig.getParameterSet("sorting")),
  tokenPFCandidates_(consumes<PFCollection>(iConfig.getParameter<InputTag>("PFCandidates"))),
  tokenPFCandidatesView_(mayConsume<PFView>(iConfig.getParameter<InputTag>("PFCandidates"))),
  tokenVertices_(consumes<VertexCollection>(iConfig.getParameter<InputTag>("Vertices"))),
  tokenJets_(consumes<edm::View<reco::Candidate> > (iConfig.getParameter<InputTag>("Jets"))),
  qualityCut_(iConfig.getParameter<int>("QualityForPrimary"))
{
 //could be made configurable if needed
  produceOriginalMapping_=true;
  produceSortedVertices_=true;
  producePFPileUp_=true;
  producePFNoPileUp_=true;


  if(produceOriginalMapping_){
      produces< PFCandToVertex> ("original");
      produces< PFCandToVertexQuality> ("original");
  }
  if(produceSortedVertices_){
      produces< reco::VertexCollection> ();
      produces< PFCandToVertex> ();
      produces< PFCandToVertexQuality> ();
  }

  if(producePFPileUp_){
      if(produceOriginalMapping_)
            produces< PFCollection> ("originalPileUp");
      if(produceSortedVertices_)
            produces< PFCollection> ("PileUp");
  }

  if(producePFNoPileUp_){
      if(produceOriginalMapping_)
            produces< PFCollection> ("originalNoPileUp");
      if(produceSortedVertices_)
            produces< PFCollection> ("NoPileUp");
  }


}



GEDPrimaryVertex::~GEDPrimaryVertex() { }



void GEDPrimaryVertex::produce(Event& iEvent,  const EventSetup& iSetup) {

  Handle<edm::View<reco::Candidate> > jets;
  iEvent.getByToken( tokenJets_, jets);

  edm::ESHandle<TransientTrackBuilder> builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", builder);


  Handle<VertexCollection> vertices;
  iEvent.getByToken( tokenVertices_, vertices);

  Handle<PFCollection> pfCandidates;
  Handle<PFView> pfView;
  PFCollection const * pfCandidatesRef = 0;
  PFCollection usedIfNoFwdPtrs;
  bool getFromFwdPtr = iEvent.getByToken( tokenPFCandidates_, pfCandidates);
  if ( getFromFwdPtr ) {
      pfCandidatesRef = pfCandidates.product();
  } else {
      bool getFromView = iEvent.getByToken( tokenPFCandidatesView_, pfView );
      if ( ! getFromView ) {
	throw cms::Exception("GEDPrimaryVertex is misconfigured. This needs to be either vector<FwdPtr<PFCandidate> >, or View<PFCandidate>");
      }
      for ( edm::View<reco::PFCandidate>::const_iterator viewBegin = pfView->begin(),
	      viewEnd = pfView->end(), iview = viewBegin;
	    iview != viewEnd; ++iview ) {
	usedIfNoFwdPtrs.push_back( edm::FwdPtr<reco::PFCandidate>( pfView->ptrAt(iview-viewBegin), pfView->ptrAt(iview-viewBegin)  ) );
      }
      pfCandidatesRef = &usedIfNoFwdPtrs;
  }

  //in case we migrate away from Fwd stuff
  typedef edm::FwdPtr<reco::PFCandidate> candRefType;

  std::map< candRefType, std::pair<int,PFPrimaryVertexAssignment::Quality> > pfToPVMap;
  std::vector<int> pfToPVVector;
  std::vector<int> pfToPVQualityVector;
  for( auto const & pf : *pfCandidatesRef) {
     std::pair<int,PFPrimaryVertexAssignment::Quality> vtxWithQuality=assignmentAlgo_.chargedHadronVertex(*vertices,*pf,*jets,*builder);
    pfToPVMap[pf]=vtxWithQuality;
    pfToPVVector.push_back(vtxWithQuality.first); 
    pfToPVQualityVector.push_back(vtxWithQuality.second); 
  }

  //reverse mapping
  std::vector< std::vector<std::pair<const reco::PFCandidate &,PFPrimaryVertexAssignment::Quality> > > pvToPFMap(vertices->size());
  for(auto const & pfToPV : pfToPVMap)
  {
    if(pfToPV.second.first >=0 )
       pvToPFMap[pfToPV.second.first].push_back(std::pair<const reco::PFCandidate &,PFPrimaryVertexAssignment::Quality>(*pfToPV.first,pfToPV.second.second));
  }

  std::multimap<float,int> scores;
  for(unsigned int i=0;i<vertices->size();i++){
     scores.insert(std::pair<float,int>(-sortingAlgo_.score((*vertices)[i],pvToPFMap[i]),i));    
  }

  //create indices
  std::vector<int> oldToNew(vertices->size()),  newToOld(vertices->size());
  size_t newIdx=0;
  for(auto const &  idx :  scores)
  {
    oldToNew[idx.second]=newIdx;
    newToOld[newIdx]=idx.second;
    newIdx++;
  }
  



  if(produceOriginalMapping_){
      auto_ptr< PFCandToVertex>  pfCandToVertexOriginalOutput( new PFCandToVertex );
      //FIXME: todo    
  }

  if(produceSortedVertices_){
      std::vector<int> pfToSortedPVVector;
      std::vector<int> pfToSortedPVQualityVector;
      for(size_t i=0;i<pfToPVVector.size();i++) {
        pfToSortedPVVector.push_back(oldToNew[pfToPVVector[i]]);
        pfToSortedPVQualityVector.push_back(pfToPVQualityVector[i]);
      }

      auto_ptr< reco::VertexCollection>  sortedVerticesOutput( new reco::VertexCollection );
      for(size_t i=0;i<vertices->size();i++){
         sortedVerticesOutput->push_back((*vertices)[newToOld[i]]); 
      }
    edm::OrphanHandle<reco::VertexCollection> oh = iEvent.put( sortedVerticesOutput);
    auto_ptr< PFCandToVertex>  pfCandToVertexOutput( new PFCandToVertex(oh) );
    auto_ptr< PFCandToVertexQuality>  pfCandToVertexQualityOutput( new PFCandToVertexQuality() );
    PFCandToVertex::Filler cand2VertexFiller(*pfCandToVertexOutput);
    PFCandToVertexQuality::Filler cand2VertexQualityFiller(*pfCandToVertexQualityOutput);

    if(getFromFwdPtr) {
       cand2VertexFiller.insert(pfCandidates,pfToSortedPVVector.begin(),pfToSortedPVVector.end());
       cand2VertexQualityFiller.insert(pfCandidates,pfToSortedPVQualityVector.begin(),pfToSortedPVQualityVector.end());
    } else  {
       cand2VertexFiller.insert(pfView,pfToSortedPVVector.begin(),pfToSortedPVVector.end());
       cand2VertexQualityFiller.insert(pfView,pfToSortedPVQualityVector.begin(),pfToSortedPVQualityVector.end());
    }
    cand2VertexFiller.fill();
    cand2VertexQualityFiller.fill();
    iEvent.put( pfCandToVertexOutput );
    iEvent.put( pfCandToVertexQualityOutput );
  }

  auto_ptr< PFCollection >  pfCollectionNOPUOriginalOutput( new PFCollection );
  auto_ptr< PFCollection >  pfCollectionNOPUOutput( new PFCollection );
  auto_ptr< PFCollection >  pfCollectionPUOriginalOutput( new PFCollection );
  auto_ptr< PFCollection >  pfCollectionPUOutput( new PFCollection );

  for(size_t i=0;i<pfCandidatesRef->size();i++) {
     auto pvWithQuality = pfToPVMap[(*pfCandidatesRef)[i]];

     if(producePFNoPileUp_ && produceSortedVertices_) 
         if(pvWithQuality.first == newToOld[0] and pvWithQuality.second <= qualityCut_) 
                   pfCollectionNOPUOutput->push_back((*pfCandidatesRef)[i]);

     if(producePFPileUp_ && produceSortedVertices_) 
         if(pvWithQuality.first != newToOld[0] and pvWithQuality.second <= qualityCut_) 
                   pfCollectionPUOutput->push_back((*pfCandidatesRef)[i]);

     if(producePFNoPileUp_ && produceOriginalMapping_) 
         if(pvWithQuality.first == 0 and pvWithQuality.second <= qualityCut_) 
                   pfCollectionNOPUOriginalOutput->push_back((*pfCandidatesRef)[i]);

     if(producePFPileUp_ && produceOriginalMapping_) 
         if(pvWithQuality.first != 0 and pvWithQuality.second <= qualityCut_) 
                   pfCollectionPUOriginalOutput->push_back((*pfCandidatesRef)[i]);

  }              
  if(producePFNoPileUp_ && produceSortedVertices_) iEvent.put(pfCollectionNOPUOutput,"NoPileUp" );
  if(producePFPileUp_ && produceSortedVertices_) iEvent.put(pfCollectionPUOutput, "PileUp");
  if(producePFNoPileUp_ && produceOriginalMapping_) iEvent.put(pfCollectionNOPUOriginalOutput,"originalNoPileUp" );
  if(producePFPileUp_ && produceOriginalMapping_) iEvent.put(pfCollectionPUOriginalOutput,"originalPileUp" );
  

} 

