#osc data to pandas df
import pandas as pd

class OSCData():
    def __init__(self, filename, name):
        data = pd.read_json(filename)
        self.name = name
        self.data = data[self.name]
        

    def get_metadata(self):
        keys = self.data.keys()
        metakeys = ['redshift','ra','dec','host']
        for key in metakeys:
            data_k = pd.read_json(pd.DataFrame(self.data[key]).to_json(),orient='column')
            data_k['source'] = data_k['source'].apply(seperate_values)
            data_k['Name'] = self.name
            s = data_k['source'].apply(pd.Series).stack().reset_index(level=-1,drop=True)
            s.name = 'source2'
            data_k = data_k.merge(s.to_frame(),left_index=True,right_index=True)
            print(data_k)
            

    def get_photometry(self):
        print(self.data.keys())
        photometry = pd.read_json(pd.DataFrame(self.data['photometry']).to_json(),orient='column')
        photometry.rename(columns={x: x.encode('ascii') for x in photometry.columns})
        photometry = Table.from_pandas(photometry)    
        self.photometry['Filter'] = photometry['band']
        self.photometry['Mag'] = photometry['magnitude']
        self.photometry['MagErr'] = photometry['e_magnitude']
        self.photometry['MJD'] = photometry['time']
        self.photometry['Survey'] = photometry['telescope']
        self.photometry['Name'] = name
        #comment



    def get_spectra(self):
        pass



def seperate_values(value):
    value = str(value)
    return(value.split(','))
