import util_plot
import trench_plot
#import upwelling_plot
#
#    history_file_path = os.path.join(util_plot.get_result_path(), testcase)
#    print "----------------------------------------------"
#    print " The history files are located in:", history_file_path
def plot_testcase():
    """Create everything needed to run a testcase

    Takes testcase name and creates compiled exe and new bash script
    """
    print "----------------------------------------------"
    """ This is the order in which test cases run """

    trench_plot.plot_trench() 
#    upwelling_plot.plot_upwelling(code_path) 
#    estuary_plot.plot_estuary_test2(code_path)
#    wetdry_plot.plot_wetdry(code_path)
#    ducknc_plot.plot_ducknc(code_path) 
#    speclight_plot.plot_speclight(code_path) 
#    sedbed_toy_plot.plot_sedbed_toy(code_path) 
#    sed_floc_toy_plot.plot_sed_floc_toy(code_path) 
#    ripcurrent_plot.plot_ripcurrent(code_path) 
#    inlettest_plot.plot_inlet(code_path) 
#    joetc_plot.plot_joetc(code_path) 
##    sandy_plot.plot_sandy(code_path) 
#    shoreface_plot.plot_shoreface(code_path)
