"""
Home Assistant的高德地图集成组件。
"""
import logging
import voluptuous as vol
import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

# 配置schema
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_API_KEY): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict):
    """设置高德地图组件。"""
    if DOMAIN not in config:
        return True

    hass.data[DOMAIN] = {}
    
    # 获取配置信息
    conf = config[DOMAIN]
    api_key = conf[CONF_API_KEY]
    
    # 创建API客户端会话
    session = async_get_clientsession(hass)
    
    # 初始化API处理类
    api = AmapApi(hass, api_key, session)
    hass.data[DOMAIN]["api"] = api

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """从配置入口设置高德地图组件。"""
    hass.data.setdefault(DOMAIN, {})
    
    # 创建API客户端会话
    session = async_get_clientsession(hass)
    
    # 初始化API处理类
    api = AmapApi(hass, entry.data[CONF_API_KEY], session)
    hass.data[DOMAIN]["api"] = api
    
    # 设置平台
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """卸载配置入口。"""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok

class AmapApi:
    """高德地图API封装类。"""
    
    def __init__(self, hass: HomeAssistant, api_key: str, session: aiohttp.ClientSession):
        """初始化高德地图API。"""
        self.hass = hass
        self.api_key = api_key
        self.session = session
        self.base_url = "https://restapi.amap.com/v3"

    async def async_get_location(self, address: str):
        """地理编码服务。"""
        try:
            url = f"{self.base_url}/geocode/geo"
            params = {
                "key": self.api_key,
                "address": address,
                "output": "JSON"
            }
            
            async with async_timeout.timeout(10):
                async with self.session.get(url, params=params) as response:
                    return await response.json()
                    
        except Exception as err:
            _LOGGER.error("获取位置信息失败: %s", err)
            return None 