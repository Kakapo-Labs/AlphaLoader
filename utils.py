import os
import rarfile

# --- RAR Support Configuration ---
RAR_SUPPORT = True
PATOOL_SUPPORT = False

# --- START OF MODIFICATION ---
# This new logic forces the script to use a modern UnRAR.exe that you provide.
# 1. Download UnRAR.exe from https://www.rarlab.com/rar_add.htm
# 2. Place the UnRAR.exe file in the same directory as this script.

try:
    # Build the path to the UnRAR.exe located alongside your script
    # This is the most reliable way to ensure the correct tool is used.
    custom_unrar_path = os.path.join(os.path.dirname(__file__), "UnRAR.exe")

    if os.path.exists(custom_unrar_path):
        rarfile.UNRAR_TOOL = custom_unrar_path
        RAR_TOOL_AVAILABLE = True
        print(f"--- RAR INFO: Successfully loaded custom UnRAR tool from: {custom_unrar_path}")
    else:
        # If the custom tool isn't found, fall back to the original search method.
        print(
            f"--- RAR WARNING: Custom UnRAR.exe not found at '{custom_unrar_path}'. Falling back to automatic search.")
        possible_paths = [
            r"C:\Program Files\WinRAR\UnRAR.exe",
            r"C:\Program Files (x86)\WinRAR\UnRAR.exe",
        ]
        rar_tool_found = False
        for path in possible_paths:
            if os.path.exists(path):
                rarfile.UNRAR_TOOL = path
                rar_tool_found = True
                print(f"--- RAR INFO: Found UnRAR tool at: {path}")
                break

        RAR_TOOL_AVAILABLE = rar_tool_found
        if not RAR_TOOL_AVAILABLE:
            print("--- RAR ERROR: No UnRAR.exe found in standard or custom paths. RAR extraction will fail.")

except Exception as e:
    print(f"--- RAR ERROR: RAR tool detection failed: {e}")
    RAR_TOOL_AVAILABLE = False
# --- END OF MODIFICATION ---


try:
    import patoolib

    PATOOL_SUPPORT = True
except ImportError:
    pass  # patoolib is optional