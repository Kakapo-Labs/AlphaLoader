# AlphaLoader

## About The Project

AlphaLoader is a sleek and user-friendly desktop application designed to simplify the process of finding, downloading, and managing AlphaConsole mods for Rocket League. It integrates seamlessly with BakkesMod to provide a smooth experience for players looking to customize their game.

## Features

- **Browse and Discover:** Explore a curated list of mods, including custom ball textures, boost meters, decals, banners, and profile borders.
- **One-Click Installation:** Install and uninstall mods with a single click.
- **Automatic Folder Detection:** AlphaLoader automatically finds your BakkesMod texture folders.
- **Lightweight and Fast:** Built with PyQt5 and a web-based UI for a responsive experience.

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- **Windows Operating System:** The application is designed for Windows.
- **Rocket League:** You must have Rocket League installed.
- **BakkesMod:** BakkesMod must be installed and running. You can download it from [bakkesmod.com](https://www.bakkesmod.com/).
- **AlphaConsole Bakkesmod Plugin:** This plugin is required for AlphaLoader to function correctly.

### Installation

1. Download the latest release from the [Releases](https://github.com/your_username/AlphaLoader/releases) page.
2. Run the `AlphaLoader.exe` file.

## Usage

Launch AlphaLoader, browse the available mods, and click the "Install" button on any mod you wish to add to your game. To remove a mod, click "Uninstall".

## How It Works

AlphaLoader is a Python application built with PyQt5 for the graphical user interface. It uses a `QWebEngineView` to render a modern, web-based UI. The backend, written in Python, handles all the core logic:

- **Fetching Mods:** It retrieves the list of available mods from a JSON file hosted on GitHub.
- **File Management:** It locates the appropriate BakkesMod data folders (`acplugin`) within your system's `APPDATA` or Steam library folders.
- **Installation/Uninstallation:** It downloads the mod files (usually ZIP archives), extracts them, and places them in the correct texture directories. It also keeps track of installed mods to allow for easy removal.


