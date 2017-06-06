import pandas as pd, os

inlocation = os.getcwd()+'\\data\\'
svlocation = os.getcwd()+'\\output\\'

zipfips = pd.read_csv(inlocation +"\\zipcode_fips.csv",header=None,names=['zip','fips'],dtype=str)
zipfips.fips = zipfips.fips.astype(int)
zipfips['fips'] = zipfips['fips'].apply(lambda x: "%06d" % (x,))
zipfips.fips = zipfips.fips.astype(str)

csv_file = pd.read_csv(inlocation +"\\csv\\assignment.csv",date_parser='record_dt')
csv_file = csv_file.fillna('')
csv_file['full_address'] = csv_file['caddress_2'] + ' '+ csv_file['caddress_3'] + ' '+ csv_file['caddress_4']
csv_file.drop(['caddress_1','caddress_2','caddress_3','caddress_4','rf_id','cname','file_id','convey_text',\
               'purge_in','last_update_dt','page_count','reel_no',\
               'frame_no'],axis=1,inplace=True)
csv_file=csv_file[csv_file['full_address']!="  "]
csv_file.full_address=csv_file['full_address'].str.strip()
csv_file['full_address']=csv_file['full_address'].str.extract('.*(\d{5})(-\d{4})?')
csv_file.dropna(inplace=True)
frame = pd.merge(csv_file, zipfips, left_on='full_address',right_on='zip')
frame.sort_values(['fips','record_dt'],inplace=True)
filter = frame['fips'].str.contains('07\d+$')
frame=frame[~filter]
frame.reset_index(inplace=True)
frame.drop(['index'],axis=1,inplace=True)
frame['date'] = pd.to_datetime(frame['record_dt'])
frame['record_dt'] = frame['date'].apply(lambda x:x.strftime('%Y-%m-01'))
frame.drop(['date'],axis=1,inplace=True)
frame = frame.groupby(['fips','record_dt']).size()
frame = pd.DataFrame(frame).reset_index()

for fips in pd.unique(frame['fips'].ravel()):
    df=frame[frame['fips']==fips]
    series_id = 'USPTOISSUED' + fips
    df.reset_index(inplace=True)
    df.drop(['index'], axis=1, inplace=True)
    print(df)
    output = df[['record_dt', 0]]
    output.set_index('record_dt', inplace=True)
    output.columns = [series_id]
    output.to_csv(os.path.join(svlocation, series_id), sep='\t')
