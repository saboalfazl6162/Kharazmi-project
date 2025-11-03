# Project

project



## Tech Stack

- **Backend**: Python Django
- **Database**: SQLite 
- **Frontend**: HTML, CSS, JavaScript

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git (optional, for version control)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/saboalfazl6162/Kharazmi-project
cd
   ```

2. **Create a virtual environment**
```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
```bash
pip install -r requirements.txt
   ```

4. **Configure the application**
   - Create `.env`
   - Copy `.env.example` to `.env`
   - Update the configuration with your settings (database URI, secret key, etc.)

5. **Initialize the database**
```bash
python manage.py migrate
   ```

## Running the Application

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

## Admin Features

- View all users and their links
- Monitor system statistics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Built with Django
- Inspired by popular URL shortening services
- Special thanks to all contributors