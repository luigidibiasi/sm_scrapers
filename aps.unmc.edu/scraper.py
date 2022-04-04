# In order to download HTML resources ... 
from urllib import request, parse
import ssl
import certifi
import re
ssl._create_default_https_context = ssl._create_unverified_context

MUST_UPDATE=False;

# STEP0: download all the peptides name from 
# https://aps.unmc.edu/database/anti
# NOTE: we must use POST to send the parameters to the web server.
param = {}
param['activity']="G";
param['name']="Antibacterial peptides";
data = parse.urlencode(param).encode()
req =  request.Request("https://aps.unmc.edu/database/anti", data=data) 

if (MUST_UPDATE):
    resp = request.urlopen(req) #re-enable this to update peptide list in the future
    with open("./peptides_name.html","w") as writer:
        html_response = resp.read()
        writer.write(str(html_response))
        writer.close()

# STEP1: Parse HTML output from link /anti
# The structure of the HTML seems standard.
with open("./peptides_name.html") as reader:
    content = reader.read()
    # try to extract all <form> tags
    result = [i for j in re.findall(r'method="([^ >"]*)"|action="([^ >"]*)"|name="([^ >"]*)"',content) for i in j if i]
    # extract all the peptide ids
    for t in range(0,len(result),4): 
        peptide_id = result[t]
        peptide_id = peptide_id.replace("AP","")
        # download data regarding each peptide.
        print("Downloading data for peptide " + str(peptide_id) + " ...")
        param = {}
        param['ID']=peptide_id;
        data = parse.urlencode(param).encode()
        req =  request.Request("https://aps.unmc.edu/database/peptide", data=data) 
        resp = request.urlopen(req) #re-enable this to update peptide list in the future
        with open("./peptides_data/"+peptide_id+".html","w") as writer:
            html_response = resp.read()
            writer.write(str(html_response))
            writer.close()
            print(html_response)
        print("\t[DONE]")

#STEP2: For each peptide into download folder ==> parse HTML and extract structured data 
