from os import remove
import re
import metadata_utils as mu


#----reading in content----
philamer = mu.read_csv("new_full_best_values.csv")
subject_entries = []

#----starting intial keyword check loop----
counter = 0
for entry in philamer[1:]:
    #--setting counters
    keywords = entry[-1]
    phillipines_counter = 0
    hawaii_counter = 0
    guam_counter = 0
    puerto_rico_counter = 0
    cuba_counter = 0
    virgin_islands_counter = 0
    indonesia_counter = 0
    polynesia_counter = 0
    #--philippines
    phillipines_list = re.findall("philippin.*", keywords.lower())
    phillipines_list.extend(re.findall("filipin.*", keywords.lower()))
    phillipines_list.extend(re.findall("tagalog.*", keywords.lower()))
    phillipines_counter = len(phillipines_list)
    #--hawaii
    hawaii_list = re.findall("hawaii.*", keywords.lower())
    hawaii_list.extend(re.findall("hawaiʻi.*", keywords.lower()))
    hawaii_counter = len(hawaii_list)
    #--guam
    guam_list = re.findall("guam.*", keywords.lower())
    guam_list.extend(re.findall("guåhan.*", keywords.lower()))
    guam_counter = len(guam_list)
    #--puerto rico
    puerto_rico_list = re.findall("puerto rico.*", keywords.lower())
    puerto_rico_list.extend(re.findall("porto rico.*", keywords.lower()))
    puerto_rico_counter = len(puerto_rico_list)
    #--cuba
    cuba_list = re.findall("cuba.*", keywords.lower())
    cuba_counter = len(cuba_list)
    #--virgin_islands
    virgin_islands_list = re.findall("virgin islands.*", keywords.lower())
    virgin_islands_counter = len(virgin_islands_list)
    #--indonesia
    indonesia_list = re.findall("indonesi.*", keywords.lower())
    indonesia_counter = len(indonesia_list)
    #--polynesia
    polynesia_list = re.findall("polynesi*", keywords.lower())
    polynesia_counter = len(polynesia_list)
    #--comparing counters, making guess
    counters = {
        "Philippines": phillipines_counter,
        "Hawaii" : hawaii_counter,
        "Guam" : guam_counter,
        "Puerto Rico" : puerto_rico_counter,
        "Cuba" : cuba_counter,
        "Virgin Islands" : virgin_islands_counter,
        "Indonesia" : indonesia_counter,
        "Polynesia" : polynesia_counter}
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
    #--making full list of tags
    full_tag_list = []
    for key, val in counters.items():
        if val > 0:
            full_tag_list.append(key)
    #--appending to csv list
    subject_entries.append([entry[0],entry[1],guess, full_tag_list, phillipines_counter, hawaii_counter, guam_counter, puerto_rico_counter, cuba_counter, virgin_islands_counter, polynesia_counter, f"keywords checked: {keywords}"])

#----initial CSV----
subject_entries.insert(0,["mms_id", "dlxs_id", "subject guess", "full_tag_list", "phillipines_counter", "hawaii_counter", "guam_counter", "puerto_rico_counter", "cuba_counter", 'virgin_islands_counter', "polynesia_counter", "checked_string"])
mu.write_csv("subject_entries.csv", subject_entries)

#----starting secondarty title check loop----

