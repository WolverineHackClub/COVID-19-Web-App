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
pip = ["pandas","requests", "beautifulsoup4",  "matplotlib", "scipy", "flask", "logger"]
for i in pip:
    subprocess.run(["pip", "install", i])
#"dask", "dask[dataframe]", "bokeh", "pyngrok"