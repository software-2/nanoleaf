# Python interface for Nanoleaf Aurora #

A Python module for the coolest lights with the worst software support.

This module aims to do more than just act as a wrapper for API calls. It provides several convenience functions to perform more complicated and robust actions than are possible in some of the other Aurora wrappers I've seen. For instance, being able to switch to a random new effect, or toggle the on/off state with a single command.

This is a pet project, and I'm doing it because I need API support just as badly as you do. But, if it really does make your life better, I'd appreciate a cup of coffee.
```Donate
BTC: 1Gr31rgb6UXEdXwbwQGUsadcd7AnY7okXT
LTC: Lajqnm28UipLbzJqvyy4tRQFf39xQy6B48
```

## Setup ##

You will need to retrieve an API token from your Aurora. I haven't added support for this here yet, so unfortunately you'll still need to do this manually. It's a simple rest call you can make in postman. (Or you can wait for me to get around to adding this - I have more Auroras I haven't setup yet, so it's still a priority for me.)

The Aurora broadcasts its information via SSDP once every minute. The contents of the broadcast are [documented on Nanoleaf's website](http://forum.nanoleaf.me/docs/openapi#_pviffjmne4te). I used wireshark to listen for it. Once you have the location ip (which is a different ip than what your router is giving it) write it down for later use.

```rest
POST http://<location_ip>/api/v1/new
```

## Examples ##

### Turn on and set to an effect ###

```python
from nanoleaf import Aurora

myAurora = Aurora("169.254.123.123", "5EvbR2FjfmYfAkEtOkEnolnZbe6qOB")
myAurura.on()
myAurora.effect("Violets Are Blue")
```

### Set multiple Auroras to the same random effect ###

```python
leftSide = Aurora("169.254.123.123", "5EvbR2FjfmYfAkEtOkEnolnZbe6qOB")
rightSide = Aurora("169.254.100.100", "fAkeR2FjfmYfAkEtOkEnolnZtOkEn")
leftSide.on()
rightSide.on()
rightSide.effectRandom()
leftSide.effect(rightSide.getEffect())
```