from distutils.command.config import config
import yaml
from pathlib import Path
from os import environ
import os
from typing import Union


def find_config():
    # find config in
    # $XDG_CONFIG_HOME/genozip_wrapper/config.yaml
    # $HOME/.config/genozip_wrapper/config.yaml
    # /etc/genozip_wrapper/config.yaml
    if environ.get("XDG_CONFIG_HOME") is not None:
        config_path = (
            Path(environ["XDG_CONFIG_HOME"]) / "genozip_wrapper" / "config.yaml"
        )
    else:
        config_path = (
            Path(environ["HOME"]) / ".config" / "genozip_wrapper" / "config.yaml"
        )
    if not config_path.exists():
        config_path = Path("/etc/genozip_wrapper") / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError("Could not find config file")
    return config_path


def read_config(config_path: Union[str, os.PathLike] = None) -> dict:
    if config_path is None:
        config_path = find_config()
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config

def get_genome_path(genome_alias: str, config: dict) -> Path:
    if genome_alias not in config["genomes"]:
        raise KeyError(f"Could not find genome alias {genome_alias}")
    return Path(config["genomes"][genome_alias])