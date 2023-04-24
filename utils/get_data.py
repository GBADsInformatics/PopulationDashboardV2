import pandas as pd
import utils.api_helpers as ah
import os


### Get data for the dashboard and store it in /data
###--------------Get data------------------------------------

tables = ['livestock_countries_population_eurostat','livestock_countries_population_faostat','livestock_countries_population_faotier1','livestock_countries_population_oie','livestock_countries_population_unfccc']

wd = os.getcwd()

# for i in tables: 
#     url = ah.construct_api_call(i)
#     df = ah.make_call(url)
#     source = str.split(i, '_')[-1:]
#     out_name = '%s/data/%s.csv' % (wd, source[0])
#     df.to_csv(out_name, index=False)

for i in tables: 
    df = ah.get_dataframe(i)
    source = str.split(i, '_')[-1:]
    out_name = '%s/data/%s.csv' % (wd, source[0])
    df.to_csv(out_name, index=False)