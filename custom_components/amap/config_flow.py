"""高德地图组件的配置流。"""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_API_KEY

from .const import DOMAIN, DEFAULT_NAME

class AmapConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理高德地图配置流。"""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """处理用户输入的配置。"""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=DEFAULT_NAME,
                data={
                    CONF_API_KEY: user_input[CONF_API_KEY],
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str,
            }),
            errors=errors,
        ) 