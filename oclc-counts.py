#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import requests
import json
import csv

#load config
with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)
      
serviceURL = config.get('searchv2_url')

# get a token
scope = ['wcapi:view_summary_holdings']
auth = HTTPBasicAuth(config.get('key'), config.get('secret'))
client = BackendApplicationClient(client_id=config.get('key'), scope=scope)
wskey = OAuth2Session(client=client)

#Open input file to Look for OCLC Numbers
input_file = "oclc-test.csv"
search_index = "oclc".upper()
delimiter = "; "

# turn input file into list
with open(input_file, 'r', encoding="utf-8") as f:
  reader = csv.reader(f)
  rows = list(reader)
  header = rows.pop(0)
  header.extend(('Held By GROUP', 'Held By STATE', 'Total WorldCat Holdings'))

#Open file to which to write results
with open("output-oclc-holdings.csv", "w", encoding="utf-8", newline='') as y:
  rows.insert(0,header)
  dw = csv.DictWriter(y, delimiter=',',fieldnames=header)
  dw.writeheader()

def main():
    
    # find search index column
    search_index_column = header.index(search_index)

    index = ''
    
    # parse rows (skip header)
    for row in rows[1:]:

        # split search index by delimiter
        search_indexes = row[search_index_column].split(delimiter)

        #generate queries
        try:
          token = wskey.fetch_token(token_url=config.get('token_url'), auth=auth)
        except BaseException as err:
          print(err)

        query_group = config.get('group_symbol')
        query_state = config.get('state_code')

        wc2_queries = []
        for index in search_indexes:
            if index:
                index = str(index)
                query_group = str(query_group)
                query_state = str(query_state)
                QueryURLs = {'heldByGroup':'/bibs-summary-holdings?oclcNumber='+ index + '&heldByGroup='+ query_group +'&format=json',
                            'heldInState':'/bibs-summary-holdings?oclcNumber='+ index + '&heldInState='+ query_state +'&format=json',
                            'totalHoldings':'/bibs-summary-holdings?oclcNumber='+ index + '&format=json'
                            }

                def getResponse():  
                  r = wskey.get(serviceURL + getCall)
                  r.raise_for_status
                  response = r.json()
                  holdCount = response["briefRecords"][0]["institutionHolding"]["totalHoldingCount"]
                  return holdCount

            #get holdings
                try:
                  getCall = QueryURLs['heldByGroup']
                  group = str(getResponse())
                  #print("group="+group)
                  getCall = QueryURLs['heldInState']
                  state = str(getResponse())
                  #print("state="+state)
                  getCall = QueryURLs['totalHoldings']
                  total=str(getResponse())
                  #print("total="+total)
                  listforCSV = [group,state,total]
                  row.extend((listforCSV))
                  print(row)
                except requests.exceptions.HTTPError as err:
                  print(err)
            
            #write output      
            with open("output-oclc-holdings.csv", "a", encoding="utf-8", newline='') as y:
                writer = csv.writer(y)
                writer.writerow(row)       


# top level            
if __name__ == "__main__":
    main()

  
   