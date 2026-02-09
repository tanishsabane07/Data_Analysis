# Chemical Equipment Parameter Visualizer

A hybrid application for visualizing and analyzing chemical equipment data. Includes a Django backend API, React web frontend, and PyQt5 desktop application.

## 📁 Project Structure

```
├── backend/          # Django REST API
├── frontend/         # React web application
├── desktop/          # PyQt5 desktop application
└── sample_equipment_data.csv
```

## 🛠️ Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **Git**

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/tanishsabane07/Data_Analysis.git
cd Data_Analysis
```

---

### 2. Backend (Django API)

```bash
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Start the server
python3 manage.py runserver
```

The API will be available at `http://localhost:8000`

---

### 3. Frontend (React Web App)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The web app will be available at `http://localhost:5173`

---

### 4. Desktop Application (PyQt5)

```bash
# Navigate to desktop
cd desktop

# Install dependencies (use a virtual environment if needed)
pip install -r requirements.txt

# Run the application
python3 main.py
```

---

## 📊 Features

- **CSV Upload**: Import equipment data from CSV files
- **Data Visualization**: Interactive charts for parameter analysis
- **History Management**: Track and review past analyses
- **PDF Reports**: Generate downloadable PDF reports
- **Cross-Platform**: Available as web and desktop applications

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| Backend   | Django, Django REST Framework |
| Frontend  | React, Vite, Chart.js |
| Desktop   | PyQt5, Matplotlib |
| Data      | Pandas |

---

## 📝 Sample Data

A sample CSV file (`sample_equipment_data.csv`) is included for testing.

---

## 📄 License

MIT License
