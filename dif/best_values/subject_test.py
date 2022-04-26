import re
import metadata_utils as mu


#----reading in content----
philamer = mu.read_csv("new_full_best_values.csv")
subject_entries = []

#----starting loop----
counter = 0
for entry in philamer[1:]:
    #setting counters
    keywords = entry[-1]
    phillipines_counter = 0
    hawaii_counter = 0
    guam_counter = 0
    puerto_rico_counter = 0
    cuba_counter = 0
    virgin_islands_counter = 0
    indonesia_counter = 0
    #philippines
    phillipines_list = re.findall("philippin.*", keywords.lower())
    phillipines_list.extend(re.findall("filipin.*", keywords.lower()))
    phillipines_list.extend(re.findall("tagalog.*", keywords.lower()))
    phillipines_counter = len(phillipines_list)
    #hawaii
    hawaii_list = re.findall("hawaii.*", keywords.lower())
    hawaii_list.extend(re.findall("hawaiʻi.*", keywords.lower()))
    hawaii_counter = len(hawaii_list)
    #guam
    guam_list = re.findall("guam.*", keywords.lower())
    guam_list.extend(re.findall("guåhan.*", keywords.lower()))
    guam_counter = len(guam_list)
    #puerto rico
    puerto_rico_list = re.findall("puerto rico.*", keywords.lower())
    puerto_rico_list.extend(re.findall("port rico.*", keywords.lower()))
    puerto_rico_counter = len(puerto_rico_list)
    #cuba
    cuba_list = re.findall("cuba.*", keywords.lower())
    cuba_counter = len(cuba_list)
    #virgin_islands
    virgin_islands_list = re.findall("virgin islands.*", keywords.lower())
    virgin_islands_counter = len(virgin_islands_list)
    # #indonesia
    # indonesia_list = re.findall("indonesi.*", keywords.lower())
    # indonesia_counter = len(indonesia_list)
    #comparing counters, making guess
    counters = {
        "Philippines": phillipines_counter,
        "Hawaii" : hawaii_counter,
        "Guam" : guam_counter,
        "Puerto Rico" : puerto_rico_counter,
        "Cuba" : cuba_counter,
        "Virgin Islands" : virgin_islands_counter,
        # "Indonesia" : indonesia_counter
    }
    big_count = 0
    guess = None
    for key,val in counters.items():
        if val > big_count:
            big_count = val
            guess = key
        elif val == big_count:
            guess = None
    if guess == None:
        guess = "Unable to Determine"

    #appending to csv list
    subject_entries.append([entry[0],entry[1],guess, phillipines_counter, hawaii_counter, guam_counter, puerto_rico_counter, cuba_counter, virgin_islands_counter, keywords])

#----finalizing CSV----
subject_entries.insert(0,["mms_id", "dlxs_id", "subject guess", "phillipines_counter", "hawaii_counter", "guam_counter", "puerto_rico_counter", "cuba_counter", 'virgin_islands_counter', "keywords"])
mu.write_csv("subject_entries.csv", subject_entries)

#----building counter JSON----
aggregator = {}
for row in subject_entries[1:]:
    guess = row[2]
    if guess in aggregator.keys():
        aggregator[guess] += 1
    else:
        aggregator[guess] = 1

mu.write_json("subject_counts", aggregator)

print("done")