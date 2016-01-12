import os 
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

def get_result_path():
    """get location of results 
    """
    return os.path.join(os.path.dirname(__file__), 'history_folder')

def plot_zeta(his_file_path,his_name,testcase,colormin,colormax):
    print "----------------------------------------"
#    print "Post processing data for",datafile.lowercase(),"datafile" 
    print "Post processing data for",testcase,"case is",his_name
    print "----------------------------------------"
    datafile=os.path.join(his_file_path,his_name)
    print datafile
    ncfile = Dataset(datafile,'r')
    zeta=ncfile.variables['zeta'][:]
    ntime,nx,ny = zeta.shape
    print ntime,nx,ny   
    x_rho=ncfile.variables['x_rho'][:]#*10
    y_rho=ncfile.variables['y_rho'][:]#*1000
    ocean_time = ncfile.variables['ocean_time'][:]
    fig = plt.figure()
    ax = fig.gca()
    ax.set_aspect('equal')    
# Plot surface zeta
    cmap=plt.cm.RdYlBu
    cmap.set_bad(color = [0.75,0.75,0.75], alpha = 1.)
    plt.pcolormesh(x_rho,y_rho,zeta[ntime-1,:,:],cmap=cmap,edgecolors = 'None',vmin=colormin,vmax=colormax)
    cb = plt.colorbar(label='Water level')
    cb.ax.tick_params(labelsize=8)
    figtitle = 'Water level for '+testcase.upper()+' case'
    plt.title(figtitle,fontsize=10)
    plt.xlabel('Longitudnal direction in kms',fontsize=12)
    plt.ylabel('Lateral direction in kms',fontsize=12)
    figname=testcase+'_'+'regress'+'.png'    
    plt.savefig(figname,dpi=300,bbox_inches='tight')
    plt.close(fig)

#  Now move all the files with these extensions or prefixes
#    for filename in os.listdir('.'):
#        if filename.endswith(('.nc','.mat')):
#            shutil.move(filename,project_path)
    for figname in os.listdir('.'):
        shutil.move(figname,his_file_path)
