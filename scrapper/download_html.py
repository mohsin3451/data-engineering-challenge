import requests

url = "https://dir.indiamart.com/impcat/fly-ash-brick-making-machine.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

with open("fly_ash_brick_machine.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("HTML saved as fly_ash_brick_machine.html")
