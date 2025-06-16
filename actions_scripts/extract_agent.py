import requests
import json

def downloadSnapshot():
    projectId = "68499f9e62b02399a43dacb3"
    apiKey = "321f573097b865f0bc910157ab15d5526429a86f6d2b4deea85322171a19766d95db581b069c03830f73990de89ece973edd5f81a659c98f001b900139661a9e"
    snapshotId = "6849a06a62b02399a43db2ff"
    headers = {
        "accept": "application/json",
        "X-API-KEY": apiKey
    }
    r = requests.post(url=f"https://api-trial.cognigy.ai/new/v2.0/snapshots/{snapshotId}/downloadlink", headers=headers, json={"projectId": projectId} )

    if r.status_code != 200:
        raise Exception("Not 200")
    
    downloadLink = json.loads(r.content)["downloadLink"]
    print(downloadLink)
    #Download
    r = requests.get(downloadLink, stream=True)

    if r.status_code == 200:
        with open("agent/snapshots/snapshot_name1.csnap", "wb") as file:
            for chunk in r.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Snapshot download complete")
    else:
        print("Snapshot download failed")
        print(r.status_code)