import requests
import re
import sys

if len(sys.argv) < 2:
    print("No input file passed")
    exit(255)

try:
    gradle_wrapper_file = open(sys.argv[1], "r")
except:
    print("Unable to find the file")
    exit(1)


compatible_version_pattern = re.compile(r"<\D+>([0-9]+)<\/p><\D+>(\d\.\d)<\/p>")
gradle_version_pattern = re.compile(r".*gradle-(\d.\d).*.zip")

page = requests.get("https://docs.gradle.org/current/userguide/compatibility.html")

versions = {}

for match in compatible_version_pattern.finditer(page.content.decode()):
    versions[match.group(2)] = match.group(1)

res = gradle_version_pattern.search(gradle_wrapper_file.read())
current_version = res.group(1)

print(f"::set-output name=java-version::{versions[current_version]}")