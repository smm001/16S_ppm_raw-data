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

    elif "max_t=" in line: # set in configuration.cfg to 0, for unrestricted blast search
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
    elif "max_num_fasta=" in line:
        max_num_fasta=int((line.split("max_num_fasta=")[1]))
    elif "min_num_fasta=" in line:
        min_num_fasta=int((line.split("min_num_fasta=")[1]))
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
        outname=inp.split("/")[-1]+'_16Sout'
    else:
        outname=inp+'_16Sout'
else:
    outname=inp.split("/")[-1]+'_16Sout'
out=outname
root_name=inp.split("/")[-1]
#print "inp =",inp
#print "out=",out
#raw_input("waiting..")

if os.path.isdir(out):
    #os.system("cp -r "+out+" "+out+"_bu")  
    os.system("rm -r "+out+"/*")
    
else:
    os.makedirs(out)

os.system(guppy_dir+"/bin/guppy_basecaller --recursive --input_path "+str(inp)+" --save_path "+str(out)+" --config "+guppy_dir+"/data/"+guppy_cfg_mode)
os.system(guppy_dir+"/bin/guppy_barcoder --input_path "+str(out)+" --save_path "+str(out)+" --config "+guppy_dir+"/data/barcoding/configuration.cfg")

ass2=glob.glob(out+"/barcode*/")
ass3=[]
for bci in ass2:
    if len(glob.glob(bci+"*.fastq")) > 0:
        bci2=re.findall("/barcode.*/",bci)[0].replace("/","").replace(" ","")
        os.system("cat "+bci+"*.fastq > "+bci+bci2+"_all.fastq")
        ass3.append(bci+bci2+"_all.fastq")

for bc in ass3:
    bc_num=re.findall("/barcode.*/",bc)[0]
    BCx=bc_num.replace("/","").replace(" ","")
    if porechop ==1:
       vp=os.system("python3.4 --version > p34version_temp")
       svp=os.path.getsize("p34version_temp")
       if svp > 0:
             print "--> porecop: using python 3.4 .." ## edit this for any specific version (a working one, however, depends also on g++ version; https://github.com/rrwick/Porechop)
             os.system("python3.4 "+porechop_runner+" -i "+bc+" -o "+bc+"_t --threads="+str(num_threads))
             os.system("mv "+bc+"_t "+bc)
       else:
             os.system("python3 "+porechop_runner+" -i "+bc+" -o "+bc+"_t --threads="+str(num_threads))
             os.system("mv "+bc+"_t "+bc)
       os.remove("p34version_temp")

    if Nanofilt ==1:
       if os.path.exists(Nanofilt_runner):
        os.system("cat "+bc+" | "+Nanofilt_runner+" -q "+Q_filt+" -l "+L_filt+" > "+bc+"_qc")
        os.system("mv "+bc+"_qc "+bc)
       else:
          vQ=1-(10**(-(float(Q_filt)/10)))
          print "Filtlong, --min_mean_q = ",vQ
          os.system(Filtlong_runner+" "+bc+" --min_mean_q "+str(vQ)+" --min_length "+L_filt+" > "+bc+"_qc")
          os.system("mv "+bc+"_qc "+bc)
    
    
    os.system("sed -n '1~4s/^@/>/p;2~4p' "+bc+" > "+bc.split(".fastq")[0]+".fasta")
    
    
    os.system("cp "+bc.split(".fastq")[0]+".fasta "+BCx+".fasta")
    fasta_input=BCx+".fasta"
    
    t_n=len(open(fasta_input).read().split(">")) - 1

    if t_n > max_num_fasta:
        t_n=max_num_fasta
    else:
        t_n=t_n

    if t_n > min_num_fasta: # min number of seqs, set in configuration file, to parse the barcoded ( -- if not for testing purposes, it could be set to 100)
        
        try:
            os.system("python2 scripts/take_random_subset_fasta.py "+fasta_input + " "+str(t_n)) 
        except:
            print "could not take random fasta subset "+fasta_input

        fasta_input_short="analyzed_seqs_"+fasta_input
        ### below, clean up of temporary files, and move output files to output folder
        os.remove(fasta_input)
        os.system("cp "+fasta_input_short+" "+outname)
        os.system("mv "+fasta_input_short+" "+fasta_input)
    
        os.system("python2 scripts/fromfasta_16Spipe.py "+fasta_input+" "+db)  
        os.system("cp -r "+BCx+"_results_fromfasta "+outname)
        os.system("rm -r "+BCx+"_results_fromfasta")
    os.system("rm "+fasta_input)

os.system("rm "+out+"/*.fastq")
print "data saved in: ",outname
   

       


          

    
    
  
    
    
    


