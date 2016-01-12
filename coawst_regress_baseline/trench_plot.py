import util_plot
import os
import sys 

def plot_trench():
    testcase='trench'
    his_name='ocean_trench_his.nc'
#  one history file would be in an old code path 
#  one history file would be in a new code path 
    his_file_path=os.path.join(util_plot.get_result_path())
    print his_file_path
    colormin=-0.01
    colormax=0.01
    util_plot.plot_zeta(his_file_path,his_name,testcase,colormin,colormax)
