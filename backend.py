import os
import re
import platform
import json
import requests
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtGui import QDesktopServices

from download_thread import DownloadThread


class Backend(QObject):
    """
    Handles the core application logic, such as finding game folders,
    fetching mod lists, and managing installations.
    Communicates with the frontend (JavaScript) via signals.
    """
    # Signals to communicate with JavaScript
    update_progress = pyqtSignal(str, int)
    install_complete = pyqtSignal(str)
    uninstall_complete = pyqtSignal(str)
    download_error = pyqtSignal(str)
    textures_found = pyqtSignal(str)
    textures_not_found = pyqtSignal()
    installed_mods_checked = pyqtSignal(list)
    mod_list_fetched = pyqtSignal(str)  # Signal to send fetched mod list

    def __init__(self):
        super().__init__()
        self._ball_textures_path = None
        self._boost_meter_textures_path = None
        self._decal_textures_path = None
        self._banner_textures_path = None
        self._border_textures_path = None
        self.installed_mods_file = "installed_mods.json"

    @property
    def ball_textures_path(self):
        if self._ball_textures_path is None:
            print("--- LAZY LOAD: First request for BallTextures path, searching now...")
            self._ball_textures_path = self.find_texture_folder("BallTextures")
        return self._ball_textures_path

    @property
    def boost_meter_textures_path(self):
        if self._boost_meter_textures_path is None:
            print("--- LAZY LOAD: First request for BoostMeterTextures path, searching now...")
            self._boost_meter_textures_path = self.find_texture_folder("BoostMeterTextures")
        return self._boost_meter_textures_path

    @property
    def decal_textures_path(self):
        if self._decal_textures_path is None:
            print("--- LAZY LOAD: First request for DecalTextures path, searching now...")
            self._decal_textures_path = self.find_texture_folder("DecalTextures")
        return self._decal_textures_path

    @property
    def banner_textures_path(self):
        if self._banner_textures_path is None:
            print("--- LAZY LOAD: First request for BannerTextures path, searching now...")
            self._banner_textures_path = self.find_texture_folder("BannerTextures")
        return self._banner_textures_path

    @property
    def border_textures_path(self):
        if self._border_textures_path is None:
            print("--- LAZY LOAD: First request for BorderTextures path, searching now...")
            self._border_textures_path = self.find_texture_folder("BorderTextures")
        return self._border_textures_path

    def load_installed_mods(self):
        if os.path.exists(self.installed_mods_file):
            try:
                with open(self.installed_mods_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}  # Return empty dict if JSON is corrupted
        return {}

    def save_installed_mods(self, data):
        with open(self.installed_mods_file, 'w') as f:
            json.dump(data, f, indent=4)

    def find_texture_folder(self, folder_name):
        """
        Locates a specific texture folder within the BakkesMod data directory.
        (e.g., "BallTextures" or "BoostMeterTextures")
        """
        if platform.system() != "Windows":
            return None

        path_found = None
        try:
            appdata_path = os.getenv('APPDATA')
            if appdata_path:
                potential_path = os.path.join(appdata_path, 'bakkesmod', 'bakkesmod', 'data', 'acplugin',
                                              folder_name)
                if os.path.isdir(potential_path):
                    path_found = potential_path
        except Exception:
            pass

        if not path_found:
            steam_path = ''
            for path in ['C:\\Program Files (x86)\\Steam', 'C:\\Program Files\\Steam']:
                if os.path.isdir(path):
                    steam_path = path
                    break

            if steam_path:
                library_vdf_path = os.path.join(steam_path, 'steamapps', 'libraryfolders.vdf')
                if os.path.isfile(library_vdf_path):
                    all_library_paths = [os.path.join(steam_path, 'steamapps')]
                    try:
                        with open(library_vdf_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            path_matches = re.findall(r'"path"\s+"([^"]+)"', content)
                            all_library_paths.extend([p.replace('\\\\', '\\') for p in path_matches])
                    except Exception:
                        pass

                    for library_path in all_library_paths:
                        steamapps_folder = os.path.join(library_path,
                                                        'steamapps') if "steamapps" not in library_path else library_path
                        potential_path = os.path.join(steamapps_folder, 'common', 'Rocket League', 'bakkesmod', 'data',
                                                      'acplugin', folder_name)
                        if os.path.isdir(potential_path):
                            path_found = potential_path
                            break

        return path_found

    @pyqtSlot(str)
    def open_link(self, url):
        """
        Opens a URL in the user's default web browser.
        """
        print(f"--- DEBUG: Opening external link: {url}")
        QDesktopServices.openUrl(QUrl(url))

    @pyqtSlot()
    def fetch_mod_list(self):
        """
        Fetches the list of mods from a remote JSON file.
        """
        url = "https://raw.githubusercontent.com/Kakapo-Labs/AlphaLoader/refs/heads/main/ballsList.json"
        print(f"--- DEBUG: Fetching mod list from: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            print("--- DEBUG: Successfully fetched mod list.")
            self.mod_list_fetched.emit(response.text)
        except requests.exceptions.RequestException as e:
            print(f"--- DEBUG: ERROR fetching mod list: {e}")
            self.download_error.emit("Could not fetch mod list. Check connection.")
            self.mod_list_fetched.emit("[]")  # Emit empty list on error

    @pyqtSlot()
    def check_textures_folder(self):
        # Check if at least one of the primary folders exists
        if (self.ball_textures_path or
            self.boost_meter_textures_path or
            self.decal_textures_path or
            self.banner_textures_path or
            self.border_textures_path):
            self.textures_found.emit("Required texture folders found.")
        else:
            self.textures_not_found.emit()

    @pyqtSlot()
    def check_installed_mods(self):
        installed = self.load_installed_mods()
        self.installed_mods_checked.emit(list(installed.keys()))

    @pyqtSlot(str, str, str, str, str)
    def start_download(self, url, name, mod_id, category, file_type="zip"):
        """
        Start download, selecting the destination based on the mod's category.
        """
        destination_folder = None
        if category == "boost-meter":
            destination_folder = self.boost_meter_textures_path
        elif category == "decals":
            destination_folder = self.decal_textures_path
        # --- START OF MODIFICATION ---
        elif category == "banner":
            destination_folder = self.banner_textures_path
        # --- END OF MODIFICATION ---
        elif category == "profile-borders":
            destination_folder = self.border_textures_path
        else:
            # Default to BallTextures for "balls" and any other category
            destination_folder = self.ball_textures_path

        if not destination_folder:
            self.download_error.emit(f"Could not find the texture folder for '{category}'.")
            return

        self.download_thread = DownloadThread(url, destination_folder, name, mod_id, category, file_type, self)
        self.download_thread.progress_updated.connect(self.update_progress.emit)
        self.download_thread.install_complete.connect(self.install_complete.emit)
        self.download_thread.download_error.connect(self.download_error.emit)
        self.download_thread.start()

    @pyqtSlot(str, str)
    def uninstall_mod(self, mod_id, category):
        """
        Uninstalls a mod by removing its files from the correct folder.
        """
        installed_mods = self.load_installed_mods()
        if mod_id in installed_mods:

            base_path = None
            if category == "boost-meter":
                base_path = self.boost_meter_textures_path
            elif category == "decals":
                base_path = self.decal_textures_path
            # --- START OF MODIFICATION ---
            elif category == "banner":
                base_path = self.banner_textures_path
            # --- END OF MODIFICATION ---
            elif category == "profile-borders":
                base_path = self.border_textures_path
            else:
                base_path = self.ball_textures_path

            if not base_path:
                print(f"Cannot uninstall, texture folder for '{category}' not found.")
                return

            paths_to_remove = installed_mods[mod_id]
            all_dirs = set()

            # 1. Remove all files and collect their parent directories
            for rel_path in paths_to_remove:
                full_path = os.path.join(base_path, rel_path)

                if os.path.isfile(full_path):
                    try:
                        os.remove(full_path)
                        parent_dir = os.path.dirname(full_path)
                        if parent_dir != base_path:
                            all_dirs.add(parent_dir)
                    except OSError as e:
                        print(f"Could not remove file {full_path}: {e}")
                elif os.path.isdir(full_path):
                    all_dirs.add(full_path)

            # 2. Remove directories, longest path first to handle nested folders
            for dir_path in sorted(list(all_dirs), key=len, reverse=True):
                try:
                    os.rmdir(dir_path)
                except OSError:
                    pass

            # Update the record of installed mods
            del installed_mods[mod_id]
            self.save_installed_mods(installed_mods)
            self.uninstall_complete.emit(mod_id)