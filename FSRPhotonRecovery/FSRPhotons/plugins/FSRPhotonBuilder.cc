// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloTopology/interface/CaloTopology.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"

#include "RecoEcal/EgammaCoreTools/interface/EcalClusterTools.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "FWCore/Utilities/interface/isFinite.h"
#include "PhysicsTools/PatAlgos/interface/ObjectModifier.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Common/interface/RefToPtr.h"

#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/PhotonCore.h"
#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"
#include "DataFormats/EgammaReco/interface/ClusterShape.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/EgammaReco/interface/ElectronSeed.h"
#include "RecoCaloTools/Selectors/interface/CaloConeSelector.h"

#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgo.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgoRcd.h"

#include "RecoEcal/EgammaCoreTools/interface/EcalClusterFunctionBaseClass.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterFunctionFactory.h"
#include "RecoEcal/EgammaCoreTools/plugins/EcalClusterCrackCorrection.h"
#include "RecoEgamma/EgammaIsolationAlgos/interface/EgammaHadTower.h"
#include "RecoEgamma/EgammaIsolationAlgos/interface/EgammaTowerIsolation.h"
#include "RecoEgamma/EgammaPhotonProducers/interface/PhotonProducer.h"

//----------------------------------------------------------------------// 
// FSRPhotonBuilder, 15.3.2019, oliver.rieger@cern.ch                   // 
// E X P E R I M E N T A L !!!                                          //  
//----------------------------------------------------------------------//

class FSRPhotonBuilder : public edm::EDProducer {
public:
  explicit FSRPhotonBuilder(const edm::ParameterSet &);
  ~FSRPhotonBuilder();

private:
  virtual void produce(edm::Event &, const edm::EventSetup &);
  double ptThresh_;
  edm::EDGetTokenT<reco::PhotonCoreCollection> photonCoreToken_;
  edm::EDGetTokenT<reco::SuperClusterCollection> scToken_;
  // edm::EDGetTokenT<EcalRecHitCollection> ecalBarrelHitToken_;
  // edm::EDGetTokenT<EcalRecHitCollection> ecalEndcapHitToken_;
  edm::EDGetTokenT<reco::VertexCollection> vertexToken_;
};

FSRPhotonBuilder::FSRPhotonBuilder(const edm::ParameterSet &iConfig)
  : ptThresh_(iConfig.getParameter<double>("ptThresh")),
    photonCoreToken_(consumes<reco::PhotonCoreCollection>(iConfig.getParameter<edm::InputTag>("photonCore"))),
    scToken_(consumes<reco::SuperClusterCollection>(iConfig.getParameter<edm::InputTag>("superCluster"))),
    // ecalBarrelHitToken_(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("ecalBarrelRecHit"))),
    // ecalEndcapHitToken_(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("ecalEndcapRecHit"))),
    vertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertex"))) 
{
  produces<pat::PhotonCollection>();
}

FSRPhotonBuilder::~FSRPhotonBuilder() {}

