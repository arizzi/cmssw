import FWCore.ParameterSet.Config as cms

from RecoVertex.AdaptiveVertexFinder.inclusiveVertexFinder_cfi import *
from RecoVertex.AdaptiveVertexFinder.vertexMerger_cfi import *
from RecoVertex.AdaptiveVertexFinder.trackVertexArbitrator_cfi import *

inclusiveSecondaryVertices = vertexMerger.clone()
inclusiveSecondaryVertices.secondaryVertices = cms.InputTag("trackVertexArbitrator")
inclusiveSecondaryVertices.maxFraction = 0.2
inclusiveSecondaryVertices.minSignificance = 10.

inclusiveVertexing = cms.Sequence(inclusiveVertexFinder*vertexMerger*trackVertexArbitrator*inclusiveSecondaryVertices)

from RecoVertex.AdaptiveVertexFinder.inclusiveCandidateVertexFinder_cfi import *
from RecoVertex.AdaptiveVertexFinder.candidateVertexMerger_cfi import *
from RecoVertex.AdaptiveVertexFinder.candidateVertexArbitrator_cfi import *

inclusiveCandidateSecondaryVertices = candidateVertexMerger.clone()
inclusiveCandidateSecondaryVertices.secondaryVertices = cms.InputTag("candidateVertexArbitrator")
inclusiveCandidateSecondaryVertices.maxFraction = 0.2
inclusiveCandidateSecondaryVertices.minSignificance = 10.



from RecoVertex.AdaptiveVertexFinder.inclusiveCandidatePtrVertexFinder_cfi import *
from RecoVertex.AdaptiveVertexFinder.candidateVertexMerger_cfi import *
from RecoVertex.AdaptiveVertexFinder.candidatePtrVertexArbitrator_cfi import *

candidatePtrVertexMerger = candidateVertexMerger.clone()
candidatePtrVertexMerger.secondaryVertices = cms.InputTag("inclusiveCandidatePtrVertexFinder")

inclusiveCandidatePtrSecondaryVertices = candidateVertexMerger.clone()
inclusiveCandidatePtrSecondaryVertices.secondaryVertices = cms.InputTag("candidatePtrVertexArbitrator")
inclusiveCandidatePtrSecondaryVertices.maxFraction = 0.2
inclusiveCandidatePtrSecondaryVertices.minSignificance = 10.
candidatePtrVertexArbitrator.secondaryVertices = cms.InputTag("candidatePtrVertexMerger")

inclusiveVertexing = cms.Sequence(inclusiveVertexFinder*vertexMerger*trackVertexArbitrator*inclusiveSecondaryVertices)
inclusiveCandidateVertexing = cms.Sequence(inclusiveCandidateVertexFinder*candidateVertexMerger*candidateVertexArbitrator*inclusiveCandidateSecondaryVertices)
inclusiveCandidatePtrVertexing = cms.Sequence(inclusiveCandidatePtrVertexFinder*candidatePtrVertexMerger*candidatePtrVertexArbitrator*inclusiveCandidatePtrSecondaryVertices)

