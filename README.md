# Uniden Assistant

A web application for managing Uniden Scanner Favourites lists. Import, edit, and export scanner configuration files with an intuitive interface.

## Quick Start

1. **Setup** - Install dependencies and initialize the application:
   ```bash
   ./setup_uniden.sh
   ```

2. **Start** - Run the application:
   ```bash
   ./uniden_assistant start
   ```

3. **Access** - Open in your browser:
   - Frontend: http://localhost:9001

## Features

- **Import** - Load Uniden scanner configuration files (.cfg, .hpd)
- **Edit** - Manage favourites lists, scanner profiles, and channel groups
- **Export** - Save your configurations back to scanner-compatible formats
- **Organize** - Create and manage multiple favourites lists

## Architecture

- **Backend** - Django 4.2 REST API with MongoDB storage
- **Frontend** - Vue 3 with Quasar Framework
- **Database** - MongoDB for user data, SQLite for Django core

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

MIT
Pull requests welcome!
