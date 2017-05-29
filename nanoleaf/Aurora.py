import requests
import random

# Primary interface for an Aurora light
# For instructions or bug reports, please visit
# https://github.com/software-2/nanoleaf


class Aurora(object):
    def __init__(self, ip_address: str, auth_token: str):
        self.baseUrl = "http://" + ip_address + ":16021/api/v1/" + auth_token + "/"
        self.ip_address = ip_address
        self.auth_token = auth_token

    def __repr__(self):
        return "<Aurora(" + self.ip_address + ")>"

    def __put(self, endpoint, data: dict) -> requests.request:
        url = self.baseUrl + endpoint
        try:
            r = requests.put(url, json=data)
        except requests.exceptions.RequestException as e:
            print(e)
            return
        return self.__check_for_errors(r)

    def __get(self, endpoint: str = "") -> requests.request:
        url = self.baseUrl + endpoint
        try:
            r = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            return
        return self.__check_for_errors(r)

    def __delete(self, endpoint: str = "") -> requests.request:
        url = self.baseUrl + endpoint
        try:
            r = requests.delete(url)
        except requests.exceptions.RequestException as e:
            print(e)
            return
        return self.__check_for_errors(r)

    def __check_for_errors(self, r: requests.request) -> requests.request:
        if r.status_code == 200:
            if r.text == "": #BUG: Delete User returns 200, not 204 like it should, as of firmware 1.5.0
                return None
            return r.json()
        elif r.status_code == 204:
            return None
        elif r.status_code == 403:
            print("Error 400: Bad request! (" + self.ip_address + ")")
        elif r.status_code == 401:
            print("Error 401: Not authorized! This is an invalid token for this Aurora (" + self.ip_address + ")")
        elif r.status_code == 404:
            print("Error 404: Resource not found! (" + self.ip_address + ")")
        elif r.status_code == 422:
            print("Error 422: Unprocessible Entity (" + self.ip_address + ")")
        elif r.status_code == 500:
            print("Error 500: Internal Server Error (" + self.ip_address + ")")
        else:
            print("ERROR! UNKNOWN ERROR " + str(r.status_code)
                  + ". Please post an issue on the GitHub page: https://github.com/software-2/nanoleaf/issues")
        return None

    ###########################################
    # General functionality methods
    ###########################################

    @property
    def info(self):
        """Returns the full Aurora Info request. 
        
        Useful for debugging since it's just a fat dump."""
        return self.__get()

    @property
    def color_mode(self):
        """Returns the current color mode."""
        return self.__get("state/colorMode")

    def delete_user(self):
        """CAUTION: Revokes your auth token from the device."""
        self.__delete()

    ###########################################
    # On / Off methods
    ###########################################

    @property
    def on(self):
        """Returns True if the device is on, False if it's off"""
        r = self.__get("state/on")
        if r is not None:
            return r["value"]

    @on.setter
    def on(self, value: bool):
        """Turns the device on/off. True = on, False = off"""
        data = {"on": value}
        self.__put("state", data)

    @property
    def off(self):
        """Returns True if the device is off, False if it's on"""
        return not self.on

    @off.setter
    def off(self, value: bool):
        """Turns the device on/off. True = off, False = on"""
        self.on = not value

    def on_toggle(self):
        """Switches the on/off state of the device"""
        self.on = not self.on

    ###########################################
    # Brightness methods
    ###########################################

    @property
    def brightness(self):
        """Returns the brightness of the device (0-100)"""
        r = self.__get("state/brightness")
        return r["value"]

    @brightness.setter
    def brightness(self, level):
        """Sets the brightness to the given level (0-100)"""
        data = {"brightness" : {"value": level}}
        self.__put("state", data)

    @property
    def brightness_min(self):
        """Returns the minimum brightness possible. (This always returns 0)"""
        return self.__get("state/brightness/min")

    @property
    def brightness_max(self):
        """Returns the maximum brightness possible. (This always returns 100)"""
        return self.__get("state/brightness/max")

    def brightness_raise(self, level):
        """Raise the brightness of the device by a relative amount (negative lowers brightness)"""
        data = {"brightness" : {"increment": level}}
        self.__put("state", data)

    def brightness_lower(self, level):
        """Lower the brightness of the device by a relative amount (negative raises brightness)"""
        self.brightness_raise(-level)

    ###########################################
    # Hue methods
    ###########################################

    @property
    def hue(self):
        """Returns the hue of the device (0-360)"""
        r = self.__get("state/hue")
        return r["value"]

    @hue.setter
    def hue(self, level):
        """Sets the hue to the given level (0-360)"""
        data = {"hue" : {"value": level}}
        self.__put("state", data)

    @property
    def hue_min(self):
        """Returns the minimum hue possible. (This always returns 0)"""
        return self.__get("state/hue/min")

    @property
    def hue_max(self):
        """Returns the maximum hue possible. (This always returns 360)"""
        return self.__get("state/hue/max")

    def hue_raise(self, level):
        """Raise the hue of the device by a relative amount (negative lowers hue)"""
        data = {"hue" : {"increment": level}}
        self.__put("state", data)

    def hue_lower(self, level):
        """Lower the hue of the device by a relative amount (negative raises hue)"""
        self.hue_raise(-level)

    ###########################################
    # Saturation methods
    ###########################################

    @property
    def saturation(self):
        """Returns the saturation of the device (0-100)"""
        r = self.__get("state/saturation")
        return r["value"]

    @saturation.setter
    def saturation(self, level):
        """Sets the saturation to the given level (0-100)"""
        data = {"saturation" : {"value": level}}
        self.__put("state", data)

    @property
    def saturation_min(self):
        """Returns the minimum saturation possible. (This always returns 0)"""
        return self.__get("state/saturation/min")

    @property
    def saturation_max(self):
        """Returns the maximum saturation possible. (This always returns 100)"""
        return self.__get("state/saturation/max")

    def saturation_raise(self, level):
        """Raise the saturation of the device by a relative amount (negative lowers saturation)"""
        data = {"saturation" : {"increment": level}}
        self.__put("state", data)

    def saturation_lower(self, level):
        """Lower the saturation of the device by a relative amount (negative raises saturation)"""
        self.saturation_raise(-level)

    ###########################################
    # Color Temperature methods
    ###########################################

    @property
    def color_temperature(self):
        """Returns the color temperature of the device (0-100)"""
        r = self.__get("state/ct")
        return r["value"]

    @color_temperature.setter
    def color_temperature(self, level):
        """Sets the color temperature to the given level (0-100)"""
        data = {"ct" : {"value": level}}
        self.__put("state", data)

    @property
    def color_temperature_min(self):
        """Returns the minimum color temperature possible. (This always returns 1200)"""
        #return self.__get("state/ct/min")
        # BUG: Firmware 1.5.0 returns the wrong value.
        return 1200

    @property
    def color_temperature_max(self):
        """Returns the maximum color temperature possible. (This always returns 6500)"""
        #return self.__get("state/ct/max")
        #BUG: Firmware 1.5.0 returns the wrong value.
        return 6500

    def color_temperature_raise(self, level):
        """Raise the color temperature of the device by a relative amount (negative lowers color temperature)"""
        data = {"ct" : {"increment": level}}
        self.__put("state", data)

    def color_temperature_lower(self, level):
        """Lower the color temperature of the device by a relative amount (negative raises color temperature)"""
        self.color_temperature_raise(-level)

    ###########################################
    # Effect methods
    ###########################################

    @property
    def effect(self):
        """Returns the active effect"""
        return self.__get("effects/select")

    @effect.setter
    def effect(self, effectName):
        """Sets the active effect to the name specified"""
        data = {"select" : effectName}
        self.__put("effects", data)

    @property
    def effects_list(self):
        """Returns a list of all effects stored on the device"""
        return self.__get("effects/effectsList")

    def effect_random(self):
        """Sets the active effect to a new random effect stored on the device"""
        effect_list = self.effects_list
        active_effect = self.effect
        if active_effect != "*Solid*":
            effect_list.remove(self.effect)
        self.effect = random.choice(effect_list)