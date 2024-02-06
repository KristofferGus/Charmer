from charmer import *

table_df = get_tabel_df("tabel.html")
programs = ["d", "it"]
program_level = ["Bachelor", "Master"]
offering_types = ["Summer work"]
comapines = find_company(table_df, programs, program_level, offering_types)
print(comapines)