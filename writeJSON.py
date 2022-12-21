import json
import os
import uproot
import sys
import argparse

def main(process_selection, outfile_name):
	
	# these files need to be deleted from AGC/nanoAOD eventually
	exclude = ['{line}.root',
		   'cmsopendata2015_ttbar_19980_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_50000_0008.root', 
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_10000_0008.root', 
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_10000_0009.root', 
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_10000_0010.root', 
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_10000_0011.root', 
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_10000_0012.root', 
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_10000_0013.root',  
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_80000_0007.root', 
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_80000_0008.root',
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_80000_0009.root', 
		   'cmsopendata2015_ttbar_19983_PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1_80000_0010.root']
	
	if process_selection=="agc":
		processes = ["ttbar", "single_top_s_chan", "single_top_t_chan","single_top_tW", "wjets"]
	if process_selection=="cmsworkshop":
		processes = ["data", "ttbar", "single_top_t_chan", "single_atop_t_chan", "single_top_tW", "wjets"]
	if process_selection=="all":
		processes = ["data", "ttbar", "single_top_s_chan", "single_atop_t_chan", "single_top_t_chan", "single_top_tW", "wjets"]
	
	variations_data = ["nominal"]
	variations_ttbar = ["nominal", "scaledown", "scaleup", "ME_var", "PS_var"]
	variations_single_top_s_chan = ["nominal"]
	variations_single_top_t_chan = ["nominal"]
	variations_single_atop_t_chan = ["nominal"]
	variations_single_top_tW = ["nominal", "scaledown", "scaleup", "DS"]
	variations_wjets = ["nominal"]

	if process_selection=="agc":
		variations_dict = {"ttbar": variations_ttbar,
	                    	   "single_top_s_chan": variations_single_top_s_chan,
			   	   "single_top_t_chan": variations_single_top_t_chan,
	                    	   "single_top_tW": variations_single_top_tW,
	                    	   "wjets": variations_wjets}
	if process_selection=="cmsworkshop":
		variations_dict = {"data": variations_data,
				   "ttbar": variations_ttbar,
                                   "single_top_t_chan": variations_single_top_t_chan,
                                   "single_atop_t_chan": variations_single_atop_t_chan,
                                   "single_top_tW": variations_single_top_tW,
                                   "wjets": variations_wjets}
	if process_selection=="all":
		variations_dict = {"data": variations_data,
                                   "ttbar": variations_ttbar,
				   "single_top_s_chan": variations_single_top_s_chan,
                                   "single_top_t_chan": variations_single_top_t_chan,
                                   "single_atop_t_chan": variations_single_atop_t_chan,
                                   "single_top_tW": variations_single_top_tW,
                                   "wjets": variations_wjets}

	pathmapping_data = {"nominal": ["store/user/AGC/nanoAOD/SingleElectron/","store/user/AGC/nanoAOD/SingleMuon/"]}
	pathmapping_ttbar = {"nominal": ["store/user/AGC/nanoAOD/TT_TuneCUETP8M1_13TeV-powheg-pythia8/"],
	                     "scaledown": ["store/user/AGC/nanoAOD/TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8/"],
	                     "scaleup": ["store/user/AGC/nanoAOD/TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8/"],
	                     "ME_var": ["store/user/AGC/nanoAOD/TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/"],
	                     "PS_var": ["store/user/AGC/nanoAOD/TT_TuneEE5C_13TeV-powheg-herwigpp/"]}
	pathmapping_single_top_s_chan = {"nominal": ["store/user/AGC/nanoAOD/ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8/"]}
	if process_selection=="agc":
		pathmapping_single_top_t_chan = {"nominal": ["store/user/AGC/nanoAOD/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/","store/user/AGC/nanoAOD/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/"]}
	else: pathmapping_single_top_t_chan = {"nominal": ["store/user/AGC/nanoAOD/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/"]}
	pathmapping_single_atop_t_chan = {"nominal": ["store/user/AGC/nanoAOD/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/"]}
	pathmapping_single_top_tW = {"nominal": ["store/user/AGC/nanoAOD/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1","store/user/AGC/nanoAOD/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/"],
	                             "scaledown": ["store/user/AGC/nanoAOD/ST_tW_antitop_5f_scaledown_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/","store/user/AGC/nanoAOD/ST_tW_top_5f_scaledown_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/"],
	                             "scaleup": ["store/user/AGC/nanoAOD/ST_tW_antitop_5f_scaleup_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/","store/user/AGC/nanoAOD/ST_tW_top_5f_scaleup_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/"],
	                             "DS": ["store/user/AGC/nanoAOD/ST_tW_antitop_5f_DS_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/","store/user/AGC/nanoAOD/ST_tW_top_5f_DS_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/"]}
	pathmapping_wjets = {"nominal":["store/user/AGC/nanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/"]}
	
	if process_selection=="agc":
		pathmapping_dict = {"ttbar": pathmapping_ttbar,
	        	            "single_top_s_chan": pathmapping_single_top_s_chan,
	                	    "single_top_t_chan": pathmapping_single_top_t_chan,
				    "single_top_tW": pathmapping_single_top_tW,
	                	    "wjets": pathmapping_wjets}
	if process_selection=="cmsworkshop":
		pathmapping_dict = {"data": pathmapping_data,
				    "ttbar": pathmapping_ttbar,
                                    "single_top_t_chan": pathmapping_single_top_t_chan,
                                    "single_atop_t_chan": pathmapping_single_atop_t_chan,
                                    "single_top_tW": pathmapping_single_top_tW,
                                    "wjets": pathmapping_wjets}
	if process_selection=="all":
		pathmapping_dict = {"data": pathmapping_data,
                                    "ttbar": pathmapping_ttbar,
				    "single_top_s_chan": pathmapping_single_top_s_chan,
                                    "single_top_t_chan": pathmapping_single_top_t_chan,
                                    "single_atop_t_chan": pathmapping_single_atop_t_chan,
                                    "single_top_tW": pathmapping_single_top_tW,
                                    "wjets": pathmapping_wjets}
	
	xrootd_prefix = "https://xrootd-local.unl.edu:1094//"
	local_prefix = "/mnt/t2ceph/cms/"
	
	json_dict = {}
	
	for process in processes:
		
		print("Process = ", process)
		processdict_temp = {}
	    
		for variation in variations_dict[process]:
	        
			print("	Variation = ", variation)
			variationdict_temp = {}
			variationdict_temp["nevts_total"] = 0
	        
			filelist = []
	
			filecounter = 0
			for path in pathmapping_dict[process][variation]:
			
				print("		Path = ", path)
	
				directory = local_prefix + path
				if os.path.isdir(directory):
					for filename in sorted(os.listdir(directory)):
						if not os.path.isdir(os.path.join(directory,filename)):
							f = uproot.open(os.path.join(directory,filename))
						
							if len(f.keys())>0 and filename not in exclude:
								print("			FileCount = ", filecounter)
								num_entries = f["Events"].num_entries
								filelist.append({"path": os.path.join(xrootd_prefix + path, filename),
										 "nevts": num_entries})
								filecounter+=1
								variationdict_temp["nevts_total"] = variationdict_temp["nevts_total"] + num_entries
		
			variationdict_temp["files"] = filelist
		
			processdict_temp[variation] = variationdict_temp
	
		json_dict[process] = processdict_temp
	
	json_file = open(outfile_name, "w")
	json_file.write(json.dumps(json_dict, indent=4))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="This program writes the filepaths of the 2015 CMS open data nanoAODs to a json file, assuming that the program is being run from T3 UNL.")
	parser.add_argument("-p", "--process_selection", help="agc: [ttbar, single_top_s_chan, single_top_t_chan, single_top_tW, wjets]; cmsworkshop: [data, ttbar, single_top_t_chan, single_atop_t_chan, single_top_tW, wjets], all: [data, ttbar, single_top_s_chan, single_top_t_chan, single_atop_t_chan, single_top_tW, wjets]")
	parser.add_argument("-o", "--outfile_path", help="output json file name")

	args = parser.parse_args()

	main(args.process_selection, args.outfile_path)
