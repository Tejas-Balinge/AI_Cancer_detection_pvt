# OncoDetect AI - Disease Detection Web Application

A full-stack AI-powered Disease Detection Web Application for Histopathologic Cancer Detection. 

## 🏗 Project Structure

```text
Histopathological-Cancer-Detection-master/
├── client/                     # React Frontend
│   ├── src/
│   │   ├── components/         # UI Components (Navbar)
│   │   ├── pages/              # Views (Landing, Login, Dashboard, Upload, Admin)
│   │   ├── utils/              # API utilities
│   │   ├── App.jsx             # Routing
│   │   ├── main.jsx            # React Entry
│   │   └── index.css           # Tailwind v4 Global Styles
│   ├── package.json            # Node Dependencies
│   └── vite.config.js          # Vite config with Tailwind
├── server/                     # FastAPI Backend
│   ├── main.py                 # REST API Endpoints
│   ├── auth.py                 # JWT Authentication & Hashing
│   ├── database.py             # SQLAlchemy DB Connection (SQLite)
│   ├── models.py               # DB Schema
│   ├── schemas.py              # Pydantic validation schemas
│   ├── ml_utils.py             # TensorFlow / Keras inference logic
│   └── requirements.txt        # Python Dependencies
├── Model/                      
│   └── cancer_detection_model.h5 # Trained model (Must be present for real inference)
├── docker-compose.yml          # Docker composition
└── README.md                   # This file
```

## 🚀 Setup & Installation (Local Development)

### 1. Backend Setup

Open a terminal and navigate to the project root:

```bash
cd server
python -m venv venv
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*The backend will run on http://localhost:8000*

### 2. Frontend Setup

Open a second terminal and navigate to the client folder:

```bash
cd client

# Install dependencies
npm install

# Start development server
npm run dev
```
*The frontend will run on http://localhost:5173*

## 🐳 Docker Deployment

To run the entire application using Docker Compose:

1. Ensure you have Docker and Docker Compose installed.
2. Run the following command in the root directory:

```bash
docker-compose up --build -d
```

- Frontend will be accessible at: `http://localhost`
- Backend API at: `http://localhost:8000`

## ⚙️ Environment Variables

### Frontend (`client/.env`)
```
VITE_API_URL=http://localhost:8000
```

## 🧠 AI Model Integration

The `server/ml_utils.py` looks for your trained model in the `Model/` directory (`cancer_detection_model.h5`). 
If the model file is absent or if TensorFlow fails to load on your current Python version (e.g., Python 3.13), the system will automatically fall back to **Mock Inference Mode** so you can still test the UI, uploading, database, and admin features flawlessly!

## 🛡️ Security Features
- **JWT Authentication** for secure sessions.
- **Bcrypt Password Hashing** before saving to the database.
- **CORS Protection** via FastAPI Middleware.
- **Admin Role Protection** for analytic routes.

Enjoy building your AI healthcare startup! 🚀
