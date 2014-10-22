// -*- C++ -*-
//
// Package:    V0Producer
// Class:      V0Fitter
// 
/**\class V0Fitter V0Fitter.cc RecoVertex/V0Producer/src/V0Fitter.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Brian Drell
//         Created:  Fri May 18 22:57:40 CEST 2007
//
//

#include "V0Fitter.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/PatternTools/interface/ClosestApproachInRPhi.h"
#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateTransform.h"
#include "TrackingTools/PatternTools/interface/TSCBLBuilderNoMaterial.h"

#include <Math/Functions.h>
#include <Math/SVector.h>
#include <Math/SMatrix.h>
#include <typeinfo>
#include <memory>

// pdg mass constants
namespace {
   const double piMass = 0.13957018;
   const double piMassSquared = piMass*piMass;
   const double protonMass = 0.938272046;
   const double protonMassSquared = protonMass*protonMass;
   const double KShortMass = 0.497614;
   const double LambdaMass = 1.115683;
}

// constructor
V0Fitter::V0Fitter(const edm::ParameterSet& theParameters, edm::ConsumesCollector && iC)
{
   using std::string;

   // which track collection to use
   token_tracks = iC.consumes<reco::TrackCollection>(theParameters.getParameter<edm::InputTag>("trackRecoAlgorithm"));

   // whether to reconstruct K0s
   doKShorts_ = theParameters.getParameter<bool>(string("doKShorts"));
   // whether to reconstruct Lambdas
   doLambdas_ = theParameters.getParameter<bool>(string("doLambdas"));

   // which vertex fitting algorithm to use
   vtxFitter = theParameters.getParameter<edm::InputTag>("vertexFitter");

   // whether to use the refit tracks for V0 kinematics
   useRefTrax = theParameters.getParameter<bool>(string("useSmoothing"));

   // cuts on the input track collection
   std::vector<std::string> qual = theParameters.getParameter<std::vector<std::string> >("trackQualities");
   for (unsigned int ndx = 0; ndx < qual.size(); ndx++) {
      qualities.push_back(reco::TrackBase::qualityByName(qual[ndx]));
   }
   tkChi2Cut_ = theParameters.getParameter<double>(string("tkChi2Cut"));
   tkPtCut_ = theParameters.getParameter<double>(string("tkPtCut"));  
   tkNhitsCut_ = theParameters.getParameter<int>(string("tkNhitsCut"));
   tkIPSigCut_ = theParameters.getParameter<double>(string("tkIPSigCut"));
   // cuts on the V0 vertex
   vtxChi2Cut_ = theParameters.getParameter<double>(string("vtxChi2Cut"));
   vtxRCut_ = theParameters.getParameter<double>(string("vtxRCut"));
   vtxRSigCut_ = theParameters.getParameter<double>(string("vtxRSigCut"));
   // miscellaneous cuts after vertexing
   //mPiPiCut_ = theParameters.getParameter<double>(string("mPiPiCut"));
   tkDCACut_ = theParameters.getParameter<double>(string("tkDCACut"));
   KShortMassCut_ = theParameters.getParameter<double>(string("KShortMassCut"));
   LambdaMassCut_ = theParameters.getParameter<double>(string("LambdaMassCut"));
   innerHitPosCut_ = theParameters.getParameter<double>(string("innerHitPosCut"));
   V0costhetaCut_ = theParameters.getParameter<double>(string("V0costhetaCut"));

   //edm::LogInfo("V0Producer") << "Using " << vtxFitter << " to fit V0 vertices.\n"; 
   //std::cout << "Using " << vtxFitter << " to fit V0 vertices." << std::endl; 
   // FOR DEBUG: 
   //initFileOutput(); 
   //-------------------- 
   //std::cout << "Entering V0Producer" << std::endl; 
   // FOR DEBUG: 
   //cleanupFileOutput(); 
   //-------------------- 

}

// method containing the algorithm for vertex reconstruction
void V0Fitter::fitAll(const edm::Event& iEvent, const edm::EventSetup& iSetup,
   reco::VertexCompositeCandidateCollection & theKShorts, reco::VertexCompositeCandidateCollection & theLambdas)
{
   using std::vector;
   using std::cout;
   using std::endl;
   using namespace reco;
   using namespace edm;

   Handle<reco::TrackCollection> TrackHandle;
   iEvent.getByToken(token_tracks, TrackHandle);
   if (!TrackHandle->size()) return;

   edm::Handle<reco::BeamSpot> BeamSpotHandle;
   iEvent.getByLabel("offlineBeamSpot", BeamSpotHandle);
   const GlobalPoint BeamSpotPos(BeamSpotHandle->position().x(), BeamSpotHandle->position().y(), BeamSpotHandle->position().z());

   ESHandle<MagneticField> bFieldHandle;
   iSetup.get<IdealMagneticFieldRecord>().get(bFieldHandle);
   const MagneticField* magField = bFieldHandle.product();

   ESHandle<GlobalTrackingGeometry> globTkGeomHandle;
   iSetup.get<GlobalTrackingGeometryRecord>().get(globTkGeomHandle);

   // create std::vectors for Tracks and TrackRefs (required for passing to the KalmanVertexFitter)
   std::vector<TrackRef> theTrackRefs;
   std::vector<TransientTrack> theTransTracks;

   // fill vectors of TransientTracks and TrackRefs which pass selection cuts
   for (unsigned int indx = 0; indx < TrackHandle->size(); indx++) {
      TrackRef tmpRef(TrackHandle, indx);
      bool quality_ok = true;
      if (qualities.size()!=0) {
         quality_ok = false;
         for (unsigned int ndx_ = 0; ndx_ < qualities.size(); ndx_++) {
            if (tmpRef->quality(qualities[ndx_])) {
               quality_ok = true;
               break;
            }
         }
      }
      if (quality_ok) {
         if (tmpRef->normalizedChi2() < tkChi2Cut_ && tmpRef->pt() > tkPtCut_ && tmpRef->numberOfValidHits() >= tkNhitsCut_) {
            FreeTrajectoryState initialFTS = trajectoryStateTransform::initialFreeState(*tmpRef, magField);
            TSCBLBuilderNoMaterial blsBuilder;
            TrajectoryStateClosestToBeamLine tscb(blsBuilder(initialFTS, *BeamSpotHandle));
            if (tscb.isValid()) {
               if (tscb.transverseImpactParameter().significance() > tkIPSigCut_) {
                  theTrackRefs.push_back(std::move(tmpRef));
                  TransientTrack tmpTk(*tmpRef, &(*bFieldHandle), globTkGeomHandle);
                  theTransTracks.push_back(std::move(tmpTk));
               }
            }
         }
      }
   }
   // good tracks have now been selected for vertexing

   // loop over tracks and vertex good charged track pairs
   for (unsigned int trdx1 = 0; trdx1 < theTrackRefs.size(); trdx1++) {
   for (unsigned int trdx2 = trdx1 + 1; trdx2 < theTrackRefs.size(); trdx2++) {

      TrackRef negativeTrackRef;
      TrackRef positiveTrackRef;
      TransientTrack* negTransTkPtr = nullptr;
      TransientTrack* posTransTkPtr = nullptr;
        
      // if the tracks are oppositely charged load them into the appropriate containers
      if (theTrackRefs[trdx1]->charge() < 0. && theTrackRefs[trdx2]->charge() > 0.) {
         negativeTrackRef = theTrackRefs[trdx1];
         positiveTrackRef = theTrackRefs[trdx2];
         negTransTkPtr = &theTransTracks[trdx1];
         posTransTkPtr = &theTransTracks[trdx2];
      } else if (theTrackRefs[trdx1]->charge() > 0. && theTrackRefs[trdx2]->charge() < 0.) {
         negativeTrackRef = theTrackRefs[trdx2];
         positiveTrackRef = theTrackRefs[trdx1];
         negTransTkPtr = &theTransTracks[trdx2];
         posTransTkPtr = &theTransTracks[trdx1];
      } else {
         continue; // try the next pair
      }
     
      // calculate the DCA and POCA for the track pair
      if (!negTransTkPtr->impactPointTSCP().isValid() || !posTransTkPtr->impactPointTSCP().isValid()) continue;
      FreeTrajectoryState const & posState = posTransTkPtr->impactPointTSCP().theState();
      FreeTrajectoryState const & negState = negTransTkPtr->impactPointTSCP().theState();
      ClosestApproachInRPhi cApp;
      cApp.calculate(posState, negState);
      if (!cApp.status()) continue;
      float dca = fabs(cApp.distance());
      if (dca > tkDCACut_) continue;
      GlobalPoint cxPt = cApp.crossingPoint();
      if (sqrt(cxPt.x()*cxPt.x() + cxPt.y()*cxPt.y()) > 120. || std::abs(cxPt.z()) > 300.) continue;

      /* stuff to calculate mPiPi
      // Get trajectory states for the tracks at POCA for later cuts
      TrajectoryStateClosestToPoint const & posTSCP = posTransTkPtr->trajectoryStateClosestToPoint(cxPt);
      TrajectoryStateClosestToPoint const & negTSCP = negTransTkPtr->trajectoryStateClosestToPoint(cxPt);
      if (!posTSCP.isValid() || !negTSCP.isValid()) continue;
      double posESq = posTSCP.momentum().mag2() + piMassSquared;
      double negESq = negTSCP.momentum().mag2() + piMassSquared;
      double posE = sqrt(posESq);
      double negE = sqrt(negESq);
      double totalE = posE + negE;
      double totalE = sqrt(posTSCP.momentum().mag2() + piMassSquared) + sqrt(negTSCP.momentum().mag2() + piMassSquared);
      double totalESq = totalE*totalE;
      double totalPSq = (posTSCP.momentum() + negTSCP.momentum()).mag2();
      double mass = sqrt(totalESq - totalPSq);
      //mPiPiMassOut << mass << std::endl;
      if (mass > mPiPiCut) continue;
      */

      // fill the vector of TransientTracks to give to the vertexers
      std::vector<TransientTrack> transTracks;
      transTracks.reserve(2);
      transTracks.push_back(*posTransTkPtr);
      transTracks.push_back(*negTransTkPtr);

      // create the vertex fitter object and vertex the tracks
      TransientVertex theRecoVertex;
      if (vtxFitter == std::string("KalmanVertexFitter")) {
         KalmanVertexFitter theKalmanFitter(useRefTrax == 0 ? false : true);
         theRecoVertex = theKalmanFitter.vertex(transTracks);
      } else if (vtxFitter == std::string("AdaptiveVertexFitter")) {
         useRefTrax = false;
         AdaptiveVertexFitter theAdaptiveFitter;
         theRecoVertex = theAdaptiveFitter.vertex(transTracks);
      }
      if (!theRecoVertex.isValid()) continue;

      // create reco::Vertex object for use in creating the Candidate
      reco::Vertex theVtx = theRecoVertex;
      if (theVtx.normalizedChi2() > vtxChi2Cut_) continue;

      // calculate radial displacement of V0 vertex from beamspot (z uncertainty is large)
      typedef ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> > SMatrixSym3D;
      typedef ROOT::Math::SVector<double, 3> SVector3;
      SMatrixSym3D totalCov = BeamSpotHandle->rotatedCovariance3D() + theVtx.covariance();
      SVector3 distanceVector(theVtx.x()-BeamSpotPos.x(), theVtx.y()-BeamSpotPos.y(), 0.);
      double rVtxMag = ROOT::Math::Mag(distanceVector);
      if (rVtxMag < vtxRCut_) continue;
      double sigmaRvtxMag = sqrt(ROOT::Math::Similarity(totalCov, distanceVector)) / rVtxMag;
      if (rVtxMag / sigmaRvtxMag < vtxRSigCut_) continue;

      // see if either daughter track has hits "inside" the vertex
      // (the methods innerOk() and innerPosition() require TrackExtra which is only available in the RECO data tier - 
      //  setting innerHitPosCut to -1 avoids this problem and allows to run on AOD)
      if (innerHitPosCut_ > 0. && positiveTrackRef->innerOk()) {
         reco::Vertex::Point posTkHitPos = positiveTrackRef->innerPosition();
         double posTkHitPosD2 =
            (posTkHitPos.x()-BeamSpotPos.x())*(posTkHitPos.x()-BeamSpotPos.x()) +
            (posTkHitPos.y()-BeamSpotPos.y())*(posTkHitPos.y()-BeamSpotPos.y());
         if (sqrt(posTkHitPosD2) < (rVtxMag - sigmaRvtxMag*innerHitPosCut_)) continue;
      }
      if (innerHitPosCut_ > 0. && negativeTrackRef->innerOk()) {
         reco::Vertex::Point negTkHitPos = negativeTrackRef->innerPosition();
         double negTkHitPosD2 =
            (negTkHitPos.x()-BeamSpotPos.x())*(negTkHitPos.x()-BeamSpotPos.x()) +
            (negTkHitPos.y()-BeamSpotPos.y())*(negTkHitPos.y()-BeamSpotPos.y());
         if (sqrt(negTkHitPosD2) < (rVtxMag - sigmaRvtxMag*innerHitPosCut_)) continue;
      }

      // create and fill vector of refitted TransientTracks (iff they've been created by the KVF)
      std::vector<TransientTrack> refittedTrax;
      if (theRecoVertex.hasRefittedTracks()) {
         refittedTrax = theRecoVertex.refittedTracks();
      }

      // make TrajectoryStates to extract momentum of daughter tracks at vertex
      std::auto_ptr<TrajectoryStateClosestToPoint> trajPlus;
      std::auto_ptr<TrajectoryStateClosestToPoint> trajMins;
      const GlobalPoint vtxPos(theVtx.x(), theVtx.y(), theVtx.z());

      if (useRefTrax && refittedTrax.size() > 1) {
         // TransientTrack objects to hold the positive and negative refitted tracks
         TransientTrack* thePositiveRefTrack = 0;
         TransientTrack* theNegativeRefTrack = 0;
         for (std::vector<TransientTrack>::iterator iTrack = refittedTrax.begin(); iTrack != refittedTrax.end(); ++iTrack) {
            if (iTrack->track().charge() > 0.) {
               thePositiveRefTrack = &*iTrack;
            } else if (iTrack->track().charge() < 0.) {
               theNegativeRefTrack = &*iTrack;
            }
         }
        if (thePositiveRefTrack == 0 || theNegativeRefTrack == 0) continue;
        trajPlus.reset(new TrajectoryStateClosestToPoint(thePositiveRefTrack->trajectoryStateClosestToPoint(vtxPos)));
        trajMins.reset(new TrajectoryStateClosestToPoint(theNegativeRefTrack->trajectoryStateClosestToPoint(vtxPos)));
      } else {
         trajPlus.reset(new TrajectoryStateClosestToPoint(posTransTkPtr->trajectoryStateClosestToPoint(vtxPos)));
         trajMins.reset(new TrajectoryStateClosestToPoint(negTransTkPtr->trajectoryStateClosestToPoint(vtxPos)));
      }
      if (trajPlus.get() == 0 || trajMins.get() == 0 || !trajPlus->isValid() || !trajMins->isValid()) continue;

      GlobalVector positiveP(trajPlus->momentum());
      GlobalVector negativeP(trajMins->momentum());
      GlobalVector totalP(positiveP + negativeP);

      // calculate the pointing angle
      double posx = theVtx.x() - BeamSpotHandle->position().x();
      double posy = theVtx.y() - BeamSpotHandle->position().y();
      double momx = totalP.x();
      double momy = totalP.y();
      double pointangle = (posx*momx+posy*momy)/(sqrt(posx*posx+posy*posy)*sqrt(momx*momx+momy*momy));
      if (pointangle < V0costhetaCut_) continue;

      // calculate total energy of V0 3 ways: assume a KShort, Lambda, or LambdaBar
      double piPlusE = sqrt(positiveP.mag2() + piMassSquared);
      double piMinusE = sqrt(negativeP.mag2() + piMassSquared);
      double protonE = sqrt(positiveP.mag2() + protonMassSquared);
      double antiProtonE = sqrt(negativeP.mag2() + protonMassSquared);
      double KShortETot = piPlusE + piMinusE;
      double LambdaEtot = protonE + piMinusE;
      double LambdaBarEtot = antiProtonE + piPlusE;

      // create momentum 4-vectors for the 3 candidate types
      const Particle::LorentzVector KShortP4(totalP.x(), totalP.y(), totalP.z(), KShortETot);
      const Particle::LorentzVector LambdaP4(totalP.x(), totalP.y(), totalP.z(), LambdaEtot);
      const Particle::LorentzVector LambdaBarP4(totalP.x(), totalP.y(), totalP.z(), LambdaBarEtot);

      Particle::Point vtx(theVtx.x(), theVtx.y(), theVtx.z());
      const Vertex::CovarianceMatrix vtxCov(theVtx.covariance());
      double vtxChi2(theVtx.chi2());
      double vtxNdof(theVtx.ndof());

      // create the VertexCompositeCandidate object that will be stored in the Event
      VertexCompositeCandidate* theKShort = nullptr;
      VertexCompositeCandidate* theLambda = nullptr;
      VertexCompositeCandidate* theLambdaBar = nullptr;

      if (doKShorts_) {
         theKShort = new VertexCompositeCandidate(0, KShortP4, vtx, vtxCov, vtxChi2, vtxNdof);
      }
      if (doLambdas_) {
         if (positiveP.mag2() > negativeP.mag2()) {
            theLambda = new VertexCompositeCandidate(0, LambdaP4, vtx, vtxCov, vtxChi2, vtxNdof);
         } else {
            theLambdaBar = new VertexCompositeCandidate(0, LambdaBarP4, vtx, vtxCov, vtxChi2, vtxNdof);
         }
      }

      // create daughter candidates for the VertexCompositeCandidates
      RecoChargedCandidate thePiPlusCand(
         1, Particle::LorentzVector(positiveP.x(), positiveP.y(), positiveP.z(), piPlusE), vtx);
      thePiPlusCand.setTrack(positiveTrackRef);
      
      RecoChargedCandidate thePiMinusCand(
         -1, Particle::LorentzVector(negativeP.x(), negativeP.y(), negativeP.z(), piMinusE), vtx);
      thePiMinusCand.setTrack(negativeTrackRef);
      
      RecoChargedCandidate theProtonCand(
         1, Particle::LorentzVector(positiveP.x(), positiveP.y(), positiveP.z(), protonE), vtx);
      theProtonCand.setTrack(positiveTrackRef);

      RecoChargedCandidate theAntiProtonCand(
         -1, Particle::LorentzVector(negativeP.x(), negativeP.y(), negativeP.z(), antiProtonE), vtx);
      theAntiProtonCand.setTrack(negativeTrackRef);

      AddFourMomenta addp4;
      // store the daughter Candidates in the VertexCompositeCandidates if they pass mass cuts
      if (doKShorts_) {
         theKShort->addDaughter(thePiPlusCand);
         theKShort->addDaughter(thePiMinusCand);
         theKShort->setPdgId(310);
         addp4.set(*theKShort);
         if (theKShort->mass() < KShortMass+KShortMassCut_ && theKShort->mass() > KShortMass-KShortMassCut_) {
            theKShorts.push_back(std::move(*theKShort));
         }
      }      
      if (doLambdas_ && theLambda) {
         theLambda->addDaughter(theProtonCand);
         theLambda->addDaughter(thePiMinusCand);
         theLambda->setPdgId(3122);
         addp4.set(*theLambda);
         if (theLambda->mass() < LambdaMass+LambdaMassCut_ && theLambda->mass() > LambdaMass-LambdaMassCut_) {
            theLambdas.push_back(std::move(*theLambda));
         }
      } else if (doLambdas_ && theLambdaBar) {
         theLambdaBar->addDaughter(theAntiProtonCand);
         theLambdaBar->addDaughter(thePiPlusCand);
         theLambdaBar->setPdgId(-3122);
         addp4.set(*theLambdaBar);
         if (theLambdaBar->mass() < LambdaMass+LambdaMassCut_ && theLambdaBar->mass() > LambdaMass-LambdaMassCut_) {
            theLambdas.push_back(std::move(*theLambdaBar));
         }
      }

      delete theKShort;
      delete theLambda;
      delete theLambdaBar;
      theKShort = theLambda = theLambdaBar = nullptr;

   }
   }

}

