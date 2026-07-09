import importlib.resources as res
from typing import Any, ClassVar

from dynaconf import Dynaconf, Validator, loaders

PACKAGE_ROOT = res.files("swcapi")
PROJECT_ROOT = PACKAGE_ROOT.parent
CONFIG_ROOT = PROJECT_ROOT / "config"


class Config(Dynaconf):
    # Mapping of configuration filenames to the list of setting attributes that are
    # allowed to be updated and persisted back to those files.
    # Format: {"filename.toml": ["attribute_1", "attribute_2"]}
    updatable: ClassVar = {".secrets.toml": ["apikey"], "settings.toml": ["test", "foo"]}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Intercepts setting assignments (e.g., config.apikey = "new_value").

        1. Updates the setting attribute in memory via Dynaconf's parent handler.
        2. Checks if the setting name exists in the `updatable` dictionary.
        3. If a match is found, persists the updated setting to the mapped configuration file.

        :param name: The name of the setting attribute being updated.
        :param value: The new value to set.
        """
        super().__setattr__(name, value)

        target_file = None
        for file_path, settings_list in self.updatable.items():
            if name in settings_list:
                target_file = file_path
                break

        if target_file:
            self._write_config(target_file, name, value)

    def _write_config(self, file_name: str, name: str, value: Any) -> None:
        """
        Persists a single setting update back to the specified configuration file on disk.

        Uses Dynaconf's native `loaders.write` to merge the updated setting value
        into the TOML file at `ROOT_PATH_FOR_DYNACONF / file_name`.

        :param file_name: The name of the target configuration file.
        :param name: The setting key to update.
        :param value: The new value for the setting.
        """
        if not getattr(self, "SETTINGS_FILE_FOR_DYNACONF", []) or getattr(self, "ROOT_PATH_FOR_DYNACONF") is None:
            print("ERROR: Dynaconf environment variables not set. Cannot write config.")
            return
        # Store the updated value in the according config file
        file = self.ROOT_PATH_FOR_DYNACONF / file_name
        loaders.write(str(file), {name: value}, merge=True)


settings = Config(
    root_path=CONFIG_ROOT,
    load_dotenv=True,
    merge_enabled=True,
    envvar_prefix="",
    settings_files=[".secrets.toml", "settings.toml"],
)
