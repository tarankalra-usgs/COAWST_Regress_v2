RUNNING THE REGRESSION MODULE

* 1. Execute by typing "python coawst_regress_run.py"

--------------------------------------------------------------------
DESCRIPTION OF THE PYTHON FILES

Inside the folder there is a sub-folder called coawst_regress_baseline
it has python files which are

* 1. util.py --> fetches the source code from subversion client,
edits jobscript, bashfile, copies output

* 2. main.py -->
calls each test case from its own separate ".py" file

* 3. WRF_Config_file --> Important folder that copies files to COAWST
distribution for WRF compilation

* 4. All the other .py files are for each case. One can comment some
cases or have all of them included by commenting/uncommenting them in
main.py.

* 5.The number of processors for each run can be changed inside each project's file. Also the time
of waiting after the execution of each case is hardwired in the command
"time.sleep()" and this time is in seconds. So, as we increase the processors for a case
we can decrease the time required to run the job.

--------------------------------------------------------------------

# COAWST_Regress_v2
