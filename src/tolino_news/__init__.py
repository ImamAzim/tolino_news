from pathlib import Path


import xdg_base_dirs


APP_NAME = 'tolino_news'

log_folder = xdg_base_dirs.xdg_state_home() / APP_NAME
log_folder.mkdir(parents=True, exist_ok=True)
LOG_FP = log_folder / 'log'
LOG_TOKEN = log_folder / 'token_updater'

exec_fn = 'tolino_news_run'  # must match script in pyproject
RUNJOB_FP = Path('/usr', 'local', 'bin', exec_fn)  # created at install
exec_fn = 'token_update'
TOKEN_UPDATE_RUNJOB_FP = Path(
'/usr', 'local', 'bin', exec_fn)  # created at install


DATA_FOLDER = xdg_base_dirs.xdg_data_home() / APP_NAME
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

cache_folder = xdg_base_dirs.xdg_cache_home() / APP_NAME
cache_folder.mkdir(parents=True, exist_ok=True)

PLUGIN_FP = Path(__file__).parent / 'plugins' / 'EpubMerge.zip'
