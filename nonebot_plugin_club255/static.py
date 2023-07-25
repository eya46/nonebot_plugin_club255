from pathlib import Path

from nonebot_plugin_datastore import get_plugin_data

PLUGIN_NAME = "club255"

Meta = get_plugin_data(PLUGIN_NAME)

Model = Meta.Model

CachePath: Path = Meta.cache_dir
ConfigPath: Path = Meta.config_dir
DataPath: Path = Meta.data_dir
