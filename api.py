
import requests

def fetchAPOD():
  URL_APOD = "https://api.nasa.gov/planetary/apod"
  date = '2020-01-22'
  params = {
      'api_key':'YwVmnhtmOzEe4RScNIqhfdW4fV9To1SzjTHNBkZg',
      'date':date,
      'hd':'True'
  }
  response = requests.get(URL_APOD,params=params).json()
  print(response)

print(fetchAPOD())