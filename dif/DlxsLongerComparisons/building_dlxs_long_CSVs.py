import metadata_utils as mu
from datetime import datetime

#-----------------------
#-reading in dlxs, alma CSVs, along with the mismatches document-

alma = mu.read_csv("alma_full.csv")
dlxs = mu.read_csv("dlxs_full")
mismatches = mu.read_csv("matches_doc.csv")

#-----------------------
#-creating lists for individual fields (to eventually be exported as CSVs)

title = []
author = []
publication_place = []
publisher = []
publication_date = []
notes = []
language = []
keywords = []

headers = ["mms_id", "dlxs_id", "alma_value", 'dlxs_value']
longer_list = [title, author, publication_date, publisher, publication_date, notes, language, keywords]
for a_list in longer_list:
    a_list.append(headers)

#-----------------------
#-looping
start_time = datetime.now()
print("started at:", start_time)

for alma_record in alma:
    mms_alma = alma_record[0]
    for dlxs_record in dlxs:
        dlxs_id = dlxs_record[1]
        if alma_record[0] == dlxs_record[0]: #change here
            for mismatch_record in mismatches:
                if alma_record[0] == mismatch_record[0]:
                    #triple match found
                    #checking title
                    if "title" in mismatch_record[4]:
                        titles_list = [mms_alma, dlxs_id]
                        titles_list.append(alma_record[1])
                        titles_list.append(dlxs_record[2])
                        title.append(titles_list)
                    #checking author
                    if "author" in mismatch_record[4]:
                        author_list = [mms_alma, dlxs_id]
                        author_list.append(alma_record[2])
                        author_list.append(dlxs_record[3])
                        author.append(author_list)
                    #checking publication place
                    if "publication place" in mismatch_record[4]:
                        publication_place_list = [mms_alma, dlxs_id]
                        publication_place_list.append(alma_record[3])
                        publication_place_list.append(dlxs_record[6])
                        publication_place.append(publication_place_list)
                    #checking publisher
                    if "publisher" in mismatch_record[4]:
                        publisher_list = [mms_alma, dlxs_id]
                        publisher_list.append(alma_record[4])
                        publisher_list.append(dlxs_record[7])
                        publisher.append(publisher_list)
                    #checking publication date
                    if "publication date" in mismatch_record[4]:
                        publication_date_list = [mms_alma, dlxs_id]
                        publication_date_list.append(alma_record[5])
                        publication_date_list.append(dlxs_record[8])
                        publication_date.append(publication_date_list)
                    #checking notes
                    if "notes" in mismatch_record[4]:
                        notes_list = [mms_alma, dlxs_id]
                        notes_list.append(alma_record[6])
                        notes_list.append(dlxs_record[9])
                        notes.append(notes_list)
                    #checking language
                    if "language" in mismatch_record[4]:
                        language_list = [mms_alma, dlxs_id]
                        language_list.append(alma_record[7])
                        language_list.append(dlxs_record[10])
                        language.append(language_list)
                    #checking keywords
                    if "keywords" in mismatch_record[4]:
                        keywords_list = [mms_alma, dlxs_id]
                        keywords_list.append(alma_record[8])
                        keywords_list.append(dlxs_record[11])
                        keywords.append(keywords_list)
                    print(f"one completed at {datetime.now()}")

#-----------------------
#-writing csv

file_name = ["title", "author", "publication_date", "publisher", "publication_date", "notes", "language", "keywords"]
i = 0
for a_list in longer_list:
    mu.write_csv(f"DlxsLongerComparisons/{file_name[i]}.csv", a_list)
    i += 1

print(f"done at {datetime.now()}. This began at {start_time}")
