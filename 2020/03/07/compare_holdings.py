#!/usr/bin/env python3

import csv
import json
import os

from config import config

RESULTS_DIRECTORY = "{0}/{1}".format(os.path.expanduser("~"), config["results_dir"])
LLC_DIRECTORY = "{0}/{1}".format(RESULTS_DIRECTORY, "2019-09-30")
EP_DIRECTORY = "{0}/{1}".format(RESULTS_DIRECTORY, "2019-12-31")

def compare_holdings(ep, llc):
    with open("results.csv", "w") as results_file:
        filewriter = csv.writer(results_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Entity Name", "EPA Holdings", "LLC Holdings", "Difference"])
        for item in ep:
            if item in llc:
                filewriter.writerow([item, ep[item], llc[item], ep[item] - llc[item]])
            else:
                filewriter.writerow([item, ep[item], "0", ep[item]])

def get_quarter_total_values(data, directory):
    totals = {} 
    
    for cik in os.listdir(directory):
        holdings_file ="{0}/{1}/{2}".format(directory, cik, config["holdings_filename"])
        if os.path.isfile(holdings_file):
            with open(holdings_file) as holdings_data:
                for blob in holdings_data:
                    for holding in json.loads(blob)["_holdings_"]:
                        if holding["name"] in totals:
                            totals[holding["name"]] += holding["shares"]
                        else:
                            totals[holding["name"]] = holding["shares"]
                    
    return totals

def initialize():
    data = {}
    
    for cik in config["ciks"]:
        data[config["ciks"][cik]["name"]] = []

    return data

def write_data(data):
    final_data = {}
    
    for cik in config["ciks"]:
        final_data["X_{0}".format(config["ciks"][cik]["name"])] = []
        final_data[config["ciks"][cik]["name"]] = []

    final_data["X_{0}".format(config["total_title"])] = []
    final_data[config["total_title"]] = []
        

    for cik in data:
        for pair in data[cik]:
            final_data["X_{0}".format(cik)].append(pair[0])
            final_data[cik].append(pair[1])

    json_file = open("{0}".format("line-graph-data.json"), "a")
    json_file.write("{0}\n".format(json.dumps(final_data)))
    json_file.close()


llc_data = initialize()
llc_data = get_quarter_total_values(llc_data, LLC_DIRECTORY)

ep_data = initialize()
ep_data = get_quarter_total_values(ep_data, EP_DIRECTORY)

compare_holdings(ep_data, llc_data)
