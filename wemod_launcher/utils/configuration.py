import logging
from typing import Any, Optional
from tomllib import load
from pathlib import Path
from xdg.BaseDirectory import save_config_path
from .logger import LoggingHandler


class Configuration(object):
    def __init__(self, cfg_path: str = save_config_path("wemod-launcher")):
        # Initialize logger for Config.
        self.__log = LoggingHandler(module_name=__name__).get_logger()

        path = Path(cfg_path)
        if not path.exists():
            logging.debug("Configuration path does not exist, creating.")
            path.mkdir()

        cfg_file = path / "config.toml"

        if not cfg_file.exists():
            # TODO: Add support to write dummy config.
            cfg_file.write_text("### WIP ###")

        self.__cfg_path = cfg_file

        self.__config = load(open(str(cfg_file), "rb"))

    def get_key(self, keys: list[str]) -> Optional[Any]:
        try:
            config = self.__config
            for key in keys:
                config = config[key]

            return config
        except KeyError:
            self.__log.debug(
                "Unable to get configuration entry, returning None"
            )
            self.__log.debug(f"Key: {keys}, config path: {self.__cfg_path}")
            return None
