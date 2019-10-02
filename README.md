# EtekCity

A python written class/custom component for interfacing with EtekCity devices. Currently under development but the switches component is functional.

If installing into Home Assistant:

1.)Add the contained files into: `../home-assistant/custom_components/etekcity`

2.) For ESWD16 Dimmer Switches, add the following to your `configuration.yaml` file, replacing EMAIL_HERE and PASSWORD_HERE with VeSync credentials. Here you also specify states for the RGB light:

      1.) on
      2.) off
      3.) light
      4.) opp_light
      
*** Note, if the switch is physically triggered it can take up to 30 seconds for the RGB light to get back in sync ****


Here is a sample config:
      
```yaml
light:
  - platform: etekcity
    email: "EMAIL_HERE"
    password: "PASSWORD_HERE"
    rgb_state: "on"
    rgb_red: 0
    rgb_green: 0
    rgb_blue: 255
```
      
2.a) Alternately although more barebones, you can specify this as switch. Add the following to your `configuration.yaml` file, replacing EMAIL_HERE and PASSWORD_HERE with your VeSync credentials:

```yaml
switch:
  - platform: etekcity
    email: "EMAIL_HERE"
    password: "PASSWORD_HERE"
```

Doing so, the class with query your EvSync account for registered switches and add them to your Home Assistant.
