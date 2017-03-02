from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR,deltaPhi

class NanoAnalyzer( Analyzer ):
    '''Analyzer for NanoAOD
    '''

    def declareHandles(self):
        super(NanoAnalyzer, self).declareHandles()
        self.handles['rhoN'] =  AutoHandle( 'fixedGridRhoFastjetCentralNeutral','double' )

    def process(self, event):
        self.readCollections( event.input )
        event.rhoN=-1
        event.rhoN= self.handles['rhoN'].product()[0]


