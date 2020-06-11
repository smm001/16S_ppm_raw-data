#Copyright 2020 Stefano M. Marino   All rights reserved.
#contact <git_hub_username:sm001>
#This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License, or in case any of the later versions.*
#This program is distributed WITHOUT ANY WARRANTY; see the GNU General Public License for more details.*
#A copy of the GNU General Public License is provided in this distribution

import re, os,sys, glob

conf=open("configuration.cfg").read().split("\n")

for line in conf:
    if "num_threads=" in line:
        num_threads=int(line.split("num_threads=")[1])
    elif "guppy_dir=" in line:
        guppy_dir=(line.split("guppy_dir=")[1])

    elif "max_t=" in line: 
        max_t=int(line.split("max_t=")[1])
    elif "db=" in line:
        db=(line.split("db=")[1])
    elif "Nanofilt=" in line:
        Nanofilt=int(line.split("Nanofilt=")[1])
    elif "Q_filt=" in line:
        Q_filt=str(line.split("Q_filt=")[1])
    elif "L_filt=" in line:
        L_filt=str(line.split("L_filt=")[1])
    elif "porechop=" in line:
        porechop=int(line.split("porechop=")[1])
    elif "blastn=" in line:
        blastn=(line.split("blastn=")[1])
    elif "porechop_runner=" in line:
        porechop_runner=(line.split("porechop_runner=")[1])

    elif "Nanofilt_runner=" in line:
        Nanofilt_runner=(line.split("Nanofilt_runner=")[1])
    elif "Filtlong_runner=" in line:
        Filtlong_runner=(line.split("Filtlong_runner=")[1])
    elif "guppy_fast_mode=" in line:
        guppy_fast_mode=str(line.split("guppy_fast_mode=")[1])

if guppy_fast_mode == "ON":
    guppy_cfg_mode="dna_r9.4.1_450bps_fast.cfg"# guppy fast
elif guppy_fast_mode == "OFF":  
    guppy_cfg_mode="dna_r9.4.1_450bps_hac.cfg"  # guppy high accuracy (significantly slower)
else:
    guppy_cfg_mode="dna_r9.4.1_450bps_fast.cfg"
    
inp=sys.argv[1]  

if inp[-1]=="/":
    inp=inp[:-1]
    if "/" in inp:
        outname=inp.split("/")[-1]+'_guppy_outdir'
    else:
        outname=inp+'_guppy_outdir'
else:
    outname=inp.split("/")[-1]+'_guppy_outdir'


out=outname
root_name=inp.split("/")[-1]
preben=inp.split("/")[-1].split(".")[0] # Preben 11

if os.path.isdir(out):
    os.system("rm -r "+out+"/*")
else:
    os.makedirs(out)

os.system(guppy_dir+"/bin/guppy_basecaller --recursive --input_path "+str(inp)+" --save_path "+str(out)+" --config "+guppy_dir+"/data/"+guppy_cfg_mode)

ass= glob.glob(out+"/*.fastq")
os.system("cat "+out+"/*.fastq > guppy_all.fastq")
bc="guppy_all.fastq"
os.system("mv "+bc+" "+root_name+".fastq")
bc=root_name+".fastq"
      
if Nanofilt ==1:
       if os.path.exists(Nanofilt_runner): 
        os.system("cat "+bc+" | "+Nanofilt_runner+" -q "+Q_filt+" -l "+L_filt+" > "+bc+"_qc")
        os.system("mv "+bc+"_qc "+bc)
       else:
          vQ=1-(10**(-(float(Q_filt)/10)))
          print "Filtlong, --min_mean_q = ",vQ
          os.system(Filtlong_runner+" "+bc+" --min_mean_q "+str(vQ)+" --min_length "+L_filt+" > "+bc+"_qc")
          os.system("mv "+bc+"_qc "+bc)
ffasta=bc.split(".fastq")[0]+".fasta"
#os.system("seqtk seq -a "+bc+" > "+ffasta)
os.system("sed -n '1~4s/^@/>/p;2~4p' "+bc+" > "+ffasta) 

#os.system("mv "+bc+" NanoFilt.log "+ffasta+" "+out)


              



    
  
    
    
    


