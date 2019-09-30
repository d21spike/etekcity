from .required.etekcity import EtekCity
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import homeassistant.util.color as color_util
from homeassistant.components.light import (
    Light,
    PLATFORM_SCHEMA,
    ATTR_BRIGHTNESS,
    SUPPORT_BRIGHTNESS,
)

_LOGGER = logging.getLogger(__name__)

CONF_DOMAIN = "etekcity"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"
CONF_RGB_STATE = "rgb_state"
CONF_RGB_RED = "rgb_red"
CONF_RGB_GREEN = "rgb_green"
CONF_RGB_BLUE = "rgb_blue"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_RGB_STATE): cv.string,
    vol.Required(CONF_RGB_RED): cv.string,
    vol.Required(CONF_RGB_GREEN): cv.string,
    vol.Required(CONF_RGB_BLUE): cv.string,
})

SUPPORT_ETEKCITY_SWITCHLIGHT = (SUPPORT_BRIGHTNESS)


def setup_platform(hass, config, add_entities, discovery_info=None):

    email = config[CONF_EMAIL]
    password = config[CONF_PASSWORD]
    devices = []

    etek = EtekCity(email, password)
    if not etek.login():
        _LOGGER.error("Could not connect to VeSync")
        return

    for device_num in etek.devices:
        if etek.devices[device_num].Device_Type == "ESWD16":
            devices.append(EtekSwitchLight(hass, config, etek.devices[device_num]))

    if len(devices):
        add_entities(devices)
    else:
        _LOGGER.error("Could not locate any EtekCity switches")


class EtekSwitchLight(Light):

    def __init__(self, hass, config, light):
        _LOGGER.info("Initializing EtekSwitchLight %s" % light.Name)

        self._hass = hass
        self._name = light.Name
        self._state = False
        if light.Status == "on": self._state = True
        self._rgb_state = False
        if light.RGB_Status == "on": self._rgb_state = True
        self._rgb_color = (light.RGB_Red, light.RGB_Green, light.RGB_Blue)
        self._brightness = light.Brightness
        self.light = light
        self.config = config

        color = (int(config[CONF_RGB_RED]), int(config[CONF_RGB_GREEN]), int(config[CONF_RGB_BLUE]))
        if config[CONF_RGB_STATE] == "on":
            self.light.set_rgb("on", color[0], color[1], color[2])
        elif config[CONF_RGB_STATE] == "off":
            self._rgb("off")
        elif config[CONF_RGB_STATE] == "light":
            self.light.set_rgb(self.light.Status, color[0], color[1], color[2])
        elif config[CONF_RGB_STATE] == "opp_light":
            if self.light.Status == "on":
                state = "off"
            else:
                state = "on"
            self.light.set_rgb(state, color[0], color[1], color[2])


    def _light(self, state):
        _LOGGER.info("Toggling EtekSwitchLight %s to state %s" % (self._name, state))
        self.light.set_status(state)

        if self.config[CONF_RGB_STATE] == "light":
            self._rgb(state)
        elif self.config[CONF_RGB_STATE] == "opp_light":
            if state == "on":
                self._rgb("off")
            else:
                self._rgb("on")

        if self.light.Status == state:
            return True


    def _rgb(self, state):
        _LOGGER.info("Toggling EtekSwitchLight RGB %s to state %s" % (self._name, state))
        self.light.set_rgb_status(state)
        if self.light.RGB_Status == state:
            return True


    def _rgb_color(self, color):
        _LOGGER.info("Toggling EtekSwitchLight RGB %s to color (%i, %i, %i)" % (self._name, color[0], color[1], color[2]))
        self.light.set_rgb_color(color[0], color[1], color[2])
        if self.light.RGB_Red == color[0] and self.light.RGB_Green == color[1] and self.light.RGB_Blue == color[2]:
            return True


    def _set_brightness(self, brightness):
        _LOGGER.info("Setting EtekSwitchLight %s to brightness %i" % (self._name, brightness))
        self.light.set_brightness(brightness)
        self._brightness = brightness


    def _query_state(self):
        _LOGGER.info("Querying state for EtekSwitchLight %s" % self._name)
        self.light.device_info()
        self._brightness = self.light.Brightness

        if self.config[CONF_RGB_STATE] == "light":
            self._rgb(self.light.Status)
        elif self.config[CONF_RGB_STATE] == "opp_light":
            if self.light.Status == "on":
                self._rgb("off")
            else:
                self._rgb("on")

        if self.light.Status == "on": return True


    def _query_rgb_state(self):
        _LOGGER.info("Querying state for EtekSwitchLight RGB %s" % self._name)
        self.light.device_info()
        self._brightness = self.light.Brightness
        if self.light.RGB_Status == "on": return True


    @property
    def supported_features(self):
        return SUPPORT_ETEKCITY_SWITCHLIGHT


    @property
    def should_poll(self):
        """ Return the polling state """
        return True


    @property
    def name(self):
        """ Return the name of the light """
        return self._name


    @property
    def brightness(self):
        """ Return the birghtness of the light """
        return int(round((self._brightness / 100) * 255))


    @property
    def is_on(self):
        """ Return if the light is on """
        return self._state


    @property
    def is_rgb_on(self):
        """ Return if the rgb light is on """
        return self._rgb_state


    @property
    def rgb_color(self):
        """ Return the rgb color """
        return self._rgb_color


    def update(self):
        """ Update device state """
        self._state = self._query_state()


    def turn_on(self, **kwargs):
        _LOGGER.info("Turning on EtekSwitchLight %s" % kwargs)
        """ Turn on switch """

        if "brightness" in kwargs:
            brightness = int(round((kwargs['brightness'] / 255) * 100))
            self._set_brightness(brightness)

        if self._light("on"): self._state = True


    def turn_off(self, **kwargs):
        """ Turn off switch Light """
        if self._light("off"): self._state = False


    def turn_on_rgb(self, **kwargs):
        _LOGGER.info("Turning on EtekSwitchLight RGB %s" % kwargs)
        """ Turn on RGB """

        if self._rgb("on"): self._rgb_state = True


    def turn_off_rgb(self, **kwargs):
        """ Turn off RGB """
        if self._rgb("off"): self._rgb_state = False
