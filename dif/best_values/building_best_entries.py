import metadata_utils as mu

#-----------------------

matches = mu.read_csv('flipped_matches_doc.csv')
alma = mu.read_csv("alma_full.csv")
dlxs = mu.read_csv("dlxs_full.csv")

#-----------------------

best_matches = []

check_author = []
check_pub_place = []
check_publisher = []
check_publication_date = []
check_language = []

for match in matches[2:]:
    for alma_record in alma:
        if match[0] == alma_record[0]:
            for dlxs_record in dlxs:
                if match[1] == dlxs_record[1]:
                    #-----------------------
                    #starting entry
                    best_entry = [match[0], match[1]]
                    #-----------------------
                    #looping on categories
                    if "title" not in match[4]:
                        best_entry.append(alma_record[1])
                    else:
                        best_entry.append(dlxs_record[2])
                    #-----------------------
                    #author
                    if "author" not in match[4]:
                        best_entry.append(alma_record[2])
                    else:
                        check_author.append([match[0],match[1],alma_record[2],dlxs_record[3],  f"https://search.lib.umich.edu/catalog/record/{match[0]}", f"https://quod.lib.umich.edu/p/philamer/{match[1]}"])
                        best_entry.append(None)
                    #-----------------------
                    #publication_place
                    if "publication place" not in match[4]:
                        best_entry.append(alma_record[3])
                    else:
                        check_pub_place.append([match[0],match[1],alma_record[3],dlxs_record[6],  f"https://search.lib.umich.edu/catalog/record/{match[0]}", f"https://quod.lib.umich.edu/p/philamer/{match[1]}"])
                        best_entry.append(None)
                    #-----------------------
                    #publisher
                    if "publisher" not in match[4]:
                        best_entry.append(alma_record[4])
                    else:
                        check_publisher.append([match[0],match[1],alma_record[4],dlxs_record[7],  f"https://search.lib.umich.edu/catalog/record/{match[0]}", f"https://quod.lib.umich.edu/p/philamer/{match[1]}"])
                        best_entry.append(None)
                    #-----------------------
                    #publication date
                    if "publication date" not in match[4]:
                        best_entry.append(alma_record[5])
                    else:
                        check_publication_date.append([match[0],match[1],alma_record[5],dlxs_record[8],  f"https://search.lib.umich.edu/catalog/record/{match[0]}", f"https://quod.lib.umich.edu/p/philamer/{match[1]}"])
                        best_entry.append(None)
                    #-----------------------
                    #language
                    if "language" not in match[3]:
                        best_entry.append(alma_record[7])
                    else:
                        check_language.append([match[0],match[1],alma_record[7],dlxs_record[10], f"https://search.lib.umich.edu/catalog/record/{match[0]}", f"https://quod.lib.umich.edu/p/philamer/{match[1]}" ])
                        best_entry.append(None)
                    #-----------------------
                    #notes
                    if "notes" not in match[4]:
                        best_entry.append(alma_record[6])
                    else:
                        best_entry.append(dlxs_record[9])
                    #-----------------------
                    #keywords
                    if "keywords" not in match[4]:
                        best_entry.append(alma_record[8])
                    else:
                        best_entry.append(dlxs_record[11])

                    best_matches.append(best_entry)

#-----------------------
#writting lists

check_headers = ["mms_id", "dlxs_id", "alma_value", "dlxs_value", "alma_url", "dlxs_url"]
list_name = ["best_matches","check_author","check_language", "check_pub_place", "check_publication_date", "check_publisher"]


best_matches.insert(0, ["mms_id", "dlxs_id", "title", "author", "publication place", "publisher", "publications date", "language", "notes", "keywords" ])
full_lists = [best_matches,check_author,check_language, check_pub_place, check_publication_date, check_publisher]

for check_list in full_lists[1:]:
    check_list.insert(0, check_headers)

i = 0
for l in full_lists:
    mu.write_csv(f"CheckLists/{list_name[i]}.csv", l)
    i += 1

print("done")