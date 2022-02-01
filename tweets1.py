import os
import re

with open("sample.txt", "r") as file:
	for line in file:
		urls = re.findall('https?://[^\s<>"]+[|www\.^\s<>"]+', line)
		print(*urls, file=open("temp1.txt", "a"))