#osc data to pandas df
import pandas as pd
import numpy as np

class OSCData():
    def __init__(self, filename):
        data = pd.read_json(filename)
        self.name = filename.split('.json')
        self.data = data[self.name]
        


    def get_metadata(self):
        pass
        


    def get_photometry(self):

        photometry = pd.read_json(pd.DataFrame(self.data['photometry']).to_json(),orient='column')
        print(photometry.columns)
        photometry.rename(columns={x: x.encode('ascii') for x in photometry.columns})
        photometry = Table.from_pandas(photometry)    
        photometry['Filter'] = photometry['band']
        photometry['Mag'] = photometry['magnitude']
        photometry['MagErr'] = photometry['e_magnitude']
        photometry['MJD'] = photometry['time']
        photometry['Survey'] = photometry['telescope']
        print(photometry)

    def get_spectra(self):
        pass