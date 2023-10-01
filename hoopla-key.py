import glob
import requests
import subprocess
import sys

print("Hoopla Digital Downloader by Larsenv\n")

if len(sys.argv) != 3:
    print("Usage: hoopla-key.py <url> <token>\n")
    sys.exit(1)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.165 Safari/537.36",
    "accept": "*/*",
    "content-type": "application/json",
}

if "/" in sys.argv[1]:
    hoopla_code = sys.argv[1].split("/")[-1]
else:
    hoopla_code = sys.argv[1]

json_data = {
    "operationName": "FETCH_TITLE_DETAIL",
    "variables": {
        "id": hoopla_code,
        "includeDeleted": True,
    },
    "query": "query FETCH_TITLE_DETAIL($id: ID!, $includeDeleted: Boolean) {\n  title(criteria: {id: $id, includeDeleted: $includeDeleted}) {\n    episodes {\n      title\n    mediaKey\n      }\n  title\n    mediaKey\n    }\n}",
}

response = requests.post(
    "https://patron-api-gateway.hoopladigital.com/graphql",
    headers=headers,
    json=json_data,
)

iterate = response.json()["data"]["title"]["episodes"]

if not iterate:
    iterate = [response.json()["data"]["title"]]

for episode in iterate:
    title = episode["title"]
    url = "https://dash.hoopladigital.com/" + episode["mediaKey"] + "/Manifest.mpd"
    try:
        pssh = (
            requests.get(url)
            .content.split(
                b'<ContentProtection schemeIdUri="urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed">'
            )[1]
            .split(b"<cenc:pssh>")[1]
            .split(b"</cenc:pssh>")[0]
        ).decode("utf-8")
    except:
        continue

    with open("headers.py", "wb") as f:
        f.write(
            b"""headers = {
            "license": "https://lic.drmtoday.com/license-proxy-widevine/cenc/?specConform=true",
            "dt-custom-data": \""""
            + sys.argv[2].encode("utf-8")
            + b"""",
            "pssh": \""""
            + pssh.encode("utf-8")
            + b"""",
            "buildInfo": "",
            "proxy": "",
        }"""
        )

    response = subprocess.run(
        [
            "python3",
            "l3.py",
            pssh,
            "https://lic.drmtoday.com/license-proxy-widevine/cenc/?specConform=true",
        ],
        stdout=subprocess.PIPE,
        text=True,
    ).stdout

    print(url + ": " + title + ": " + "--key " + response.split("--key ")[1])

    print("Downloading...")

    subprocess.call(["yt-dlp", "--allow-unplayable-formats", url])
    if len(glob.glob("*.mp4")) > 0:
        subprocess.call(["mv", glob.glob("*.mp4")[0], "Input.mp4"])
    subprocess.call(["mv", glob.glob("*.m4a")[0], "Input.m4a"])
    if len(glob.glob("*.mp4")) > 0:
        subprocess.call(
            [
                "mp4decrypt",
                "--key",
                response.split("--key ")[1],
                "Input.mp4",
                "Output.mp4",
            ]
        )
    subprocess.call(
        ["mp4decrypt", "--key", response.split("--key ")[1], "Input.m4a", "Output.m4a"]
    )
    if len(glob.glob("*.mp4")) > 0:
        subprocess.call(
            [
                "ffmpeg",
                "-i",
                "Output.mp4",
                "-i",
                "Output.m4a",
                title.replace("/", "-") + ".mp4",
            ]
        )
    else:
        subprocess.call(["mv", "Output.m4a", title.replace("/", "-") + ".m4a"])
    subprocess.call(["rm", "Input.mp4"])
    subprocess.call(["rm", "Input.m4a"])
    subprocess.call(["rm", "Output.mp4"])
    subprocess.call(["rm", "Output.m4a"])
