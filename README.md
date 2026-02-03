# Uniden Assistant

A web application for managing Uniden Scanner Favourites lists. Import, edit, and export scanner configuration files with an intuitive interface.

## Quick Start

1. **Setup** - Install dependencies and initialize the application:
   ```bash
   ./setup_uniden.sh
   ```
   
   For a clean installation (removes old dependencies):
   ```bash
   ./setup_uniden.sh --clean
   ```

2. **Start** - Run the application:
   ```bash
   ./uniden_assistant start
   ```

3. **Access** - Open in your browser:
   - Frontend: http://localhost:9001

## System Requirements

- **OS**: Debian/Ubuntu Linux or WSL (Windows Subsystem for Linux)
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher (auto-installed if missing)
- **Disk Space**: ~500MB (including dependencies)

## Setup Script Features

The setup script (`setup_uniden.sh`) automatically:
- Installs required OS packages (Python, Node.js, build tools)
- Creates and configures Python virtual environment
- Installs Python dependencies with pinned versions
- Installs frontend Node.js dependencies
- Sets up configuration files
- Initializes SQLite databases
- Validates system prerequisites

**Usage**:
```bash
./setup_uniden.sh              # Standard setup
./setup_uniden.sh --clean      # Clean install (removes old dependencies)
```

**WSL Users**: The script detects WSL and provides helpful reminders about file locations and accessing the app from Windows.

## Features

- **Import** - Load Uniden scanner configuration files (.cfg, .hpd)
- **Edit** - Manage favourites lists, scanner profiles, and channel groups
- **Export** - Save your configurations back to scanner-compatible formats
- **Organize** - Create and manage multiple favourites lists

## Architecture

- **Backend** - Django 4.2 REST API
- **Frontend** - Vue 3 with Quasar Framework
- **Database** - SQLite for Django core and favourites (separate database files)

## Configuration

Edit [config.env](config.env) to customize settings:

```bash
cp config.env.example config.env
# Edit config.env with your settings
```

## Development

For detailed API architecture, see [docs/architecture.md](docs/architecture.md).

## File Specifications

Documentation for supported file formats and record types is available in [docs/Input_File_Specification/](docs/Input_File_Specification/).

## License

Apache License 2.0
Pull requests welcome!
