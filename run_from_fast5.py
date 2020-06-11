#Copyright 2020 Stefano M. Marino   All rights reserved.
#contact <git_hub_username:sm001>
#This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License, or in case any of the later versions.*
#This program is distributed WITHOUT ANY WARRANTY; see the GNU General Public License for more details.*
#A copy of the GNU General Public License is provided in this distribution

import os, sys
print ("command format: python run.py input_data")
try:
    inp=sys.argv[1] # input data in fast5 format
except:
    inp="error_no_input"
    print (" -->>> warning: NO FAST5 INPUT specified...")
    
# qui puoi specificare max_t and num_threads (oppure lo puoi avere in config file

conf=open("configuration.cfg").read().split("\n")

for line in conf:
    if "script_BC=" in line:
        script_BC=line.split("script_BC=")[1]
    if "script_noBC=" in line:
        script_noBC=line.split("script_noBC=")[1]
    if "script_fromfasta=" in line:
        script_fromfasta=line.split("script_fromfasta=")[1]

choice=True
while choice:
    print("""
    1. type 1 to run BARCODE-dependent analysis (input=folder for fast5 data, if BARCODED)
    2. type 2 to run analysis WITHOUT BARCODES (input=folder for fast5 data, if NOT BARCODED)
    3. type 3 to Exit/Quit
    """)
    choice=str(input("What would you like to do? "))


    if choice=="1":
      print("\nchoice 1: run BARCODE-dependent analysis  ")
      os.system("python2 scripts/"+script_BC+" "+inp)
      break
      
    elif choice=="2":
      print("\nchoice 2: run analysis WITHOUT BARCODES")
      os.system("python2 scripts/"+script_noBC+" "+inp)
      break
    elif choice=="3":
      print("\nExit") 
      choice = None
    else:
       print("\n Not a Valid Choice [1,2; or 3 to exit]")
