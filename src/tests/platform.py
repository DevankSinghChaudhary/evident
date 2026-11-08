from platformdirs import PlatformDirs

dirs = PlatformDirs(appname="evident", appauthor=False)

print(dirs.user_config_dir)
print(dirs.user_cache_dir)
print(dirs.user_data_dir)
