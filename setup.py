import subprocess
#subprocess.run(["python.exe", "-m", "pip", "install", "--upgrade", "pip"]) #upgrading pip to latest version
#installing stuff for geopandas
'''
subprocess.run(["pip", "install", "wheel"]) 
subprocess.run(["pip", "install", "pipwin"])
pipwin=["numpy", "pandas", "shapley", "gdal", "fiona", "pyproj", "six", "rtree", "geopandas"]
for i in pipwin:
    subprocess.run(["pipwin", "install", i])
#installing the rest of the modules
'''
pip = ["requests", "beautifulsoup4", "dask", "dask[dataframe]", "bokeh", "matplotlib", "scipy", "flask", "pyngrok", "logger"]
for i in pip:
    subprocess.run(["pip", "install", i])
