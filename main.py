from match_salami_files import *
import pandas as pd
pair_list_filename = "./salami_youtube_pairings.csv"
df = load_matchlist()
md = load_song_info()
cod_ids = list((md.salami_id[md.source=="Codaich"]).astype(int))
iso_ids = list((md.salami_id[md.source=="Isophonics"]).astype(int))
cod_ids.sort()
iso_ids.sort()

# Initial search, including youtube queries to build candidate lists:
# for salami_id in iso_ids:
# 	print salami_id
# 	try:
# 		output_list = multiple_searches_for_song(salami_id)
# 		define_candidates_from_searches(salami_id, output_list)
# 		prioritize_candidates(salami_id, no_longs=True, must_be_longer=True)
# 		# If match not found on first pass, we can relax constraint and set no_longs=False to get more options.
# 		# Also, focus for now only on things that are at least as long as the SALAMI file.
# 		suggest_previous_find(salami_id) # (if it exists)
# 		process_candidates(salami_id, max_tries_per_video=3, max_potential=2, sleep=60)
# 		purge_rejected_audio(salami_id)
# 	except (KeyboardInterrupt):
# 		raise
# 	except:
# 		print "Error processing salami_id {0}".format(salami_id)

# Secondary searching, focusing on non-matched audio:
matchlist = pd.read_csv(pair_list_filename)
remaining_ids = set(cod_ids+iso_ids) - set(matchlist.salami_id) 
remaining_ids = list(remaining_ids)
remaining_ids.sort()
for salami_id in remaining_ids[54:]:  # FRom 277 onwards
	print(salami_id)
	try:
		prioritize_candidates(salami_id, no_longs=True, must_be_longer=True)
		# If match not found on first pass, we can relax constraint and set no_longs=False to get more options.
		# Also, focus for now only on things that are at least as long as the SALAMI file.
		process_candidates(salami_id, max_tries_per_video=12, max_potential=0, sleep=0)
		purge_rejected_audio(salami_id)
		# Prioritize again after doing that, so that the diff isn't screwed up:
		prioritize_candidates(salami_id, no_longs=True, must_be_longer=True)
	except (KeyboardInterrupt):
		raise
	except:
		print("Error processing salami_id {0}".format(salami_id))


matchlist = pd.DataFrame(columns=["salami_id","salami_length","youtube_id","youtube_length","coverage","coverage_percent"])
for salami_id in (cod_ids + iso_ids):
	# Record best answer so far [might be nothing]
	candidates = load_candidate_list(salami_id)
	# Read candidate report
	next_ind = len(matchlist)
	salami_length = df.salami_length[df.salami_id==salami_id].values[0]
	if "match" in candidates.decision.values:
		row = candidates[candidates.decision=="match"].iloc[0,:]
		# Select best candidate from report [could be a "potential", not "match".]
		matchlist.loc[next_ind,"salami_id"] = salami_id
		matchlist.loc[next_ind,"salami_length"] = salami_length
		matchlist.loc[next_ind,"youtube_id"] = row.youtube_id
		matchlist.loc[next_ind,"youtube_length"] = row.duration
		matchlist.loc[next_ind,"coverage"] = row.matching_length
		matchlist.loc[next_ind,"coverage_percent"] = matchlist.loc[next_ind,"coverage"] / salami_length
		matchlist.loc[next_ind,"onset_in_youtube"] = row.onset_in_youtube
		matchlist.loc[next_ind,"onset_in_salami"] = row.onset_in_salami
	elif "potential" in candidates.decision.values:
		tmp_df = candidates[candidates.decision=="potential"].sort_values("matching_length",ascending=False)
		row = tmp_df.iloc[0,:]
		matchlist.loc[next_ind,"salami_id"] = salami_id
		matchlist.loc[next_ind,"salami_length"] = salami_length
		matchlist.loc[next_ind,"youtube_id"] = row.youtube_id
		matchlist.loc[next_ind,"youtube_length"] = row.duration
		matchlist.loc[next_ind,"coverage"] = row.matching_length
		matchlist.loc[next_ind,"coverage_percent"] = matchlist.loc[next_ind,"coverage"] / salami_length
		matchlist.loc[next_ind,"onset_in_youtube"] = row.onset_in_youtube
		matchlist.loc[next_ind,"onset_in_salami"] = row.onset_in_salami
	# Choose better of the matches
	# Update file with results
	# If no match yet, do nothing.

