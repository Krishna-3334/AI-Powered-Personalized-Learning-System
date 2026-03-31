# AI-Powered Personalized Learning System

A quick starter project that generates personalized learning plans based on learner profile data.

## Tech Stack

- Backend: Python + Flask API
- Frontend: HTML, CSS, Vanilla JavaScript

## Project Structure

```text
AI-Powered Personalized Learning System/
  backend/
    app.py
    requirements.txt
  frontend/
    index.html
    style.css
    app.js
```

## Run Quickly

### 1) Start Backend API

```bash
cd "AI-Powered Personalized Learning System/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

API runs on `http://localhost:8000`

### 2) Open Frontend

Open this file in your browser:

`AI-Powered Personalized Learning System/frontend/index.html`

## API

### `POST /api/recommend`

Sample request body:

```json
{
  "name": "Krishna",
  "subject": "Data Structures",
  "goal": "Crack coding interviews",
  "level": "Intermediate",
  "learning_style": "Visual",
  "minutes_per_day": 60
}
```
