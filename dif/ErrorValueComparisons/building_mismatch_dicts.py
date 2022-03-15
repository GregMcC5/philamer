import metadata_utils as mu

#-----------------------
#-reading in dlxs, alma CSVs, along with the mismatches document-

alma = mu.read_csv("alma_full.csv")
dlxs = mu.read_csv("dlxs_full")
matches = mu.read_csv("matches_doc.csv")

#-----------------------
#-creating list for dicts

entries = []

#-----------------------
#-beginning loop

for matches_entry in matches:
    for alma_entry in alma:
        if matches_entry[0] == alma_entry[0]:
            for dlxs_entry in dlxs:
                if matches_entry[1] == dlxs_entry[1]:
                    #-----------------------
                    #-starting dict
                    matches_dict = {
                        "mms_id" : matches_entry[0],
                        "dlxs_id" : matches_entry[1],}
                    if "title" in matches_entry[3]:
                        matches_dict["alma_title"] = alma_entry[1]
                        matches_dict["dlxs_title"] = dlxs_entry[2]
                    if "author" in matches_entry[3]:
                        matches_dict["alma_author"] = alma_entry[2]
                        matches_dict["dlxs_author"] = dlxs_entry[3]
                    if "publication place" in matches_entry[3]:
                        matches_dict["alma_publication_place"] = alma_entry[3]
                        matches_dict["dlxs_publication_place"] = dlxs_entry[6]
                    if "publisher" in matches_entry[3]:
                        matches_dict["alma_publisher"] = alma_entry[4]
                        matches_dict["dlxs_publisher"] = dlxs_entry[7]
                    if "publication date" in matches_entry[3]:
                        matches_dict["alma_publication_date"] = alma_entry[5]
                        matches_dict["dlxs_publication_date"] = dlxs_entry[8]
                    if "notes" in matches_entry[3]:
                        matches_dict["alma_notes"] = alma_entry[6]
                        matches_dict["dlxs_notes"] = dlxs_entry[9]
                    if "language" in matches_entry[3]:
                        matches_dict["alma_language"] = alma_entry[7]
                        matches_dict["dlxs_language"] = dlxs_entry[10]
                    if "keywords" in matches_entry[3]:
                        matches_dict["alma_keywords"] = alma_entry[8]
                        matches_dict["dlxs_keywords"] = dlxs_entry[11]
                    matches_dict["alma_link"] = f"https://search.lib.umich.edu/catalog/record/{matches_entry[0]}"
                    matches_dict["dlxs_link"] = f"https://quod.lib.umich.edu/p/philamer/{matches_entry[1]}"
                    entries.append(matches_dict)
#-----------------------
#-writing json

mu.write_json("mismatched_values.json", entries)
print("done")