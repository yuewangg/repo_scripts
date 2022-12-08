import os
for filename in os.listdir('/mnt/e/new2/'): 
	newname = filename.replace('P2', '')  #把 P2 替换成空白
	os.rename('/mnt/e/new2/'+filename, '/mnt/e/new2/'+newname)
