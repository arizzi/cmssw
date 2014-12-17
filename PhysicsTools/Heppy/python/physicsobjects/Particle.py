class Particle(object):
    def particlePrint(self) :
        tmp = '{className} : {pdgId:>3}, pt = {pt:5.1f}, eta = {eta:5.2f}, phi = {phi:5.2f}, mass = {mass:5.2f}'
        return tmp.format( className = self.__class__.__name__,
                           pdgId = self.pdgId(),
                           pt = self.pt(),
                           eta = self.eta(),
                           phi = self.phi(),
                           mass = self.mass() )
    

    def __str__(self):
        return self.particlePrint()        
