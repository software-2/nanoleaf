# Python interface for Nanoleaf Aurora #

A Python module for the coolest lights with the worst software support.

This module aims to do more than just act as a wrapper for API calls. It provides several convenience functions to perform more complicated and robust actions than are possible in some of the other Aurora wrappers I've seen. For instance, being able to switch to a random new effect, or toggle the on/off state with a single command.


### Support The Project ###

This is a pet project, and I'm doing it because I need API support just as badly as you do. But, if it really does make your life better, I'd appreciate a cup of coffee.
```
BTC: 1Gr31rgb6UXEdXwbwQGUsadcd7AnY7okXT
LTC: Lajqnm28UipLbzJqvyy4tRQFf39xQy6B48
```

## Install ##

It's super easy - just use pip to get the latest version.

```
pip install nanoleaf --upgrade
```

## Setup ##

There are two pieces of information you'll need to control your Aurora: The IP address and an auth token.

### Finding IP Address ###

For most people, the IP address that the Aurora uses to communicate is the one assigned by your router, but this might not necessarily be true depending on your network setup. Either way, you can get this by using the setup class.
After about 90 seconds, this will return a list of the IP address of every Aurora found on the network.

```python
from nanoleaf import setup

ipAddressList = setup.find_auroras()
```

### Generate Auth Token ###

To generate an auth token, you must first press and hold the power button on the Aurora for about 5-7 seconds, until the white LED flashes briefly. Then, call the Setup class like so:

```python
from nanoleaf import setup

token = setup.generate_auth_token("192.168.1.129")
```

Be sure to store this auth token somewhere for future use. If you lose this token, you'll have to generate another. Personally, I just keep it in the scripts I've written that call this library. 

## Examples ##

### Turn on and set to an effect ###

```python
from nanoleaf import Aurora

my_aurora = Aurora("169.254.123.123", "5EvbR2FjfmYfAkEtOkEnolnZbe6qOB")
my_aurora.on = True
my_aurora.effect = "Violets Are Blue"
```

### Set multiple Auroras to the same random effect ###

```python
left_side = Aurora("192.168.1.56", "5EvbR2FjfmYfAkEtOkEnolnZbe6qOB")
right_side = Aurora("192.168.1.78", "fAkeR2FjfmYfAkEtOkEnolnZtOkEn")
left_side.effect = right_side.effect_random()
```

### Add a new effect ###

Presently, you must create your own raw dict that exactly matches the structure found on the [API documentation](http://forum.nanoleaf.me/docs/openapi#_e5qyi8m8u68). Methods of making this much easier are planned for future updates.

``` python
effect_data = {
    "command": "add",
    "animName": "My Random Animation",
    "animType": "random",
    "colorType": "HSB",
    "animData": None,
    "palette": [
        {
            "hue": 0,
            "saturation": 100,
            "brightness": 100
        },
        {
            "hue": 120,
            "saturation": 100,
            "brightness": 100
        },
        {
            "hue": 240,
            "saturation": 100,
            "brightness": 100
        }
    ],
    "brightnessRange": {
        "minValue": 25,
        "maxValue": 100
    },
    "transTime": {
        "minValue": 25,
        "maxValue": 100
    },
    "delayTime": {
        "minValue": 25,
        "maxValue": 100
    },
    "loop": True
}

my_aurora.effect_set_raw(effect_data)
```

### Delete an effect ###

``` python
my_aurora.effect_delete("My Random Animation")
```
