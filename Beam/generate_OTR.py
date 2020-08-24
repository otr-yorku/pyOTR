import concurrent.futures
import numpy as np
import Config as cf
import Beam
import Geometry
from PrepareData import PrepareData

@cf.timer
def SimulateBeam(X, V, system):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(system.TraceRays, X, V)
        for i, result in enumerate(results):
            if i % 100 == 0:
                cf.logger.debug(f'Running data piece: {i}')
            x, v = result
            assert x.shape == v.shape
            if i == 0:
                Xf = np.array(x)
                Vf = np.array(v)
            else:
                Xf = np.concatenate((Xf, x), axis=0)
                Vf = np.concatenate((Vf, v), axis=0)

    Xf = np.array(Xf)
    Vf = np.array(Vf)
    return Xf, Vf

if __name__ == '__main__':

    cf.GetTime()
    # Get details about the beam:
    beam = Beam.Beam()
    if(cf.source == 'protons'):
        X, V = beam.GenerateBeam()
    elif(cf.source == 'filament'):
        X, V = beam.GenerateBackgroundLight()
    else:
        print('Not a valid source')
    
    #Save initial distribution
    if cf.save:
        #np.save(f'{cf.name}_protonsX', X)
        #np.save(f'{cf.name}_protonsV', V)
        np.save(f'{cf.name}_bgX', X)
        np.save(f'{cf.name}_bgV', V)

    if cf.chunck > 0:
        X, V  = PrepareData(X, V, chunck=cf.chunck)

    # Get the Foil Geometry: 
    system = Geometry.GetGeometry()
    # Run simulation:
    X, V = SimulateBeam(X, V, system)
    if cf.save:
        np.save(f'{cf.name}_X', X)
        np.save(f'{cf.name}_V', V)
    
    cf.GetTime(start=False)


