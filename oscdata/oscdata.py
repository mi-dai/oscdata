#osc data to pandas df
import pandas as pd

class OSCData():
    def __init__(self, filename):
        data = pd.read_json(filename)
        self.name = filename.split('.json')[0]
        self.data = data[self.name]
        


    def get_metadata(self):
        pass


    def get_photometry(self):
        print self.data.keys()
        photometry = pd.read_json(pd.DataFrame(self.data['photometry']).to_json(),orient='column')
        photometry.rename(columns={x: x.encode('ascii') for x in photometry.columns})
        photometry = Table.from_pandas(photometry)    
        self.photometry['Filter'] = photometry['band']
        self.photometry['Mag'] = photometry['magnitude']
        self.photometry['MagErr'] = photometry['e_magnitude']
        self.photometry['MJD'] = photometry['time']
        self.photometry['Survey'] = photometry['telescope']
        self.photometry['Name'] = name



    def get_spectra(self):
        pass