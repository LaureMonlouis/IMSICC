import os
for root, dirs, files in os.walk("../Data/raw_data", topdown=False):
   for name in files:
      print(os.path.join(root, name))
      

