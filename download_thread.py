import os
import io
import zipfile
import json
import requests
import re
from PyQt5.QtCore import QThread, pyqtSignal

# --- MODIFICATION: Added 'unidecode' for character transliteration ---
# This library is excellent for converting non-English characters to ASCII.
# The user will need to install it by running: pip install unidecode
try:
    from unidecode import unidecode

    UNIDECODE_AVAILABLE = True
except ImportError:
    UNIDECODE_AVAILABLE = False

try:
    from PIL import Image

    PILLOW_SUPPORT = True
except ImportError:
    PILLOW_SUPPORT = False

from utils import RAR_SUPPORT, RAR_TOOL_AVAILABLE

if RAR_SUPPORT:
    import rarfile


# --- MODIFICATION: New function to sanitize file and folder names ---
def sanitize_filepath(path):
    """
    Sanitizes a full file path by cleaning each component (directory or filename).
    Converts non-English characters to their closest English equivalent.
    """
    if not UNIDECODE_AVAILABLE:
        print(
            "--- SANITIZE WARNING: 'unidecode' not found. Using basic sanitization. Run 'pip install unidecode' for better results.")

    # Normalize path separators for consistent processing
    path = path.replace('\\', '/')

    parts = path.split('/')
    sanitized_parts = []

    for part in parts:
        if not part:
            continue

        sanitized_part = part
        if UNIDECODE_AVAILABLE:
            # Transliterate Unicode to ASCII (e.g., 'é' -> 'e', '你好' -> 'Ni Hao')
            sanitized_part = unidecode(sanitized_part)

        # --- MODIFICATION: Preserve spaces in filenames by removing '\s' from the regex ---
        # This will still replace other illegal characters with an underscore.
        sanitized_part = re.sub(r'[<>:"/\\|?*]+', '_', sanitized_part)

        # A final strict filter to keep only standard characters
        sanitized_part = re.sub(r'[^\w._\s-]', '', sanitized_part)

        if sanitized_part:
            sanitized_parts.append(sanitized_part)

    # Rejoin the parts into a path appropriate for the current OS,
    # or return an empty string if the path was fully sanitized away.
    return os.path.join(*sanitized_parts) if sanitized_parts else ""


