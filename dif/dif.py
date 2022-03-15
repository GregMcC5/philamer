
import metadata_utils as mu

#-----------------------
#-reading in alma and dlxs data-

alma = mu.read_csv("alma_full.csv")
dlxs = mu.read_csv("dlxs_full")

#-----------------------
#-converting to dicts-

alma_dict = {}
dlxs_dict = {}

for entry in alma:
    alma_dict[entry[0]] = entry

for entry in dlxs:
    dlxs_dict[entry[0]] = entry

mu.write_json("alma_test_dicts.json", alma_dict)
mu.write_json("dlxs_test_dicts.json", dlxs_dict)

#-----------------------
#-writing info into new csv-

matches_doc = []
matches_header = ["mms_id", "dlxs_id", "value mismatches?", "mismatched Fields", "fields where DLXS string is longer"]

#-----------------------
#-finding match, beginning comparison-

paranthetical_counter_1 = 0
paranthetical_counter_2 = 0

paranthetical_equality_ids = []
author_check = []
for mms_alma in alma_dict.keys():
    for mms_dlxs in dlxs_dict.keys():
        if mms_alma == mms_dlxs:
            match = []
            match.append(mms_alma)
            match.append(dlxs_dict[mms_dlxs][1])
            #-----------------------------
            #-establishing testing values-
            error_field_list = []
            error_value = 0
            dlxs_longer_list = []
            #-----------------------------
            #-checking title-
            #removes Volume and editions specifications
            #removes references to "microform", "electronic resource", etc in Alma titles

            if len(dlxs_dict[mms_dlxs][2]) > len(alma_dict[mms_alma][1]):
                dlxs_longer_list.append("title")

            if "[Vol. " in dlxs_dict[mms_dlxs][2]:
                dlxs_edit = dlxs_dict[mms_dlxs][2].replace(": ","").replace(":", "").replace("/ ", "").replace(",", "").strip(".").replace(".", "").lower().replace(";", "")
                dlxs_split_title = dlxs_edit.split("  ")
                if len(dlxs_split_title) <= 2:
                    dlxs_title = dlxs_split_title[0]
                else:
                    dlxs_title = " ".join(dlxs_split_title[0:-1])
            else:
                dlxs_title = dlxs_dict[mms_dlxs][2].replace(": ","").replace(":", "").replace("/ ", "").replace(",", "").strip(".").replace(".", "").lower().replace(";", "")
            if dlxs_title.strip(".").lower().replace(";", "").replace(" ", "") != alma_dict[mms_alma][1].replace(": ","").replace("/ ", "").replace(",", "").replace(" [microform]", "").replace(" [electronic resource]", "").strip(".").replace(".", "").lower().replace(";", "").replace("[microfilm]", "").replace(" ", ""):
                error_field_list.append("title")
                error_value += 1

            #-----------------------------
            #-checking author-
            #if a title has a paranthetical, checks to see if paranthetical is in corresponding string, or is equal to the other's paranthetical

            if len(dlxs_dict[mms_dlxs][3]) > len(alma_dict[mms_alma][2]):
                dlxs_longer_list.append("author")

            if "(" and ")" in dlxs_dict[mms_dlxs][3]:
                author_string = dlxs_dict[mms_dlxs][3]
                dlxs_paranthetical = author_string[author_string.index("(")+1:author_string.index(")")]
            else:
                dlxs_paranthetical = None

            if "(" and ")" in alma_dict[mms_alma][2]:
                author_string = alma_dict[mms_alma][2]
                alma_paranthetical = author_string[author_string.index("(")+1:author_string.index(")")]
            else:
                alma_paranthetical = None

            if dlxs_paranthetical and not alma_paranthetical:
                paranthetical_counter_1 += 1
                if dlxs_paranthetical not in alma_dict[mms_alma][2]:
                    error_field_list.append("author")
                    error_value += 1
            elif alma_paranthetical and not dlxs_paranthetical:
                paranthetical_counter_2 += 1
                if alma_paranthetical not in dlxs_dict[mms_dlxs][3]:
                    error_field_list.append("author")
                    error_value += 1
            else:
                if dlxs_dict[mms_dlxs][3].strip(".").strip().lower().strip().replace(" ", "").replace(".", "").replace(",", "") != alma_dict[mms_alma][2].strip(".").strip().lower().strip().replace(" ", "").replace(".", "").replace(",", ""):
                    error_field_list.append("author")
                    error_value += 1

            if "author" in error_field_list:
                if alma_paranthetical and dlxs_paranthetical:
                    if alma_paranthetical == dlxs_paranthetical:
                        error_field_list.remove("author")
                        error_value -= 1
                        paranthetical_equality_ids.append([mms_alma])

        #this was an attempt to loop through and remove years from the author fields; but it didn't work.
            # if "author" in error_field_list:
            #     #dlxs re-loop
            #     dlxs_author = dlxs_dict[mms_dlxs][3].strip(".").strip().lower().strip().replace(" ", "").replace(".", "").replace(",", "").replace("b. ", "").replace("d. ", "").replace("ca. ", "").replace("ed. ", "").replace("fl. ", "")
            #     remove_list = []
            #     for character in dlxs_dict[mms_dlxs][3]:
            #         try:
            #             int(character)
            #         except:
            #             remove_list.append(character)
            #     for character in remove_list:
            #         dlxs_author = dlxs_author.replace(character, "")

            #     #alma re-loop
            #     alma_author = alma_dict[mms_alma][2].strip(".").strip().lower().strip().replace(" ", "").replace(".", "").replace(",", "").replace("b. ", "").replace("d. ", "").replace("ca. ", "").replace("ed. ", "").replace("fl. ", "")
            #     remove_list = []
            #     for character in alma_dict[mms_alma][2]:
            #         try:
            #             int(character)
            #         except:
            #             remove_list.append(character)
            #     for character in remove_list:
            #         alma_author = alma_author.replace(character, "")

            #     if dlxs_author and alma_author:
            #         if dlxs_author == alma_author:
            #             error_field_list.remove("author")
            #             error_value -= 1
            #             author_check.append([mms_alma, [dlxs_dict[mms_dlxs][3], dlxs_author], [alma_dict[mms_alma][2], alma_author]])

            #-----------------------------
            #-checking publication place-

            if len(dlxs_dict[mms_dlxs][6]) > len(alma_dict[mms_alma][3]):
                dlxs_longer_list.append("publication place")

            if dlxs_dict[mms_dlxs][6] == "unknown":
                dlxs_pub_place = ""
            else:
                dlxs_pub_place = dlxs_dict[mms_dlxs][6]

            if dlxs_pub_place.strip(" :").strip("[").strip(",").strip().strip(",").replace(".", "").replace(":", "") != alma_dict[mms_alma][3].strip(",").strip(" :").strip("[").strip(",").replace(".", "").replace(":", ""):
                error_field_list.append("publication place")
                error_value += 1

            #-----------------------------
            #-checking publisher-

            if len(dlxs_dict[mms_dlxs][7]) > len(alma_dict[mms_alma][4]):
                dlxs_longer_list.append("publisher")

            if dlxs_dict[mms_dlxs][7] == "unknown":
                dlxs_publisher = ""
            else:
                dlxs_publisher = dlxs_dict[mms_dlxs][7]

            if dlxs_publisher.strip(",") != alma_dict[mms_alma][4].strip(","):
                error_field_list.append("publisher")
                error_value += 1
            #-----------------------------
            #-checking publication date-

            if len(dlxs_dict[mms_dlxs][8]) > len(alma_dict[mms_alma][5]):
                dlxs_longer_list.append("publication date")

            if dlxs_dict[mms_dlxs][8] == "unknown":
                dlxs_pub_date = ""
            else:
                dlxs_pub_date = dlxs_dict[mms_dlxs][8]

            if dlxs_pub_date.strip("[").strip("]").strip(".") != alma_dict[mms_alma][5].strip("[").strip("]").strip("."):
                error_field_list.append("publication date")
                error_value += 1

            #-----------------------------
            #-checking notes-

            if len(dlxs_dict[mms_dlxs][9]) > len(alma_dict[mms_alma][6]):
                dlxs_longer_list.append("notes")

            #I explored the possibility of spliiting the notes string into a list and looping through each to check, but have not have a chance to implement it yet
            if dlxs_dict[mms_dlxs][9].strip("['").strip(".']").strip("[").strip("]").strip().replace(".", "").replace(",", "").replace(":", "").replace("'", "").replace("]", "").replace("[", "") != alma_dict[mms_alma][6].strip("[").strip("]").strip("['").strip(".']").replace(".", "").replace(",", "").replace(":", "").replace("'", "").replace("]", "").replace("[", ""):
                error_field_list.append("notes")
                error_value += 1
            #-----------------------------
            #-checking language-
            # in alma_to_csv.py I pulled each entry's  3-digit lanugage code from its 008 MARC field
            if alma_dict[mms_alma][7].lower() not in dlxs_dict[mms_dlxs][10].lower():
                error_field_list.append("language")
                error_value += 1
            #-----------------------------
            #-checking keywords-
            #to neutralize keyword order, I split keywords strings into a list of keywords and looped over the between the two entries.

            if len(dlxs_dict[mms_dlxs][11]) > len(alma_dict[mms_alma][8]):
                dlxs_longer_list.append("keywords")

            if dlxs_dict[mms_dlxs][11] == "[]":
                dlxs_dict[mms_dlxs][11] = ""

            #for entires with multiple keywords, splitting them up and cycles through both lists to check them; elimninates flags for keywords in different orders
            dlxs_keywords_str = dlxs_dict[mms_dlxs][11]
            fixed_dlxs_keywords = []
            if "', '" in dlxs_keywords_str:
                dlxs_keywords_str = dlxs_keywords_str.replace("', '", "|")
                dlxs_keywords_list = dlxs_keywords_str.split("|")
                for keyword in dlxs_keywords_list:
                    fixed_dlxs_keywords.append(keyword.strip("[").strip("'").strip("]").strip().replace(".", "").lower())
            else:
                dlxs_keywords_list = None
                fixed_dlxs_keywords = None

            alma_keywords_str = alma_dict[mms_alma][8]
            fixed_alma_keywords = []
            if "', '" in alma_keywords_str:
                alma_keywords_str = alma_keywords_str.replace("', '", "|")
                alma_keywords_list = alma_keywords_str.split("|")
                for keyword in alma_keywords_list:
                    fixed_alma_keywords.append(keyword.strip("[").strip("'").strip("]").strip().replace(".", "").lower())
            else:
                alma_keywords_list = None
                fixed_alma_keywords = None

            keyword_error_count = 0
            if fixed_alma_keywords and fixed_dlxs_keywords:
                for alma_keyword in fixed_alma_keywords: 
                    if alma_keyword not in fixed_dlxs_keywords:
                        keyword_error_count += 1
                for dlxs_keyword in fixed_dlxs_keywords:
                    if dlxs_keyword not in fixed_alma_keywords:
                        keyword_error_count += 1
                if keyword_error_count > 0:
                    error_field_list.append("keywords")
                    error_value += 1
            else:
                if dlxs_dict[mms_dlxs][11].replace(".", "") != alma_dict[mms_alma][8].replace(".", ""):
                    error_field_list.append("keywords")
                    error_value += 1

            #-----------------------------
            #-creating mismatch values-
            if error_value == 0:
                match.append("No")
            else:
                match.append("Yes")
            match.append(error_field_list)
            match.append(dlxs_longer_list)
            matches_doc.append(match)

headers = ["mms_id", "dlxs_id", "value mismatches?", "mismatched Fields", "fields where DLXS string is longer"]
matches_doc[0] = headers
mu.write_csv("matches_doc.csv", matches_doc)

print("done")
