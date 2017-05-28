import requests
import random
import socket
import select
import time


class Setup(object):

    def findAuroras(self):
        """
        Returns a list of the IP addresses of all Auroras found on the network
        
        Discovery will take about 90 seconds.
        """
        SSDP_IP = "239.255.255.250"
        SSDP_PORT = 1900
        SSDP_MX = 3
        SSDP_ST = "nanoleaf_aurora:light"

        req = ['M-SEARCH * HTTP/1.1',
               'HOST: ' + SSDP_IP + ':' + str(SSDP_PORT),
               'MAN: "ssdp:discover"',
               'ST: ' + SSDP_ST,
               'MX: ' + str(SSDP_MX)]
        req = '\r\n'.join(req).encode('utf-8')

        auroraLocations = []
        def checkIfNewAurora(response):
            if not SSDP_ST in response:
                return
            for line in response.split("\n"):
                if "Location:" in line:
                    newLocation = line.replace("Location:", "").strip() \
                                      .replace("http://", "") \
                                      .replace(":16021", "")
                    if not newLocation in auroraLocations:
                        auroraLocations.append(newLocation)
                        print("New Aurora found at " + newLocation)
                    return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, SSDP_MX)
        sock.bind((socket.gethostname(), 9090))
        sock.sendto(req, (SSDP_IP, SSDP_PORT))
        sock.setblocking(False)

        seekTime = 90
        timeout = time.time() + seekTime
        print("Starting discovery. This will continue for " + str(seekTime) + " seconds.")
        while time.time() < timeout:
            try:
                ready = select.select([sock], [], [], 5)
                if ready[0]:
                    response = sock.recv(1024).decode("utf-8")
                    checkIfNewAurora(response)
            except socket.error as err:
                print("Socket error while discovering SSDP devices!")
                print(err)
                print("If you are sure your network connection is working, please post an issue on the GitHub page: https://github.com/software-2/nanoleaf/issues")
                print("Please include as much information as possible, including your OS, how your computer is connected to your network, etc.")
                sock.close()
                break

        if len(auroraLocations) == 0:
            print("Discovery complete, but no Auroras found!")
            return auroraLocations
        print("Discovery complete! Found " + str(len(auroraLocations)) + " Auroras.")
        return auroraLocations

    def generateAuthToken(self, ipAddress):
        '''
        Generates an auth token for the Aurora at the given IP address. 
        
        You must first press and hold the power button on the Aurora for about 5-7 seconds, until the white LED flashes briefly.
        '''
        url = "http://" + ipAddress + ":16021/api/v1/new"
        r = requests.post(url)
        code = r.status_code
        if code == 200:
            print("Auth token for "  + ipAddress + " successfully generated!   " + str(r.json()))
            return r.json()['auth_token']
        if r.status_code == 401:
            print("Not Authorized! I don't even know how this happens. Please post an issue on the GitHub page: https://github.com/software-2/nanoleaf/issues")
        if r.status_code == 403:
            print("Forbidden! Press and hold the power button for 5-7 seconds first! (Light will begin flashing)")
        if r.status_code == 422:
            print("Unprocessable Entity! I'm blaming your network on this one.")
        return None



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