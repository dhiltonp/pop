'''
Convenience wrappers to make using the conf system as easy and seamless as possible
'''


def integrate(hub, imports, override=None):
    '''
    Load the conf sub and run the integrate sequence.
    '''
    hub.tools.sub.add('conf', pypath='pop.mods.conf')
    hub.conf.integrate.load(imports, override)