from pathlib import Path


import xdg_base_dirs


APP_NAME = 'tolino_news'
log_folder = xdg_base_dirs.xdg_state_home() / APP_NAME
log_folder.mkdir(exist_ok=True)
LOG_FP = log_folder / 'log'
exec_fn = 'tolino_news_run'
RUNJOB_FP = Path('/usr', 'local', 'bin', exec_fn)  # created at install
