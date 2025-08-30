import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui_components import BrowserWindow
import os

if __name__ == "__main__":
    """
    Main entry point for the application.
    Initializes the QApplication and the main BrowserWindow.
    """
    # --- MODIFICATION: Add more flags for enhanced GPU utilization ---
    chromium_flags = [
        # --- Existing Good Flags ---
        '--disable-frame-rate-limit',  # Unlocks the frame rate for smoother animations on high-refresh-rate monitors.
        '--ignore-gpu-blocklist',  # Forces GPU acceleration even on systems with older GPUs.
        '--enable-gpu-rasterization',  # Offloads rasterization from the CPU to the GPU.

        # --- Recommended Additions ---
        '--use-angle=d3d11',  # Explicitly use the high-performance D3D11 backend on Windows.
        '--enable-oop-rasterization',  # Moves rasterization to the dedicated GPU process.
        '--enable-native-gpu-memory-buffers',  # Use native GPU memory for better performance in compositing.
        '--enable-zero-copy',  # More efficient path for video/image data to the GPU.
        '--in-process-gpu'  # Runs the GPU process in the same process to reduce overhead.
    ]
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = ' '.join(chromium_flags)

    # Enable High DPI Scaling (best placed before QApplication instantiation)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())