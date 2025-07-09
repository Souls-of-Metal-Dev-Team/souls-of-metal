# ⚔️ Souls of Metal 🌍

> *"Where strategy meets history in an epic grand strategy experience"* 🎮

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://pygame.org)
[![Development Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

## 📋 Table of Contents
- [🎯 What is Souls of Metal?](#-what-is-souls-of-metal)
- [✨ Features](#-features)
- [🚀 Getting Started](#-getting-started)
- [🎮 Gameplay](#-gameplay)
- [🏗️ Project Structure](#-project-structure)
- [🌐 Localization](#-localization)
- [⚙️ Configuration](#-configuration)
- [🛠️ Development](#-development)
- [📝 Todo List](#-todo-list)
- [🤝 Contributing](#-contributing)

## 🎯 What is Souls of Metal?

**Souls of Metal** is an ambitious grand strategy game built with Python and Pygame, inspired by classic strategy titles. Navigate the complexities of international politics, manage your nation's resources, and shape the course of history in a dynamic world where every decision matters.

### 🌟 Key Highlights
- 🗺️ **Interactive World Map** - Zoom, pan, and explore detailed political boundaries
- 🏛️ **Nation Management** - Control political power, stability, economy, and military
- 👥 **Character System** - Leaders with unique traits and abilities
- 🎵 **Dynamic Soundtrack** - Immersive audio experience with period music
- 🌍 **Multi-language Support** - Internationalization for global accessibility
- ⚡ **Real-time Gameplay** - Day/night cycles and time progression

## ✨ Features

### 🎮 Core Gameplay
- **🏴 Country Selection**: Choose from major and minor nations
- **📊 Diplomacy System**: Manage international relations and alliances
- **💰 Resource Management**: Balance political power, stability, money, and manpower
- **🗓️ Time Progression**: Experience dynamic time flow with customizable speed
- **🎯 Interactive Map**: Click provinces to explore and manage territories

### 🖥️ Technical Features
- **🎨 Custom UI Framework**: Beautiful, responsive interface with animations
- **🔧 Settings System**: Customizable graphics, audio, and gameplay options
- **💾 Save/Load System**: Persistent game state and progress tracking
- **🎵 Audio Engine**: Background music with shuffle and volume controls
- **🌐 Localization Engine**: Support for multiple languages and regions

## 🚀 Getting Started

### 📋 Prerequisites
```bash
Python 3.12+
Pygame 2.0+
```

### 🛠️ Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/Soilad/souls-of-metal.git
   cd souls-of-metal
   ```

2. **Install dependencies**
   ```bash
   pip install pygame
   ```

3. **Launch the game**
   ```bash
   python main.py
   ```

### 🎮 Controls
- **🖱️ Mouse**: Navigate menus and interact with the map
- **⌨️ WASD/Arrow Keys**: Move the camera around the map
- **🔍 Mouse Wheel**: Zoom in/out on the map
- **🖱️ Middle Mouse**: Pan the map view
- **⏸️ Escape**: Access pause menu during gameplay
- **🖥️ F4**: Toggle fullscreen mode

## 🎮 Gameplay

### 🏁 Starting Your Campaign
1. **🌍 Choose Your Nation**: Select from available major or minor countries
2. **📍 Map Overview**: Familiarize yourself with your territory and neighbors
3. **📊 Assess Your Situation**: Check your nation's stats and starting position
4. **🎯 Set Your Goals**: Plan your strategy for expansion, diplomacy, or development

### 🏛️ Managing Your Nation
- **💪 Political Power**: Influence domestic and foreign policy
- **⚖️ Stability**: Maintain order and prevent internal conflicts
- **💰 Treasury**: Fund your military, infrastructure, and diplomatic efforts
- **👥 Manpower**: Recruit and maintain your armed forces

### 🗺️ World Interaction
- **🖱️ Province Selection**: Click on territories to view detailed information
- **🏴 Diplomatic Relations**: Interact with other nations through the diplomacy panel
- **⏰ Time Management**: Control the speed of time progression
- **📈 Character Management**: Utilize leaders and their unique abilities

## 🏗️ Project Structure

```
souls-of-metal/
├── 🐍 main.py              # Game entry point and main loop
├── 🎨 classes.py           # UI components and game objects
├── 🔧 func.py              # Utility functions and helpers
├── 🌐 globals.py           # Global variables and settings
├── 🏛️ CountryData.py       # Country management and data
├── ⚙️ settings.py          # Game configuration
├── 📁 flags/               # Country flag assets (100+ flags)
├── 🎵 sound/music/         # Background music tracks
├── 🗺️ starts/Modern World/ # Game scenarios and maps
├── 🎨 ui/                  # User interface assets
├── 🌐 translation files/   # Localization data
├── 📊 CountryData.json     # Nation statistics and information
├── 🎨 theme.json           # UI color scheme and styling
└── 🌍 translation.json     # Main translation file
```

## 🌐 Localization

The game supports multiple languages with dedicated translation files:
- 🇧🇷 **Portuguese** (`br-translation.json`)
- 🇮🇹 **Italian** (`it-translation.json`) 
- 🇸🇰 **Slovak** (`sl-translation.json`)
- 🇵🇱 **Polish** (`po-translation.json`)
- 🇺🇸 **English** (default)

Add your language by creating a new translation file in the `translation files/` directory!

## ⚙️ Configuration

Customize your experience through `settings.json`:
- 🖥️ **UI Size**: Adjust interface scaling (14-40)
- 📺 **FPS**: Set frame rate (12+ recommended)
- 🔊 **Sound Volume**: Control sound effects (0-100)
- 🎵 **Music Volume**: Adjust background music (0-100)
- 🖱️ **Scroll Invert**: Toggle scroll direction

## 🛠️ Development

### 📁 Key Files for Developers
- **`main.py`**: Core game loop and menu system
- **`classes.py`**: UI components (buttons, maps, country selectors)
- **`func.py`**: Utility functions (clamping, lerping, rounding)
- **`CountryData.py`**: Nation data management
- **`theme.json`**: UI styling and color configuration

### 🔧 Code Style
- Uses **Ruff** for linting with 100-character line limit
- Follows Python conventions with clear commenting
- Modular design for easy feature addition

## 📝 Todo List

### 🎯 High Priority
- 🏛️ **Diplomacy UI Enhancement** - Improve diplomatic interaction interface
- ⚔️ **Military UI Development** - Create comprehensive military management
- 🗺️ **Province System** - Complete province management functionality

### 🎨 UI/UX Improvements
- ✨ **Dynamic Tooltips** - Hover windows with smooth animations
- 📊 **Charts and Graphs** - Implement pie charts for data visualization
- 🧭 **3D Political Compass** - Advanced political alignment system

### 🚀 Gameplay Features
- 🪖 **Troop Types** - Diverse military unit system
- 🏭 **Building System** - Infrastructure and economic development
- 👑 **Estate Management** - Noble and administrative systems

### 🔧 Technical Enhancements
- 💾 **Save System** - Complete game state persistence
- 🌐 **Multiplayer Foundation** - Network gameplay preparation
- 🎮 **Mod Support** - Enable community content creation

## 🤝 Contributing

We welcome contributions! Whether you're interested in:
- 🐛 **Bug Fixes** - Help us squash those pesky issues
- ✨ **New Features** - Implement items from our todo list
- 🌐 **Translations** - Add support for your language
- 🎨 **Art Assets** - Create flags, UI elements, or maps
- 📝 **Documentation** - Improve guides and comments

### 💡 Getting Involved
1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. 💻 Make your changes
4. 🧪 Test thoroughly
5. 📤 Submit a pull request

---

<div align="center">

### 🌟 Made with ❤️ by the Souls of Metal Team 🌟

*Experience history. Shape the future. Command your destiny.*

**⚔️ Souls of Metal - Where Strategy Meets History ⚔️**

</div>


