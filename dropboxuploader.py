#!/usr/bin/python3

import dropbox

dbx=dropbox.Dropbox("vK8-PPhDTnAAAAAAAAAACGWylQd-KGSy69UfxePz2QkwlDw5W9_LyMeEtTHlNqms")

file = open("machine.log", "rb")

#response=dbc.put_file(fname, f)
response=dbx.files_upload(file, "/machine.log", mode=dropbox.files.WriteMode.overwrite)

print("uploaded: ", response)

file.close()
