import numpy as np
import glob
import matplotlib.pyplot as plt
import os
import pymongo
import datetime
import pickle
    
def get_records(mongo_client, database_name, collection_name, query):
    
    collection = mongo_client[database_name][collection_name]
    response = collection.find(query)
        
    records = tuple(
        doc for doc in response
    )
            
    return records


# tstart = datetime.datetime.fromisoformat("2023-01-10")
# tstop  = datetime.datetime.fromisoformat("2023-12-01")

# query = dict()
# query.update({"tstart": {"$gte": tstart.timestamp()}})
# query.update({"tstop": {"$lte": tstop.timestamp()}})
        
query = None

read_db = False


if read_db:

    client_tcu  = pymongo.MongoClient('localhost:27017')
    records_tcu  = get_records(client_tcu,  'lst1_obs_summary', 'camera', query)

    client_caco = pymongo.MongoClient('localhost:27018')
    records_caco = get_records(client_caco, 'CACO', 'RUN_INFORMATION', query)

    with open('objects/records_tcu.pkl', 'wb') as f:
        pickle.dump(records_tcu, f, pickle.HIGHEST_PROTOCOL)
    with open('objects/records_caco.pkl', 'wb') as f:
        pickle.dump(records_caco, f, pickle.HIGHEST_PROTOCOL)

else:

    with open('objects/records_tcu.pkl', 'rb') as f:
        records_tcu = pickle.load(f)
    with open('objects/records_caco.pkl', 'rb') as f:
        records_caco = pickle.load(f)


for rec in records_tcu:
    try:
        rec["run_number"]
    except KeyError:
        rec["run_number"] = np.nan



def get_run_num_tcu(recs):
    run_numbers = []
    for rec in recs:
        try:
            run_numbers.append(rec["run_number"])
        except KeyError:
            pass
    return np.array(run_numbers)


run_num_tcu  = get_run_num_tcu(records_tcu)
run_num_caco = np.array([rec["run_number"] for rec in records_caco])

tstart_tcu  = np.array([datetime.datetime.utcfromtimestamp(rec["tstart"])       for rec in records_tcu])
tstop_tcu   = np.array([datetime.datetime.utcfromtimestamp(rec["tstop"])        for rec in records_tcu])
tstart_caco = np.array([datetime.datetime.fromisoformat(rec["start_time"][:-1]) for rec in records_caco])
tstop_caco  = np.array([datetime.datetime.fromisoformat(rec["stop_time"][:-1])  for rec in records_caco])

deltat_tcu = tstop_tcu - tstart_tcu
deltat_caco = tstop_caco - tstart_caco


higher_run = max(np.nanmax(run_num_caco), np.nanmax(run_num_tcu))

for run in np.arange(higher_run+1)[1:]:

    run_dict_caco = [rec for rec in records_caco if rec["run_number"] == run]
    isincaco = len(run_dict_caco) > 0

    run_dict_tcu = [rec for rec in records_tcu if rec["run_number"] == run]
    isintcu = len(run_dict_tcu) > 0

    if isincaco and isintcu:
        col = "92"
    elif isincaco or isintcu:
        col = "93"
    else:
        col = "91"

    if isintcu:
        end = "type --> "+run_dict_tcu[0]["kind"]
    else:
        end = ""
    if len(run_dict_tcu) == 2:
        end = end + " - 2 same run_num TCU runs!!!!!"

    print(f"\033[{col}mRun {run}  inCaCo: {isincaco} \tinTCU: {isintcu}\t{end}")

