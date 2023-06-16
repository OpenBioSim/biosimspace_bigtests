import os
import re
import pandas as pd

pattern = "Systems/(.*?)/rep"

storage = []
for subdir, dirs, files in os.walk("./Systems"):
	for file in files:
		print(file)
		if file.endswith("mineq.o"):
			pert = re.search(pattern,subdir).group(1)
			rep = subdir[-4:]
			vacsolv = file.split("_")[0]
			count = 0
			with open(os.path.join(subdir,file),'r') as f:
				lines=f.readlines()
				for line in lines:
					if "Success" in line:
						count+=1
			storage.append([pert,rep,vacsolv,count])

s_t = [list(i) for i in zip(*storage)]
df = pd.DataFrame(storage,columns=["Perturbation","Replica","system","passed"])
df.to_csv("report_MinEq.csv")
