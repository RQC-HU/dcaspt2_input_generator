import os


class DirInfo:
    def __init__(self):
        self.user_current_dir = os.getcwd()
        self.app_rootdir = os.path.join(os.path.dirname((os.path.abspath(__file__))), "..")
        self.setting_file_path = os.path.abspath(os.path.join(self.app_rootdir, "settings.json"))
        self.sum_dirac_dfcoef_path = os.path.join(self.app_rootdir, "sum_dirac_dfcoef.out")


dir_info = DirInfo()
