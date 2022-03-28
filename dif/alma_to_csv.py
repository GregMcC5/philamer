
import pymarc
import metadata_utils as mu

#--------------------------------------------
#reading MARC file into a list of pymarch objects.

marc_file = "updated_philamer_alma_export.mrc"
marc_records = []
with open(marc_file, 'rb') as data:
    reader = pymarc.MARCReader(data)
    for record in reader:
        marc_records.append(record)
#--------------------------------------------
#making a new list of marc records as json-friendly dicts

marc_dicts = []
for record in marc_records:
    marc_dicts.append(record.as_dict())

mu.write_json("test_marc_dicts.json", marc_dicts)

#--------------------------------------------
#cleaning json. Consolidating subdictionaries and sublists

for record in marc_dicts:
    if record["fields"]:
        for field in record["fields"]:
            for key, val in field.items():
                if key in record.keys():
                    key_counter = 1
                    for record_key in record.keys():
                        if key == record_key:
                            key_counter += 1
                    record[f"{key}_{key_counter}"] = val
                else:
                    record[f"{key}"] = val
        del record["fields"]

#at this point, records that have multiple 650 fields have overwritten the last one.
mu.write_json("test_marc_dicts.json", marc_dicts)

for record in marc_dicts:
    for key, val in record.items():
        if isinstance(val, dict):
            replace_dict = {}
            for key2, val2 in val.items():
                if key2 == "subfields" and isinstance(val2, list):
                    for subfield_items in val2:
                        if isinstance(subfield_items, dict):
                            for sub_key, sub_val in subfield_items.items():
                                if sub_key not in replace_dict.keys(): #change
                                    replace_dict[sub_key] = sub_val #change
                                else: #change
                                    replace_dict[sub_key] = replace_dict[sub_key] + " " + sub_val #change
            record[key] = replace_dict

mu.write_json("test_marc_dicts.json", marc_dicts)

#--------------------------------------------
#developing new list of dicts with the headings of DLXS data:

#--here's a reference dict
# alma_reference_dict = {
#     "mms_id" : None,
#     "alma_title" : None,
#     "alma_author": None,
#     "alma_pubplace" : None,
#     "alma_publisher": None,
#     "alma_pubdate" : None,
#     "alma_notes" : None,
#     "alma_lang" : None,
#     "alma_keywords" : None,
#     }

