import pandas as pd
import requests
from datetime import date
from lxml import html

def text(elt):
    return elt.text_content().replace(u'\xa0', u' ')

base = 'https://www5.fdic.gov/'
hsob = 'hsob/HSOBSummaryRpt.asp'
bg_year = 'BegYear='
cr_year = str(date.today().year)
end_year = 'EndYear='
st_year = '1934'
state = 'State=1'
header = 'Header=1'
full = base + hsob + '?' + bg_year + cr_year + '&' + end_year + st_year + '&' + state + '&' + header
user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; Active Content Browser)'
headers = { 'User-Agent' : user_agent }
req = requests.get(full, headers=headers)

root = html.fromstring(req.content)

for table in root.xpath('/html/body/table[2]'):
	header = [text(th) for th in table.xpath('//th')]
	header[4:7]=[]
    print(header)
	df = pd.DataFrame(columns=header)
	dl = [text(td) for td in table.xpath('//td')]
	dl[0:3]=[]
	dl.pop()
    print(dl)
	col = 0
	row=[]
	for cell in dl:
		row.append(cell)
		col += 1
		if col%23 == 0:
			row = pd.DataFrame(data=[row],columns=header)
			if(row.iloc[0][0]=='Total '):
				continue
			else:
				df = df.append(row)
				col = 0
				row = []
	df = df.iloc[::-1]
	df.set_index('Year',inplace=True)
	df.index.rename('date',inplace=True)
	df.index = pd.to_datetime(df.index)

	for column in df:
		series = pd.DataFrame(data=df[column])
		series_id = series.columns[0]
		series_id = series_id.replace('*','')
		series_id = series_id.replace('/','')
		series.to_csv(series_id,index=True,sep='\t')

