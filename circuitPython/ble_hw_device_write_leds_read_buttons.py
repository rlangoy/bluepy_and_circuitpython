# Library for BLE Radio Advertising
#######################################
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

# Libray For grenerating a new Service
########################################
from adafruit_ble.services import Service
from adafruit_ble.uuid import StandardUUID
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.characteristics.int import Uint8Characteristic

class myLedervice(Service):
    uuid = StandardUUID(0xA000) # (0xA000 - my/Custom Service ID)
    leds = Uint8Characteristic(
        max_value=255,
        properties=Characteristic.WRITE ,
        uuid=StandardUUID(0xA002), #0ls -alcat xA002 -my/ID Write-to-Leds ID
    )
    bottons = Uint8Characteristic(
        max_value=255,
        properties=Characteristic.READ | Characteristic.NOTIFY  ,
        uuid=StandardUUID(0xA001), #0ls -alcat xA002 -my/ID Write-to-Leds ID
    )

# Create Service width Characteristic to turn-on/off leds
buttonAndLedService=myLedervice()

#Start BLE-Radio
ble = BLERadio()
ble.name = "RunesBLE"
leds=0
#Fortell verden hvem du er og hva du kan gjøre
advertisement = ProvideServicesAdvertisement(buttonAndLedService)
ble.start_advertising(advertisement)

print("Venter på tilkobling/bonding ")
while not ble.connected:
        pass

print("Bluetooth enhet er tilkoblet/bondet ")
#Ikke vis verden hvem du er :)
ble.stop_advertising()
    
oldLedVal=0
buttonVal=0
while ble.connected:
    #  Gjør noe morsomt    
    newLedValue=buttonAndLedService.leds
    if(oldLedVal != newLedValue) :
        print("New Led data " + str(newLedValue))
        oldLedVal=newLedValue
    buttonVal=buttonVal+1
    if(buttonVal>2):
       buttonVal=0
    buttonAndLedService.bottons=buttonVal
     
    
print("Bluetooth enhet er frakoblet")


