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
from nanoleaf import Setup

ipAddressList = Setup.find_auroras()
```

### Generate Auth Token ###

To generate an auth token, you must first press and hold the power button on the Aurora for about 5-7 seconds, until the white LED flashes briefly. Then, call the Setup class like so:

```python
from nanoleaf import Setup

token = Setup.generate_auth_token("192.168.1.129")
```

Be sure to store this auth token somewhere for future use. If you lose this token, you'll have to generate another. Personally, I just keep it in the scripts I've written that call this library. 

## Examples ##

### Turn on and set to an effect ###

```python
from nanoleaf import Aurora

myAurora = Aurora("169.254.123.123", "5EvbR2FjfmYfAkEtOkEnolnZbe6qOB")
myAurora.on()
myAurora.effect("Violets Are Blue")
```

### Set multiple Auroras to the same random effect ###

```python
leftSide = Aurora("192.168.1.56", "5EvbR2FjfmYfAkEtOkEnolnZbe6qOB")
rightSide = Aurora("192.168.1.78", "fAkeR2FjfmYfAkEtOkEnolnZtOkEn")
leftSide.on()
rightSide.on()
rightSide.effectRandom()
leftSide.effect(rightSide.getEffect())
```