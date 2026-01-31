# Uniden Assistant

Minimal setup and run instructions.

## Quick start

1. Setup environment and dependencies:

```bash
./setup_uniden.sh
```

2. Start the application:

```bash
./uniden_assistant start
```

3. Check status or logs if needed:

```bash
./uniden_assistant status
./uniden_assistant logs
```

## Configuration

Edit [config.env](config.env) or start from [config.env.example](config.env.example).

```bash
cp config.env.example config.env
```

## URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api

## Development

### Backend
- Django 4.2
- Django REST Framework 3.14
- Django CORS Headers
- Python-decouple

### Frontend
- Vue 3
- Vue Router 4
- Pinia (state management)
- Quasar Framework (UI)
- Axios (HTTP client)
- Vite (build tool)

## File Upload

Supported file types:
- `.hpd` - Uniden database files
- `.cfg` - Configuration files

Max file size: 5MB

## Deployment

### Django Backend
```bash
# Collect static files
python manage.py collectstatic

# Use gunicorn for production
gunicorn uniden_assistant.wsgi:application
```

### Vue Frontend
```bash
# Build for production
npm run build

# Deploy the dist/ folder to a web server
```

## Troubleshooting

### CORS Errors
Ensure `CORS_ALLOWED_ORIGINS` includes your frontend URL in Django settings.

### File Upload Fails
Check file size and format. Maximum 5MB, `.hpd` or `.cfg` files only.

### Port Already in Use
Change the port in:
- Django: `python manage.py runserver 0.0.0.0:8001`
- Vue: Modify `vite.config.js` server port

## License

MIT

## Contributing

Pull requests welcome!