void FSRPhotonBuilder::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {
  
  std::unique_ptr<pat::PhotonCollection> phot(new pat::PhotonCollection);
  
  edm::Handle<reco::PhotonCoreCollection> photonCoreHandle;
  iEvent.getByToken(photonCoreToken_, photonCoreHandle);
  
  edm::Handle<reco::SuperClusterCollection> SuperClusterHandle;
  iEvent.getByToken(scToken_, SuperClusterHandle);

  // bool validBarrelEcalRecHits = true;
  // edm::Handle<EcalRecHitCollection> barrelHitHandle;
  // EcalRecHitCollection barrelRecHits;
  // iEvent.getByToken(ecalBarrelHitToken_, barrelHitHandle);

  // bool validEndcapEcalRecHits = true;
  // edm::Handle<EcalRecHitCollection> endcapHitHandle;
  // EcalRecHitCollection endcapRecHits;
  // iEvent.getByToken(ecalEndcapHitToken_, endcapHitHandle);

  edm::Handle<reco::VertexCollection> vertexHandle;
  iEvent.getByToken(vertexToken_, vertexHandle);

  bool PV_found = false;
  unsigned int tmpIndex = 0;
  unsigned int vertexIndex = 0;
  for (reco::VertexCollection::const_iterator vtr = vertexHandle->begin();
       vtr != vertexHandle->end(); ++vtr) {
    if (!(vtr->isFake()) && vtr->ndof() > 4 && fabs(vtr->z()) <= 24. &&
        fabs(vtr->position().Rho()) <= 2.) {
      vertexIndex = tmpIndex;
      PV_found = true;
      break;
    }
    tmpIndex++;
  }
  if (PV_found) { 
    reco::Vertex vtx = vertexHandle->at(vertexIndex);
  
    for (unsigned int i = 0; i < photonCoreHandle->size(); i++) {

      if (std::abs(photonCoreHandle->at(i).superCluster()->eta()) > 2.4 || photonCoreHandle->at(i).superCluster()->energy() < ptThresh_)
	continue;
      if (photonCoreHandle->at(i).superCluster()->energy()/std::cosh(photonCoreHandle->at(i).superCluster()->eta()) <= 2)
	continue;
    
      // if (!barrelHitHandle.isValid()) {
      // 	edm::LogError("PhotonProducer")<< "Error! Can't get the barrelEcalHits";
      // 	validBarrelEcalRecHits = false;
      // }
    
      // if (validBarrelEcalRecHits)
      // 	barrelRecHits = *(barrelHitHandle.product());

      // if (!endcapHitHandle.isValid()) {
      // 	edm::LogError("PhotonProducer")<< "Error! Can't get the endcapEcalHits";
      // 	validEndcapEcalRecHits = false;
      // }
    
      // if (validEndcapEcalRecHits)
      // 	endcapRecHits = *(endcapHitHandle.product());
    
      // noZS::EcalClusterLazyTools lazyToolsNoZS(iEvent, iSetup, ecalBarrelHitToken_, ecalEndcapHitToken_);
      // photonModifier_->setEvent(iEvent);
      // photonModifier_->setEventContent(iSetup);

      // edm::ESHandle<CaloTopology> theCaloTopo_;
      // iSetup.get<CaloTopologyRecord>().get(theCaloTopo_);
      // const CaloTopology *topology = theCaloTopo_.product();

      // float e3x3 = EcalClusterTools::e3x3(*(photonCoreHandle->at(i).superCluster()->seed()), barrelHitHandle.product(), topology);
      // std::vector<float> locCov = EcalClusterTools::localCovariances(*(photonCoreHandle->at(i).superCluster()->seed()), barrelHitHandle.product(), topology);
      // float sigmaIetaIeta = sqrt(locCov[0]);
      // float r9 = e3x3 / (photonCoreHandle->at(i).superCluster()->rawEnergy());

      double energy = photonCoreHandle->at(i).superCluster()->energy();
      double energyUncertainty = photonCoreHandle->at(i).superCluster()->correctedEnergyUncertainty();
      math::XYZVector direction = photonCoreHandle->at(i).superCluster()->position() - vtx.position();
      math::XYZVector momentum = direction.unit() * energy;
      const reco::Particle::LorentzVector p4(momentum.x(), momentum.y(), momentum.z(), energy);

      reco::PhotonCoreRef coreRef(reco::PhotonCoreRef(photonCoreHandle, i));

      reco::Photon newCandidate(p4, photonCoreHandle->at(i).superCluster()->position(), coreRef, vtx.position());

      pat::Photon pho(newCandidate);
      // pho.addUserFloat("sigmaIetaIeta", sigmaIetaIeta);
      // pho.addUserFloat("r9", r9);
      pho.addUserFloat("energyUncertainty", energyUncertainty);
      phot->push_back(newCandidate);
    }
  }
  iEvent.put(std::move(phot));
    
}

DEFINE_FWK_MODULE(FSRPhotonBuilder);
