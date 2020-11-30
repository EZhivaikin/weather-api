from config.configs import APPLICATION_CONFIGS_ROOT
from omegaconf import OmegaConf, DictConfig

from config.settings import Settings, ApiClient


def _load_application_configuration(profile: str) -> DictConfig:
    config_folder = APPLICATION_CONFIGS_ROOT / "profiles" / profile
    config_params = config_folder / "params.yaml"
    return OmegaConf.load(str(config_params))




settings = load_settings("default")
