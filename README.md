# EventSpot - Music Event Discovery
EventSpot is a web application that recommends events based on user Spotify listening history and in-app preferences. The backend is built with Django and the frontend is built with React.

## Getting Started

Note: Database is a locally hosted PostgreSQL server. Database setup and dataset not included.
To get a version running yourself here are the steps:

### Prerequisites

- Python 3.8 or higher
- Node.js 14.0.0 or higher
- npm 6.14.0 or higher

### Backend Setup

1. Navigate to the `backend` directory:

```sh
cd backend
```

2. Create a virtual environment:
```sh
python3 -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```py
venv\Scripts\activate
```
- On Unix or MacOS:
```py
source venv/bin/activate
```
4. Install the Python dependencies:
```sh
pip install -r requirements.txt
```
5. Apply the migrations:
```sh
python manage.py migrate
```
6. Run the Django server:
```sh
python manage.py runserver
```
The Django server will start running at `http://localhost:8000`.
**Frontend Setup**
1. Navigate to the `frontend` directory:
```sh
cd frontend
```
2. Install the Node.js dependencies:
```sh
npm install
```
3. Start the React development server:
```sh
npm start
```
The React development server will start running at `http://localhost:3000`.
___
## Built With
- Django - The web framework used for the backend
- React - The web library used for the frontend
- Playwright - Automation tool used for webscraper
- BeautifulSoup4 - HTML parser used for webscraper
- PostgreSQL - Database used
- SpotifyAPI - For user data and authentication

## Author
Matthew Tweedy