len(matchlist)
matchlist.to_csv(pair_list_filename,header=True,index=False)


for salami_id in remaining_ids:
	info = get_true_artist(salami_id)
	if info[3] == "Latcho Drom Soundtrack":
		manually_suggest_and_process(salami_id, "zVwDN-pyL8Y")
	# manually_suggest()


# Reset to original priorities to spare diff:
for salami_id in iso_ids + cod_ids:
	print(salami_id)
	prioritize_candidates(salami_id, no_longs=True, must_be_longer=True)


for salami_id in iso_ids + cod_ids:
	print(salami_id)
	prioritize_candidates(salami_id, no_longs=True, must_be_longer=True)


def update_matchlist_from_candidate_report(salami_id):
	# Open file
	global matchlist
	# Record best answer so far [might be nothing]
	# Read candidate report
	# Select best candidate from report [could be a "potential", not "match".]
	# Choose better of the matches
	# Update file with results
	# If no match yet, do nothing.





df = load_matchlist()
df.columns = df.columns.tolist()[:7] + ['matching_length','raw_hashes'] + df.columns.tolist()[9:]
for salami_id in df.salami_id:
	index = df.index[df['salami_id'] == salami_id].tolist()[0]
	youtube_id = df.loc[index,"youtube_id"]
	if youtube_id != "":
		matched_song_id, matching_length, raw_hashes, onset, hashes, total_hashes = test_for_matching_audio(youtube_id, salami_id, redo=False)
		df.loc[index,"matching_length"] = matching_length
		df.loc[index,"raw_hashes"] = raw_hashes

df.to_csv(salami_matchlist_csv_filename, header=True, index=False)





# Download youtube files for all the genres
md = load_song_info()
salami_pop = md.index[md["class"]=="popular"]
salami_jazz = md.index[md["class"]=="jazz"]
salami_world = md.index[md["class"]=="world"]
salami_classical = md.index[md["class"]=="classical"]
all_salami = list(salami_pop) + list(salami_jazz) + list(salami_world) + list(salami_classical)
all_salami.sort()
# download_for_salami_ids(salami_pop, min_sleep_interval=10)

# Run all the fingerprint tests
for salami_id in all_salami:
	test_fingerprints_for_salami_id(salami_id)

# How many match?
df = load_matchlist()
resolved_ids = list(df.salami_id[df.youtube_id != ""])
unresolved_ids = list(df.salami_id[df.youtube_id == ""])
ia_rwc_ids = list((md.salami_id[(md["source"]=="IA") | (md.source=="RWC")]).astype(int))
len(resolved_ids)
cod_ids = list((md.salami_id[md.source=="Codaich"]).astype(int))
cod_ids.sort()
# Note: none of the IA audio is involved in this.
# Note: none of the RWC songs were found.
rwc_ids = list(md.index[md.source=='RWC'])
set.intersection(set(rwc_ids),set(resolved_ids))
# Some of the Isophonics was found, naturally
iso_ids = list(md.index[md.source=='Isophonics'])
len(set.intersection(set(cod_ids),set(resolved_ids)))
len(set.intersection(set(iso_ids),set(resolved_ids)))

# Success across class:
for clas in ["popular","jazz","classical","world"]:
	clasids = list((md.salami_id[(md["class"]==clas) & (md.source=="Codaich")]).astype(int))
	print("{0} / {1}".format(len(set.intersection(set(clasids),set(resolved_ids))), len(clasids)))



# TODO:
# Find the rest of the audio
import matplotlib.pyplot as plt
plt.ion()

next_ids = list(set.difference(set(unresolved_ids),set(ia_rwc_ids)))
for id in next_ids[1:]:
	if (id >= 300):
		print(id)
		download_for_salami_ids([id],min_sleep_interval=60)
		test_fingerprints_for_salami_id(id)
