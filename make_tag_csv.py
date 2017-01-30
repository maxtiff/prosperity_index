import pandas as pd
def make_tags(input_file,output_file):

	tags = pd.read_table(input_file,sep='\t',header=None)
	tags = pd.melt(tags,id_vars=0,value_name='tag')
	tags.drop(['variable'],axis=1,inplace=True)
	tags.columns=(['series_id','tag'])
	tags.to_csv(output_file,index=False)

def main():
	
	make_tags('tags.txt','clean_tags.txt')

if __name__=='__main__':
	main()