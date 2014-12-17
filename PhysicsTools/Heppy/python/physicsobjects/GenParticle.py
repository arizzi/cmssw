from PhysicsTools.Heppy.physicsobjects.PhysicsObject import *

class GenParticle( PhysicsObject ):
    def __str__(self):
        base = self.particlePrint()
        theStr = '{base}, status = {status:>2}'.format(base=base, status=self.status())
        return theStr

import ROOT
import FastObjects
FastObjects.decorate(ROOT.reco.GenParticle,GenParticle)


class GenLepton( GenParticle ):
    def sip3D(self):
        '''Just to make generic code work on GenParticles'''
        return 0
    def relIso(self, dummy):
        '''Just to make generic code work on GenParticles'''
        return 0

    def absIso(self, dummy):
        '''Just to make generic code work on GenParticles'''
        return 0

    def absEffAreaIso(self,rho):
        '''Just to make generic code work on GenParticles'''
        return 0

    def relEffAreaIso(self,rho):
        '''Just to make generic code work on GenParticles'''
        return 0
