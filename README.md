# EtekCity

A python written class/custom component for interfacing with EtekCity devices. Currently under development but the switches component is functional.

If installing into Home Assistant:

1.)Add the contained files into: `../home-assistant/custom_components/etekcity`
   
2.) Add the following to your `configuration.yaml` file, replacing EMAIL_HERE and PASSWORD_HERE with your VeSync credentials:

```yaml
switch:
  - platform: etekcity
    email: EMAIL_HERE
    password: PASSWORD_HERE
```

Doing so, the class with query your EvSync account for registered switches and add them to your Home Assistant.
