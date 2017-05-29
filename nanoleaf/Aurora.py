import requests
import random
import socket
import select
import time

# Primary interface for an Aurora light
# For instructions or bug reports, please visit
# https://github.com/software-2/nanoleaf

class Aurora(object):
    def __init__(self, ipAddress, authToken):
        self.baseUrl = "http://" + ipAddress + ":16021/api/v1/" + authToken + "/"
        self.ipAddress = ipAddress
        self.authToken = authToken

    def __repr__(self):
        return "<Aurora(" + self.ipAddress + ")>"

    def __put(self, endpoint, data):
        url = self.baseUrl + endpoint
        try:
            return requests.put(url, json = data)
        except requests.exceptions.RequestException as e:
            print(e)
            return

    def __get(self, endpoint=None):
        url = self.baseUrl
        if (endpoint is not None):
            url = self.baseUrl + endpoint
        try:
            return requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            return

    def getInfo(self):
        """Returns the full Aurora Info request. 
        
        Useful for debugging since it's just a fat dump."""
        r = self.__get()
        print(r.text)
        return r.json()



    def getOn(self):
        """Returns True if the device is on, False if it's off"""
        r = self.__get("state/on")
        return r.json()["value"]
    def on(self, value=True):
        """Turns on the device. Optional param to turn off if you hate using the off function"""
        data = {"on": value}
        self.__put("state", data)
    def off(self):
        """Turns off the device"""
        data = {"on": False}
        self.__put("state", data)
    def toggleOn(self):
        """Switches the on/off state of the device"""
        self.on(not self.getOn())



    def getBrightness(self):
        """Returns the brightness of the device (0-100)"""
        r = self.__get("state/brightness")
        return r.json()["value"]
    def getMaxBrightness(self):
        """Returns the maximum brightness possible.
        
        No, I don't really know why..."""
        r = self.__get("state/brightness")
        return r.json()["max"]
    def getMinBrightness(self):
        """Returns the minimum brightness possible."""
        r = self.__get("state/brightness")
        return r.json()["min"]
    def brightness(self, level):
        """Sets the brightness to the given level (0-100)"""
        data = {"brightness" : {"value": level}}
        self.__put("state/brightness", data)
    def brightnessRaise(self, level):
        """Raise the brightness of the device by a relative amount (negative lowers brightness)"""
        data = {"brightness" : {"increment": level}}
        self.__put("state/brightness", data)
    def brightnessLower(self, level):
        """Lower the brightness of the device by a relative amount (negative raises brightness)"""
        self.brightnessRaise(-level)



    def getEffect(self):
        """Returns the active effect"""
        r = self.__get("effects/select")
        return r.json()
    def getEffects(self):
        """Returns a list of all effects stored on the device"""
        r = self.__get("effects/effectsList")
        return r.json()
    def effect(self, effectName):
        """Sets the active effect to the name specifiec"""
        data = {"select" : effectName}
        self.__put("effects", data)
    def effectRandom(self):
        """Sets the active effect to a new random effect stored on the device"""
        effectList = self.getEffects()
        effectList.remove(self.getEffect())
        self.effect(random.choice(effectList))