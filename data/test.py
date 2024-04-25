from requests import get

print(get("http://127.0.0.1:5000/player/advancements/w0dr").json())
print(" ")
print(" ")
print(get("http://127.0.0.1:5000/player/stats/w0dr").json())
