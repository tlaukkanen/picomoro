import time
from machine import Pin, PWM

# SMA420564 pinout mapping to GPIO pins
pin = [
  # Top row
  Pin(4, Pin.OUT), # GP4
  Pin(5, Pin.OUT), # GP5
  Pin(6, Pin.OUT), # GP6
  Pin(7, Pin.OUT), # GP7
  Pin(8, Pin.OUT), # GP8
  Pin(9, Pin.OUT), # GP9
  
  # Bottom row
  Pin(16, Pin.OUT), # GP16
  Pin(17, Pin.OUT), # GP17
  Pin(18, Pin.OUT), # GP18
  Pin(19, Pin.OUT), # GP19
  Pin(20, Pin.OUT), # GP20
  Pin(21, Pin.OUT)  # GP21
]

buzzer = PWM(Pin(22))

def beep():
  buzzer.freq(600)
  buzzer.duty_u16(200)
  time.sleep(0.2)
  buzzer.deinit()

def buzz():
  buzzer.freq(400)
  buzzer.duty_u16(200)
  time.sleep(0.1)
  buzzer.freq(800)
  buzzer.duty_u16(400)
  time.sleep(0.2)
  buzzer.freq(600)
  buzzer.duty_u16(200)
  time.sleep(0.1)
  buzzer.deinit()

buzz()
time.sleep(1)
beep()

def getGND(place):
  p = 0
  if place == 1:
    p = 0
  elif place == 2:
    p = 3
  elif place == 3:
    p = 4
  elif place == 4:
    p = 11
  else:
    return None
  return p

pin1digits = [0, 2, 3, 5, 6, 7, 8, 9]
pin2digits = [0, 4, 5, 6, 8, 9]
pin5digits = [0, 1, 2, 3, 4, 7, 8, 9]
pin6digits = [0, 2, 6, 8]
pin7digits = [0, 2, 3, 5, 6, 8]
pin9digits = [0, 1, 3, 4, 5, 6, 7, 8, 9]
pin10digits = [2, 3, 4, 5, 6, 8, 9]

def display(digit,place):
  gnd = getGND(place)
  pin[gnd].off()
  if (digit == 0 or digit == 2 or digit == 3 or digit == 5 or digit == 6 or digit == 7 or digit == 8 or digit == 9):
    pin[1].on()
  if (digit == 0 or digit == 4 or digit == 5 or digit == 6 or digit == 8 or digit == 9):
    pin[2].on()
  if (digit == 0 or digit == 1 or digit == 2 or digit == 3 or digit == 4 or digit == 7 or digit == 8 or digit == 9):
    pin[5].on()
  if (digit == 0 or digit == 2 or digit == 6 or digit == 8):
    pin[6].on()
  if (digit == 0 or digit == 2 or digit == 3 or digit == 5 or digit == 6 or digit == 8):
    pin[7].on()
  if (digit == 0 or digit == 1 or digit == 3 or digit == 4 or digit == 5 or digit == 6 or digit == 7 or digit == 8 or digit == 9):
    pin[9].on()
  if (digit == 2 or digit == 3 or digit == 4 or digit == 5 or digit == 6 or digit == 8 or digit == 9):
    pin[10].on()
  time.sleep(0.002)
  pin[1].off()
  pin[2].off()
  pin[5].off()
  pin[6].off()
  pin[7].off()
  pin[9].off()
  pin[10].off()  
  pin[gnd].on()

def cleanup():
  for i in [1,2,5,6,7,9,10]:
    pin[i].off()

def cleanupDigitPins():
    pin[0].on()
    pin[3].on()
    pin[4].on()
    pin[11].on()

cleanupDigitPins()

# Countdown time 20 minutes in seconds
countdown = 25 * 60

while countdown > 0:
  #cleanup()
  minutes = countdown // 60
  seconds = countdown % 60

  # format minutes and seconds to 4 digits with leading zeros, for example 8 minutes and 5 seconds will be 0805
  displayString = "{:02d}{:02d}".format(minutes, seconds)
  print(displayString)

  for flicker in range(1,125):
      for displayIndex in range(1, 5):
        digit = int(displayString[displayIndex - 1])
        #print("display ", digit, " at ", displayIndex)
        display(digit, displayIndex)
  #time.sleep(0.5)
  countdown -= 1


time.sleep(5)

# Final shutdown
cleanupDigitPins()
buzzer.deinit()