update_counter = 0
for row in subject_entries[1:]:
    if row[2] == "Unable to Determine":
        for entry in philamer[1:]:
            if row[1] == entry[1]:
                title = entry[2]
                #--setting counters
                phillipines_counter = 0
                hawaii_counter = 0
                guam_counter = 0
                puerto_rico_counter = 0
                cuba_counter = 0
                virgin_islands_counter = 0
                indonesia_counter = 0
                polynesia_counter = 0
                #--philippines
                phillipines_list = re.findall("philippin.*", entry[2].lower())
                phillipines_list.extend(re.findall("filipin.*", entry[2].lower()))
                phillipines_list.extend(re.findall("tagalog.*", entry[2].lower()))
                phillipines_counter = len(phillipines_list)
                #--hawaii
                hawaii_list = re.findall("hawaii.*", entry[2].lower())
                hawaii_list.extend(re.findall("hawaiʻi.*", entry[2].lower()))
                hawaii_counter = len(hawaii_list)
                #--guam
                guam_list = re.findall("guam.*", entry[2].lower())
                guam_list.extend(re.findall("guåhan.*", entry[2].lower()))
                guam_counter = len(guam_list)
                #--puerto rico
                puerto_rico_list = re.findall("puerto rico.*", entry[2].lower())
                puerto_rico_list.extend(re.findall("porto rico.*", entry[2].lower()))
                puerto_rico_counter = len(puerto_rico_list)
                #--cuba
                cuba_list = re.findall("cuba.*", entry[2].lower())
                cuba_counter = len(cuba_list)
                #--virgin_islands
                virgin_islands_list = re.findall("virgin islands.*", entry[2].lower())
                virgin_islands_counter = len(virgin_islands_list)
                #--indonesia
                indonesia_list = re.findall("indonesi.*", entry[2].lower())
                indonesia_counter = len(indonesia_list)
                #--polynesia
                polynesia_list = re.findall("polynesi*", entry[2].lower())
                polynesia_counter = len(polynesia_list)
                counters = {
                    "Philippines": phillipines_counter,
                    "Hawaii" : hawaii_counter,
                    "Guam" : guam_counter,
                    "Puerto Rico" : puerto_rico_counter,
                    "Cuba" : cuba_counter,
                    "Virgin Islands" : virgin_islands_counter,
                    "Indonesia" : indonesia_counter,
                    "Polynesia" : polynesia_counter}
                big_count = 0
                guess = None
                for key,val in counters.items():
                    if val > big_count:
                        big_count = val
                        guess = key
                        update_counter += 1
                    elif val == big_count:
                        guess = None
                #--making full list of tags
                new_full_tag_list = []
                for key, val in counters.items():
                    if val > 0:
                        new_full_tag_list.append(key)
                #--finalizing edits
                if guess == None:
                    guess == "Unable to Determine"
                if guess != None:
                    new_row = [entry[0],entry[1],guess, new_full_tag_list, phillipines_counter, hawaii_counter, guam_counter, puerto_rico_counter, cuba_counter, virgin_islands_counter, polynesia_counter, f"title checked: {title}"]
                    subject_entries[subject_entries.index(row)] = new_row

mu.write_csv("editied_subject_entries.csv", subject_entries)

print("update counter:", update_counter)

#----counter JSON----
aggregator = {}
for row in subject_entries[1:]:
    guess = row[2]
    if guess in aggregator.keys():
        aggregator[guess] += 1
    else:
        aggregator[guess] = 1

mu.write_json("subject_counts.json", aggregator)

#----getting phi language list----
total_list_phi = []
language_flags = ("dictionary", "dictionaries", "diccionario", "diccionarios", "grammar", "gramática", "gramatica", "text", "texts")

for row in subject_entries[1:]:
    if row[2] == "Philippines":
        keywords = row[-1]
        keywords = keywords.split("', '")
        for flag in language_flags:
            for keyword in keywords:
                if flag in keyword.lower():
                    lang_keyword = keyword
                    #language keyword establishied
                    potential_lang = lang_keyword.split(" -- ")[0].split(" ")[0].replace("['", "")
                    if potential_lang not in total_list_phi:
                        total_list_phi.append(potential_lang)

remove_list = ("Christian", "Geography", "x", "Songs,", "Central", "Botany", "English", "keywords", "title", "Spanish")
for removal_term in remove_list:
    try:
        total_list_phi.remove(removal_term)
    except:
        continue

phi_lang_test_list = []
for row in subject_entries:
    if row[2] == "Unable to Determine":
        for lang in total_list_phi:
            if lang.lower() in row[-1].lower():
                phi_lang_test_list.append([row[0], row[1], row[2], lang, "Suggested: Philippines", row[-1]])

mu.write_csv("phi_lang_test.csv", phi_lang_test_list)

#----full tag counts----
flag_counters = {}
for row in subject_entries[1:]:
    for tag in row[3]:
        if tag in flag_counters.keys():
            flag_counters[tag] += 1
        else:
            flag_counters[tag] = 1

mu.write_json("full_tag_counts.json", flag_counters)

#----string tags counts----
string_counters = {}
for row in subject_entries[1:]:
    flags = str(row[3])
    print(flags)
    if flags in string_counters.keys():
        string_counters[flags] += 1
    else:
        string_counters[flags] = 1

mu.write_json("string_tag_counts.json", string_counters)

print("done")