new_alma_dicts = []
#--looping through each record dict, extracting info to building each "new_alma_dict" and appending it to "new_alma_dicts"
for record in marc_dicts:
    new_record_dict = {
    "mms_id" : None,
    "alma_title" : None,
    "alma_author": None,
    "alma_pubplace" : None,
    "alma_publisher": None,
    "alma_pubdate" : None,
    "alma_notes" : None,
    "alma_lang" : None,
    "alma_keywords" : None}

    #--establishing "alma_id" pair:

    new_record_dict["mms_id"] = record["001"]

    #--establishing "alma_title":

    if record["245"] and isinstance(record["245"], dict):
        if len(record["245"].keys()) == 1:
            for val in record["245"].values():
                new_record_dict["alma_title"] = val
        elif len(record['245'].keys()) > 1:
            title_list = []
            for val in record["245"].values():
                title_list.append(val)
            new_title = " ".join(title_list)
            new_record_dict["alma_title"] = new_title

    #--establishing "alma_author", checking for both 100 and 110 fields:

    test_100 = record.get('100')
    test_110 = record.get('110')

    if test_100 and isinstance(record["100"], dict):
        if len(record["100"].keys()) == 1:
            for val in record["100"].values():
                new_record_dict["alma_author"] = val
        elif len(record["100"].keys()) > 1:
            author_list = []
            for val in record["100"].values():
                author_list.append(val)
            new_author = " ".join(author_list)
            new_record_dict["alma_author"] = new_author
    elif test_110 and isinstance(record["110"], dict):
        if len(record["110"].keys()) == 1:
            for val in record["110"].values():
                new_record_dict["alma_author"] = val
        elif len(record["110"].keys()) > 1:
            author_list = []
            for val in record["110"].values():
                author_list.append(val)
            new_author = " ".join(author_list)
            new_record_dict["alma_author"] = new_author

    #--establishing alma_pubplace, alma_publisher, alma_pubdate

    test_260 = record.get("260")
    if test_260 and isinstance(record["260"], dict):
        new_record_dict["alma_pubplace"] = record["260"].get("a")
        new_record_dict["alma_publisher"] = record["260"].get("b")
        new_record_dict["alma_pubdate"] = record["260"].get("c")

    #--establishing alma_notes

    new_record_dict["alma_notes"] = []

    if record.get("500") and isinstance(record['500'], dict):
        new_record_dict["alma_notes"].append(record["500"].get("a"))
    if record.get("500_2") and isinstance(record['500_2'], dict):
        new_record_dict["alma_notes"].extend(record["500_2"].values())
    if record.get("504") and isinstance(record['504'], dict):
        new_record_dict["alma_notes"].extend(record["504"].values())
    if record.get("505") and isinstance(record['505'], dict):
        new_record_dict["alma_notes"].extend(record["505"].values())
    if record.get("505_2") and isinstance(record['505_2'], dict):
        new_record_dict["alma_notes"].extend(record["505_2"].values())
    if record.get("515") and isinstance(record['515'], dict):
        new_record_dict["alma_notes"].extend(record["515"].values())
    if record.get("515_2") and isinstance(record['515_2'], dict):
        new_record_dict["alma_notes"].extend(record["515_2"].values())
    if record.get("533") and isinstance(record["533"], dict):
        new_record_dict["alma_notes"].extend(record["533"].values())
    if record.get("533_2") and isinstance(record["533_2"], dict):
        new_record_dict["alma_notes"].extend(record["533_2"].values())
    if record.get("546") and isinstance(record['546'], dict):
        new_record_dict["alma_notes"].extend(record["546"].values())
    if record.get("590") and isinstance(record["590"], dict):
        new_record_dict["alma_notes"].extend(record["590"].values())
    if record.get("590_2") and isinstance(record['590_2'], dict):
        new_record_dict["alma_notes"].extend(record["590_2"].values())


    #--establishing alma_lang

    test_008 = record.get("008")
    if test_008 and isinstance(record["008"], str):
        lang_code = record["008"][-5: -2]
        new_record_dict["alma_lang"] = lang_code

    #--establishing alma_keywords

    keywords = []
    if record.get("650") and isinstance(record["650"], dict):
        val_list = list(record["650"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if record.get("650_2") and isinstance(record["650_2"], dict):
        val_list = list(record["650_2"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if record.get("651") and isinstance(record["651"], dict):
        val_list = list(record["651"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if record.get("651_2") and isinstance(record["651_2"], dict):
        val_list = list(record["651_2"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if record.get("600") and isinstance(record["600"], dict):
        val_list = list(record["600"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if record.get("600_2") and isinstance(record["600_2"], dict):
        val_list = list(record["600_2"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if record.get("610") and isinstance(record["610"], dict):
        val_list = list(record["610"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if record.get("610_2") and isinstance(record["610_2"], dict):
        val_list = list(record["610_2"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if record.get("630") and isinstance(record["630"], dict):
        val_list = list(record["630"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if record.get("630_2") and isinstance(record["630_2"], dict):
        val_list = list(record["630_2"].values())
        joined_vals = " -- ".join(val_list)
        keywords.append(joined_vals)

    if len(keywords) > 0:
        new_record_dict["alma_keywords"] = keywords
    else:
        new_record_dict["alma_keywords"] = None

    #--dict is built, adding it to new list

    new_alma_dicts.append(new_record_dict)

mu.write_json("new_marc_dicts.json", new_alma_dicts)

#--------------------------------------------
#custom conversion of alma dicts to csv; using pandas caused trouble

new_alma_lists = []
new_alma_lists.append(list(new_alma_dicts[0].keys()))

for dict in new_alma_dicts:
    new_alma_lists.append(list(dict.values()))

mu.write_csv("alma_full.csv", new_alma_lists)

print("done")