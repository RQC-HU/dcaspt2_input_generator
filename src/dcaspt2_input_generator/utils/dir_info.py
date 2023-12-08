from pathlib import Path


class DirInfo:
    def __init__(self):
        self.user_current_dir = Path.cwd()
        self.app_rootdir = Path(__file__).parent.parent.expanduser().resolve()  # src/dcaspt2_input_generator
        self.setting_file_path = (self.app_rootdir / "settings.json").resolve()
        self.sum_dirac_dfcoef_path = (self.app_rootdir / "sum_dirac_dfcoef.out").resolve()


dir_info = DirInfo()
