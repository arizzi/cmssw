# FSR Photon Recovery 

Collection of CMSSW modules to implement Particle Flow (PF) photons radiated by muons (FSR photons)

## Setup 

```
export SCRAM_ARCH=slc6_amd64_gcc630
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_9_4_9
cd CMSSW_9_4_9/src
cmsenv
git clone https://gitlab.cern.ch/uhh-cmssw/fsr-photon-recovery.git FSRPhotonRecovery
cd FSRPhotonRecovery
scram b -j8
```
## Implementation

In order to add FSR photons to your analyzer you can simply add the following piece of code in your python config
```
from FSRPhotonRecovery.FSRPhotons.FSRphotonSequence_cff import addFSRphotonSequence 
addFSRphotonSequence(process, 'slimmedMuons', PathToPhotonMVAWeightFile)
```
and add the FSRPhotonSequence in your path
```
cms.Path(process.FSRphotonSequence
	*process.YourAnalyzer)
```
Furthermore, you can find a full example on how to run the code here
```
FSRPhotonRecovery/FSRPhotons/python/testFSRphotonSequence_cfg.py

```
## Embedded UserData

In order to access useful information of the photons more easily, we added UserFloats to the photons. You can acess these via
```cpp
photon.userFloat("USERFLOATNAME")
```
Quantities which are used to select the FSR photons are the following     
```
FSRphotonMVAValue, PFphotonIso03, ETgammadeltaR 
```
Besides, the closest muon is saved via the UserCand function.
```cpp
pat::Muon *associatedMuon = (pat::Muon*)(photon.userCand("associatedMuon").get());
```
In case the PF photon exceeds the 10 GeV threshold and we find match to a pat::Photon object, you can also access the following variables
``` 
photonMVAIdValue, photonPuppiIso, EleVeto, hasPixelSeed, correctedPt, correctedEta, correctedPhi
```

## Accessing FSR photons 

The code snippet below shows how to recalculate the muon isolation excluding the selected photons from the muon isolation cone, and the calculation of the full mass reconstruction of FSR events.

```cpp
      edm::Handle<std::vector<pat::Muon>> selectedMuons;
      event.getByLabel(edm::InputTag("selectedMuons"), selectedMuons);
      
      edm::Handle<std::vector<pat::PFParticle>> selectedFSRphotons;
      event.getByLabel(edm::InputTag("FSRRecovery", "selectedFSRphotons"), selectedFSRphotons);
      
      // select photon
      double fsrDrEt2Cut = 0.019;
      double fsrIsoCut = 0.8;

      for (unsigned int i = 0; i < selectedFSRphotons->size(); i++)
      {
        pat::PFParticle photon = selectedFSRphotons->at(i);
        pat::Muon *associatedMuon = (pat::Muon *)(photon.userCand("associatedMuon").get());
        if (photon.userFloat("PFphotonIso03") < fsrIsoCut && photon.userFloat("ETgammadeltaR") < fsrDrEt2Cut)
        {
          reco::CandidatePtr cutBasedFsrPhoton(selectedFSRphotons, i);
          if (associatedMuon->hasUserCand("cutBasedFsrPhoton"))
          {
            pat::PFParticle *tmpPhoton = (pat::PFParticle *)(associatedMuon->userCand("cutBasedFsrPhoton").get());
            if (photon.userFloat("ETgammadeltaR") < tmpPhoton->userFloat("ETgammadeltaR"))
            {
              associatedMuon->addUserCand("cutBasedFsrPhoton", cutBasedFsrPhoton, true);
            }
          }
          else
          {
            associatedMuon->addUserCand("cutBasedFsrPhoton", cutBasedFsrPhoton);
          }
        }
      }

      // remove photon from iso
      bool removeFSRfromIso = true;

      for (unsigned int i = 0; i < selectedMuons->size(); i++)
      {
        pat::Muon mu = selectedMuons->at(i);
        TLorentzVector muLV(mu.px(), mu.py(), mu.pz(), mu.energy());

        double isoCharged = mu.pfIsolationR04().sumChargedHadronPt;
        double isoNeutral = mu.pfIsolationR04().sumNeutralHadronEt + mu.pfIsolationR04().sumPhotonEt;
        double isoCorrection = 0.5 * mu.pfIsolationR04().sumPUPt;

        double miniIsoCharged = mu.userFloat("PFMiniIsoChargedHadronIso");
        double miniIsoNeutral = mu.userFloat("PFMiniIsoNeutralHadronIso") + mu.userFloat("PFMiniIsoPhotonIso");
        double miniIsoCorrection = mu.userFloat("miniIsoEffectiveAreasCorrection");
        if (removeFSRfromIso && mu.hasUserCand("cutBasedFsrPhoton"))
        {
          pat::PFParticle *pho = (pat::PFParticle *)(mu.userCand("cutBasedFsrPhoton").get());
          TLorentzVector phoLV(pho->px(), pho->py(), pho->pz(), pho->energy());
          if (phoLV.DeltaR(muLV) < 0.4)
            isoCorrection += pho->pt();
          if (phoLV.DeltaR(muLV) < std::max(0.05, std::min(0.2, 10. / mu.pt())))
            miniIsoCorrection += pho->pt();
        }

        mu.setIsolation(pat::IsolationKeys(7), (isoCharged + std::max(0., isoNeutral - isoCorrection)) / mu.pt());
        mu.setIsolation(pat::IsolationKeys(8), (miniIsoCharged + std::max(0., miniIsoNeutral - miniIsoCorrection)) / mu.pt());
      }

      // calculate dimuon mass
      double dimuonMass = (selectedMuons->at(0).p4() + selectedMuons->at(1).p4()).M();
      math::XYZTLorentzVector cutBasedPhoton1(0, 0, 0, 0);
      if (selectedMuons->at(0).hasUserCand("cutBasedFsrPhoton"))
      {
        cutBasedPhoton1 = selectedMuons->at(0).userCand("cutBasedFsrPhoton")->p4();
      }
      math::XYZTLorentzVector cutBasedPhoton2(0, 0, 0, 0);
      if (selectedMuons->at(1).hasUserCand("cutBasedFsrPhoton"))
      {
        cutBasedPhoton2 = selectedMuons->at(1).userCand("cutBasedFsrPhoton")->p4();
      }
      double dimuonMass_FSR = (selectedMuons->at(0).p4() + cutBasedPhoton1 + selectedMuons->at(1).p4() + cutBasedPhoton2).M();
```