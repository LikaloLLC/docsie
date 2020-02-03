import os
import sys
cwd = os.getcwd()

from os import listdir
from os.path import isfile, join



if __name__=='__main__':
  site_path = sys.argv[1]
  folder = cwd + '/src/'
  flows = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(cwd + '/src/')] for val in
           sublist]


  site_map = []
  for f in flows:
    if 'index.html' in f:
      site_map.append(site_path+'/'+f.replace(cwd+'/src/', '').replace('index.html',''))

  with open('sitemap/sitemap.txt', 'w') as f:
    for item in site_map:
      f.write("%s\n" % item)
