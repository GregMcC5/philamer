import metadata_utils as mu

#---------------
#reading in and combining

dlxs1 = mu.read_csv("philamer1_dlxs_metadata.csv")
dlxs2 = mu.read_csv("philamer2_dlxs_metadata.csv")

dlxs1.extend(dlxs2[1:])
dlxs = dlxs1

mu.write_csv("dlxs_full",dlxs)

#---------------
#readings in ids

philamer_mms_ids = mu.read_csv("Philamer_Identifiers_MMS_IDs_ Matched_Notis Ids.csv")

#---------------
#looping through identifiers, finding match, adding mms_id

for row in philamer_mms_ids:
    for entry in dlxs[1:]:
        if row[0][2:] == entry[0][:7]:
            entry.insert(0, row[2])

dlxs[0].insert(0,"mms_id")

#---------------
#reading in previously mismatched ones

missing_ids = mu.read_csv("missing_dlxs_mms_ids - Sheet1.csv")

for row in missing_ids:
    test_value = row[0][2:]
    for entry in dlxs:
        if entry[0][0] == "A" and row[2] == entry[0][:7]:
            entry.insert(0, row[3])

#---------------
#adding blanks

for entry in dlxs[1:]:
    if entry[0][0] == "A" or entry[0][0] != "9":
        entry.insert(0, None)

#---------------

mu.write_csv("dlxs_full",dlxs)
print("done")