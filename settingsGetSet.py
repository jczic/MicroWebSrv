import ujson
def setSettings(filename, SSID, PSK):
  
  try:
    import uos as os
  except:
    import os

  with open(filename, 'r') as settings:
    data = ujson.load(settings)
    data['STATION']['SSID'] = SSID
    data['STATION']['PSK'] = PSK
  os.remove(filename)
  with open(filename, 'w') as settings:
    ujson.dump(data, settings)
  print("Restart after Update")
  #machine.reset()

def getSettings (filename, AP):
  with open(filename, 'r') as settings:
    data = ujson.load(settings)
    if AP == True:
      SSID = data['AP']['SSID']
      PSK = data['AP']['PSK']
    else:
      SSID = data['STATION']['SSID']
      PSK = data['STATION']['PSK']

  return SSID, PSK