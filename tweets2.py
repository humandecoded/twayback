import requests

with open(r'temp1.txt') as in_file, open(r'temp2.txt', 'w') as out_file:
    for line in in_file:
        if len(line) <= 60:
            out_file.write(line)

with open("temp2.txt") as fid:
    url_lines = set(line.rstrip() for line in fid)

results = []
headers = {'user-agent':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}

for url in url_lines:
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    results.append((url, status_code))

with open("temp3.txt", "w") as f:
    for url, status_code in results:
        f.write(f"{url} {status_code}\n")


bad_status = [' 404']

with open('temp3.txt') as oldfile, open('temp4.txt', 'w') as newfile:
    for line in oldfile:
        if any(bad_status in line for bad_status in bad_status):
            newfile.write(line)

with open('temp4.txt', 'r') as file :
  filedata = file.read()

filedata = filedata.replace(' 404', '')

with open('temp5.txt', 'w') as file:
  file.write(filedata)