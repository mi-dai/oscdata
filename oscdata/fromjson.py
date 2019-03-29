print "Download metadata json file from OSC:"
urllib.urlretrieve ("https://raw.githubusercontent.com/astrocatalogs/supernovae/master/output/catalog.json",
                    "/home/mi/Desktop/project-data/metadata/osc.json")

rootfolder = '/home/mi/Desktop/project-data/metadata/'
osc_ia_file = rootfolder+'osc_ia_list.txt' 

if not os.path.exists(osc_ia_file) or not filecmp.cmp(rootfolder+'osc.json',rootfolder+'osc.json.prev') or force_oscsearch:

    filename = rootfolder+'osc.json'
    f = open(filename,'r')
    data=json.load(f)
    f.close()

    maxlen_alias = 0
    for d in data:
        if 'claimedtype' in d.keys() and d['claimedtype'][0]['value'][0:2]=='Ia':
            if 'alias' in d.keys() and len(d['alias']) > maxlen_alias:
                maxlen_alias = len(d['alias'])
    print 'maxlen_alias=', maxlen_alias

    maxlen_redshift = 0
    for d in data:
        if 'claimedtype' in d.keys() and d['claimedtype'][0]['value'][0:2]=='Ia':
            if 'redshift' in d.keys() and len(d['redshift']) > maxlen_redshift:
                maxlen_redshift = len(d['redshift'])
    #             print maxlen_redshift,d['name'],d['redshift']
    print 'maxlen_redshift=',maxlen_redshift

    namelist1 = ['Alias'+str(i) for i in range(1,maxlen_alias+1)]
    typelist1 = ['S30']*maxlen_alias
    print namelist1
    print typelist1
    t_host = Table(names=['Name', 'Type', 'Host','z','zkind','ra','dec']+namelist1, 
                   dtype=['S30', 'S20', 'S30','f8','S30','S30','S30']+typelist1)
    print t_host

    maxlen=maxlen_alias
    for d in data:
        if 'claimedtype' in d.keys() and d['claimedtype'][0]['value'][0:2]=='Ia':
            if 'alias' in d.keys():
                alias = list()
                for i in range(0,len(d['alias'])):
                    alias.append(d['alias'][i]['value'].encode('ascii','ignore'))
                for i in range(len(d['alias']),maxlen_alias):
                    alias.append('N/A')
    #             print alias
    #         print d['name']
            if 'host' in d.keys():
                host = d['host'][0]['value']
            else:
                host = 'N/A'
            if 'redshift' in d.keys():
                z = d['redshift'][0]['value']
                if 'kind' in d['redshift'][0].keys():
                    if isinstance(d['redshift'][0]['kind'],list):                        
                        zkind = '-'.join(d['redshift'][0]['kind'])
                    else:
                        zkind = d['redshift'][0]['kind']
#                     print zkind
                else:
                    zkind = 'N/A'
            else:
                z = -99.
            if 'ra' in d.keys():
                ra = d['ra'][0]['value']
            else:
                ra = -99.
            if 'dec' in d.keys():
                dec = d['dec'][0]['value']
            else:
                dec = -99.

            t_host.add_row([d['name'].encode('ascii','ignore'),d['claimedtype'][0]['value'],host,z,zkind,ra,dec]+alias)
    
    print "Writing osc sninfo to: ", osc_ia_file
    t_host.write(osc_ia_file,format='ascii',overwrite=True)

    print "Copy 'osc.json' to 'osc.json.prev'."
    shutil.copy2(rootfolder+'osc.json',rootfolder+'osc.json.prev')
else:
    print "'osc.json' does not change, reload t_host from old file: ", osc_ia_file
    t_host = Table.read(osc_ia_file,format='ascii')





### photometry
photometry = pd.read_json(pd.DataFrame(data['photometry']).to_json(),orient='column')
print(photometry.columns)
photometry.rename(columns={x: x.encode('ascii') for x in photometry.columns})
photometry = Table.from_pandas(photometry)    
photometry['Filter'] = photometry['band']
photometry['Mag'] = photometry['magnitude']
photometry['MagErr'] = photometry['e_magnitude']
photometry['MJD'] = photometry['time']
photometry['Survey'] = photometry['telescope']



###spectra
spectra = pd.read_json(pd.DataFrame(data['spectra']).to_json(),orient='column')