/*
double V0Fitter::findV0MassError(const GlobalPoint &vtxPos, const std::vector<reco::TransientTrack> &dauTracks)
{ 
  return -1.;
}
double V0Fitter::findV0MassError(const GlobalPoint &vtxPos, std::vector<reco::TransientTrack> const & dauTracks)
{
   // Returns -99999. if trajectory states fail at vertex position
   // Load positive track trajectory at vertex into vector, then negative track
   std::vector<TrajectoryStateClosestToPoint> sortedTrajStatesAtVtx;
   for (unsigned int ndx = 0; ndx < dauTracks.size(); ndx++) {
      if (dauTracks[ndx].trajectoryStateClosestToPoint(vtxPos).isValid()) {
         std::cout << "From TSCP: " <<
            dauTracks[ndx].trajectoryStateClosestToPoint(vtxPos).perigeeParameters().transverseCurvature() <<
            "; From Track: " << dauTracks[ndx].track().qoverp() << std::endl;
      }
      if (sortedTrajStatesAtVtx.size() == 0) {
         if (dauTracks[ndx].charge() > 0) {
            sortedTrajStatesAtVtx.push_back(dauTracks[ndx].trajectoryStateClosestToPoint(vtxPos));
         } else {
            sortedTrajStatesAtVtx.push_back(dauTracks[ndx].trajectoryStateClosestToPoint(vtxPos));
         }
      }
  }
   std::vector<PerigeeTrajectoryParameters> param;
   std::vector<PerigeeTrajectoryError> paramError;
   std::vector<GlobalVector> momenta;
   for (unsigned int ndx2 = 0; ndx2 < sortedTrajStatesAtVtx.size(); ndx2++) {
      if (sortedTrajStatesAtVtx[ndx2].isValid()) {
         param.push_back(sortedTrajStatesAtVtx[ndx2].perigeeParameters());
         paramError.push_back(sortedTrajStatesAtVtx[ndx2].perigeeError());
         momenta.push_back(sortedTrajStatesAtVtx[ndx2].momentum());
      } else {
         return -99999.;
      }
  }
  return 0;
}
*/