class DownloadThread(QThread):
    """
    Manages the download and extraction of mod files in a separate thread
    to prevent the UI from freezing.
    """
    progress_updated = pyqtSignal(str, int)
    install_complete = pyqtSignal(str)
    download_error = pyqtSignal(str)

    # --- MODIFICATION: Added 'category' to the constructor ---
    def __init__(self, url, destination_folder, name, mod_id, category, file_type, backend, parent=None):
        super().__init__(parent)
        self.url = url
        self.destination_folder = destination_folder
        self.name = name
        self.mod_id = mod_id
        self.category = category  # Store the category for later use
        self.file_type = file_type
        self.backend = backend
        self.is_running = True

    def detect_file_type(self, url, content_type=None):
        """Detect file type from URL or content type"""
        url_lower = url.lower()

        if content_type:
            content_type_lower = content_type.lower()
            if 'application/zip' in content_type_lower or 'application/x-zip' in content_type_lower:
                return 'zip'
            elif 'application/x-rar' in content_type_lower or 'application/vnd.rar' in content_type_lower:
                return 'rar'
            elif 'image/png' in content_type_lower:
                return 'png'
            elif 'image/vnd.ms-dds' in content_type_lower or 'image/dds' in content_type_lower:
                return 'dds'

        if '.zip' in url_lower:
            return 'zip'
        elif '.rar' in url_lower:
            return 'rar'
        elif '.png' in url_lower:
            return 'png'
        elif '.jpg' in url_lower or '.jpeg' in url_lower:
            return 'png'
        elif '.dds' in url_lower:
            return 'dds'

        return 'auto'

    def extract_zip_file(self, zip_path):
        """Extract ZIP file, sanitizing filenames and tracking all created files and folders."""
        extracted_members = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                # --- MODIFICATION: Use the original filename from the archive to preserve encoding/spaces ---
                # The final path will be sanitized by sanitize_filepath.
                try:
                    # Attempt to decode with UTF-8, fall back to a safe encoding if it fails
                    member_filename = member.filename.encode('cp437').decode('utf-8')
                except:
                    member_filename = member.filename

                sanitized_relative_path = sanitize_filepath(member_filename)

                if not sanitized_relative_path:
                    continue

                target_path = os.path.join(self.destination_folder, sanitized_relative_path)

                if not os.path.abspath(target_path).startswith(os.path.abspath(self.destination_folder)):
                    print(f"--- SECURITY WARNING: Skipping potentially malicious path '{member.filename}'")
                    continue

                if member.is_dir():
                    os.makedirs(target_path, exist_ok=True)
                else:
                    parent_dir = os.path.dirname(target_path)
                    os.makedirs(parent_dir, exist_ok=True)
                    with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                        target.write(source.read())

                extracted_members.append(sanitized_relative_path.replace('\\', '/'))

        return list(set(extracted_members))

    def extract_rar_file(self, rar_path):
        """Extract RAR file, sanitizing filenames and tracking all created files and folders."""
        if not RAR_SUPPORT or not RAR_TOOL_AVAILABLE:
            raise Exception("RAR support not available or UnRAR.exe tool not found.")

        extracted_members = []
        with rarfile.RarFile(rar_path) as rar_ref:
            for member in rar_ref.infolist():
                sanitized_relative_path = sanitize_filepath(member.filename)

                if not sanitized_relative_path:
                    continue

                target_path = os.path.join(self.destination_folder, sanitized_relative_path)

                if not os.path.abspath(target_path).startswith(os.path.abspath(self.destination_folder)):
                    print(f"--- SECURITY WARNING: Skipping potentially malicious path '{member.filename}'")
                    continue

                if member.isdir():
                    os.makedirs(target_path, exist_ok=True)
                else:
                    parent_dir = os.path.dirname(target_path)
                    os.makedirs(parent_dir, exist_ok=True)
                    with open(target_path, 'wb') as f:
                        f.write(rar_ref.read(member))

                extracted_members.append(sanitized_relative_path.replace('\\', '/'))

        return list(set(extracted_members))

    def convert_dds_to_png(self, dds_path):
        """
        Converts a DDS file to a PNG file, removes the original DDS,
        and returns the path of the new PNG file.
        """
        if not PILLOW_SUPPORT:
            print("--- CONVERT WARNING: Pillow library not installed. Skipping DDS conversion.")
            return None

        directory = os.path.dirname(dds_path)
        folder_name = os.path.basename(directory)
        png_path = os.path.join(directory, f"{folder_name}.png")

        try:
            with Image.open(dds_path) as img:
                img.save(png_path, 'PNG')
            os.remove(dds_path)
            print(f"--- CONVERT INFO: Converted {os.path.basename(dds_path)} to {os.path.basename(png_path)}.")
            return png_path
        except Exception as e:
            print(f"--- CONVERT ERROR: Failed to convert {os.path.basename(dds_path)}. Error: {e}")
            return None

    def process_directory_for_images(self, base_path):
        """
        Recursively scans for images, converts .dds files, renames duplicates,
        creates JSON configs, and returns a list of all created files.
        """
        # --- START OF MODIFICATION ---
        # This list will hold ALL processed/created files to ensure the uninstaller gets a complete list.
        processed_and_created_files = []
        # --- END OF MODIFICATION ---

        for root, _, files in os.walk(base_path):
            for filename in files:
                if filename.lower().endswith('.dds'):
                    full_dds_path = os.path.join(root, filename)
                    new_png_path = self.convert_dds_to_png(full_dds_path)
                    if new_png_path:
                        relative_path = os.path.relpath(new_png_path, self.destination_folder)
                        # A converted DDS becomes a primary asset, so track it.
                        processed_and_created_files.append(relative_path.replace('\\', '/'))

        if self.category == 'balls':
            while True:
                png_file_paths = {}
                for root, _, files in os.walk(base_path):
                    for filename in files:
                        if filename.lower().endswith('.png'):
                            lower_filename = filename.lower()
                            if lower_filename not in png_file_paths:
                                png_file_paths[lower_filename] = []
                            png_file_paths[lower_filename].append(os.path.join(root, filename))

                file_to_rename = None
                for lower_filename, paths in png_file_paths.items():
                    if len(paths) > 1 and lower_filename != 'tint.png':
                        file_to_rename = paths[1]
                        break

                if file_to_rename is None:
                    break

                base_name, extension = os.path.splitext(file_to_rename)
                counter = 1
                new_full_path = f"{base_name}_{counter}{extension}"

                while os.path.exists(new_full_path):
                    counter += 1
                    new_full_path = f"{base_name}_{counter}{extension}"

                try:
                    os.rename(file_to_rename, new_full_path)
                    print(
                        f"--- RENAME INFO: Renamed duplicate '{os.path.basename(file_to_rename)}' to '{os.path.basename(new_full_path)}'")
                except OSError as e:
                    print(f"--- RENAME ERROR: Could not rename {file_to_rename}: {e}")

        for root, _, files in os.walk(base_path):
            image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            if not image_files:
                continue

            # --- START OF MODIFICATION ---
            # Add all found image files to the list of assets to be tracked for uninstallation.
            for image_filename in image_files:
                relative_image_path = os.path.relpath(os.path.join(root, image_filename), self.destination_folder)
                processed_and_created_files.append(relative_image_path.replace('\\', '/'))

            # Logic specifically for the 'banner' category
            if self.category == 'banner':
                for image_filename in image_files:
                    base_name = os.path.splitext(image_filename)[0]
                    json_data = {
                        base_name: {
                            "Diffuse": image_filename,
                            "Paint": "",
                            "Tint": ""
                        }
                    }
                    json_filename = f"{base_name}.json"
                    json_full_path = os.path.join(root, json_filename)
                    try:
                        with open(json_full_path, 'w') as json_file:
                            json.dump(json_data, json_file, indent=4)
                        relative_path = os.path.relpath(json_full_path, self.destination_folder)
                        processed_and_created_files.append(relative_path.replace('\\', '/'))
                        print(f"--- BANNER JSON INFO: Created specific config at: {relative_path}")
                    except IOError as e:
                        print(f"--- BANNER JSON ERROR: Could not write JSON file at {json_full_path}: {e}")
                continue
            # --- END OF MODIFICATION ---

            has_existing_json = any(f.lower().endswith('.json') for f in files)

            if has_existing_json:
                print(
                    f"--- JSON INFO: Skipping JSON creation in '{os.path.basename(root)}' as a .json file already exists.")
                continue

            json_data = {}
            for image_filename in image_files:
                base_name = os.path.splitext(image_filename)[0]
                json_data[base_name] = {
                    "Group": "",
                    "Params": {"Diffuse": image_filename}
                }

            if json_data:
                folder_name = os.path.basename(root)
                json_filename = f"{folder_name}.json"
                json_full_path = os.path.join(root, json_filename)

                try:
                    with open(json_full_path, 'w') as json_file:
                        json.dump(json_data, json_file, indent=4)

                    relative_path = os.path.relpath(json_full_path, self.destination_folder)
                    processed_and_created_files.append(relative_path.replace('\\', '/'))
                    print(f"--- JSON INFO: Created config file at: {relative_path}")
                except IOError as e:
                    print(f"--- JSON ERROR: Could not write JSON file at {json_full_path}: {e}")

        return processed_and_created_files

    def save_image_file(self, source_path, file_is_dds=False):
        """Processes a downloaded image, converting DDS to PNG if necessary."""
        image_content = b''
        extension = 'png'

        if file_is_dds:
            if not PILLOW_SUPPORT:
                raise Exception("Pillow library is required to process .dds files.")
            try:
                with Image.open(source_path) as img:
                    buffer = io.BytesIO()
                    img.save(buffer, format='PNG')
                    image_content = buffer.getvalue()
                print("--- CONVERT INFO: Converted downloaded DDS to PNG in memory.")
            except Exception as e:
                raise Exception(f"Failed to convert downloaded DDS file: {e}")
        else:
            with open(source_path, 'rb') as f:
                image_content = f.read()

        clean_name = sanitize_filepath(self.name)
        filename = f"{clean_name}.{extension}"
        base_name = clean_name

        mod_folder = os.path.join(self.destination_folder, self.mod_id)
        os.makedirs(mod_folder, exist_ok=True)

        final_image_path = os.path.join(mod_folder, filename)
        with open(final_image_path, 'wb') as img_file:
            img_file.write(image_content)

        json_path = os.path.join(mod_folder, f"{base_name}.json")

        # --- START OF MODIFICATION ---
        # Generate specific JSON format if the category is 'banner'
        if self.category == 'banner':
            json_data = {
                base_name: {
                    "Diffuse": filename,
                    "Paint": "",
                    "Tint": ""
                }
            }
        else:
            # Original generic JSON format
            json_data = {
                base_name: {
                    "Group": "",
                    "Params": {"Diffuse": filename}
                }
            }
        # --- END OF MODIFICATION ---

        with open(json_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        tracked_paths = [
            os.path.relpath(mod_folder, self.destination_folder).replace('\\', '/'),
            os.path.relpath(final_image_path, self.destination_folder).replace('\\', '/'),
            os.path.relpath(json_path, self.destination_folder).replace('\\', '/')
        ]
        return tracked_paths

    def find_all_mod_assets(self, initial_assets):
        """
        Scans the destination folder to create a comprehensive list of all files and folders
        related to the newly installed mod based on the initial list of extracted assets.
        """
        if not initial_assets:
            return []

        # Determine the top-level directory/directories created by the installation
        top_level_assets = set()
        for asset in initial_assets:
            top_level_assets.add(asset.split('/')[0])

        all_paths = set()
        for top_level in top_level_assets:
            scan_path = os.path.join(self.destination_folder, top_level)

            # Add the top-level asset itself (could be a file or a folder)
            all_paths.add(top_level.replace('\\', '/'))

            # If it's a directory, walk through it to find all contents
            if os.path.isdir(scan_path):
                for root, dirs, files in os.walk(scan_path):
                    for name in files:
                        full_path = os.path.join(root, name)
                        relative_path = os.path.relpath(full_path, self.destination_folder)
                        all_paths.add(relative_path.replace('\\', '/'))
                    for name in dirs:
                        full_path = os.path.join(root, name)
                        relative_path = os.path.relpath(full_path, self.destination_folder)
                        all_paths.add(relative_path.replace('\\', '/'))

        return list(all_paths)

    def run(self):
        temp_file_path = None
        try:
            self.progress_updated.emit(f"Downloading {self.name}...", 25)
            os.makedirs(self.destination_folder, exist_ok=True)
            temp_file_path = os.path.join(self.destination_folder, f"temp_{self.mod_id}.tmp")

            with requests.get(self.url, stream=True, timeout=20) as r:
                r.raise_for_status()
                with open(temp_file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            self.progress_updated.emit("Download complete. Processing...", 50)
            content_type = requests.head(self.url, timeout=10).headers.get('content-type', '')
            actual_file_type = self.detect_file_type(self.url, content_type)

            tracked_files = []
            if actual_file_type == 'zip':
                self.progress_updated.emit("Extracting ZIP...", 75)
                tracked_files.extend(self.extract_zip_file(temp_file_path))
            elif actual_file_type == 'rar':
                self.progress_updated.emit("Extracting RAR...", 75)
                tracked_files.extend(self.extract_rar_file(temp_file_path))
            elif actual_file_type in ['png', 'jpg', 'jpeg', 'dds']:
                self.progress_updated.emit(f"Saving {actual_file_type.upper()}...", 75)
                is_dds = actual_file_type == 'dds'
                tracked_files.extend(self.save_image_file(temp_file_path, file_is_dds=is_dds))
            else:
                raise TypeError(f"Unsupported file type: {actual_file_type}")

            self.progress_updated.emit("Finalizing installation...", 85)
            for root, _, files in os.walk(self.destination_folder):
                for filename in files:
                    if filename.lower().endswith('.zip'):
                        zip_path = os.path.join(root, filename)
                        print(f"--- ZIP CHECK: Found nested zip file: {zip_path}. Extracting...")
                        try:
                            tracked_files.extend(self.extract_zip_file(zip_path))
                            os.remove(zip_path)
                        except Exception as e:
                            print(f"--- ZIP CHECK ERROR: Failed to extract nested zip: {e}")

            tracked_files.extend(self.process_directory_for_images(self.destination_folder))

            final_asset_list = self.find_all_mod_assets(tracked_files)

            installed_mods = self.backend.load_installed_mods()
            installed_mods[self.mod_id] = list(set(final_asset_list))
            self.backend.save_installed_mods(installed_mods)

            self.progress_updated.emit("Installation complete!", 100)
            self.install_complete.emit(self.mod_id)

        except requests.exceptions.RequestException as e:
            self.download_error.emit(f"Download failed: {e}")
        except Exception as e:
            self.download_error.emit(f"An error occurred: {e}")
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except OSError as e:
                    print(f"Error removing temp file: {e}")

    def stop(self):
        self.is_running = False