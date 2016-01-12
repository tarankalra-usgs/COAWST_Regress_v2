import util_plot
import os
import sys 

def plot_upwelling(history_filepath):
    testcase='upwelling'
    his_name='ocean_upwelling_his.nc'
# In future may be have user input a text file
# of these parameters and if file does not exist
# use these values by default 
#    if os.path.isfile(his_name):
# Indices of point where zeta needs to be plotted
    colormin=-0.01
    colormax=0.01
    util_plot.plot_zeta(testcase,his_name,colormin,colormax)
