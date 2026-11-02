# Expiry-IQ

AI-powered fridge scanner that cuts household food waste. Upload a photo of your fridge and get detected items, expiry predictions, waste cost in INR, recipes that use up what's about to go bad, and a fridge health score.

## Features

- **Item detection**: YOLOv8 finds food items in the photo
- **Expiry prediction**: shelf-life database labels each item `fresh`, `expiring soon` (≤ 3 days) or `expired`
- **Waste cost (INR)**: totals the price of everything at risk
- **Recipe suggestions**: GPT-4o-mini builds recipes that prioritise expiring items
- **Fridge health score**: 0–100 from freshness plus food-group variety
- **Scan history and analytics**: results stored in MongoDB
- **Graceful fallbacks**: runs without an OpenAI key (static recipes) and without MongoDB (no persistence)

## Tech stack

| Layer | Tools |
|---|---|
| API | Python, FastAPI, Uvicorn |
| Vision | YOLOv8 (Ultralytics), OpenCV, Pillow, NumPy |
| GenAI | OpenAI `gpt-4o-mini` |
| Database | MongoDB (Motor async driver) |
| Frontend | Streamlit |

## How it works

```
Fridge photo → POST /api/scan-fridge
   1. Validate and save image
   2. YOLOv8 detects food items
   3. Expiry service predicts days left
   4. Cost service totals at-risk items (INR)
   5. Recipe service queries GPT-4o-mini
   6. Health service scores the fridge
   7. Save to MongoDB → return JSON
```

**Health score**

```
base    = (fresh_items / total_items) × 80
variety = min(food_groups_present × 4, 20)
score   = min(base + variety, 100)
```

## Project structure

```
expiry-iq/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, lifecycle hooks
│   │   ├── routes/scan.py       # /scan-fridge, /scans, /analytics
│   │   ├── services/
│   │   │   ├── vision_service.py
│   │   │   ├── expiry_service.py
│   │   │   ├── cost_service.py
│   │   │   ├── recipe_service.py
│   │   │   └── health_service.py
│   │   ├── database/mongodb.py
│   │   └── models/item_model.py
│   ├── uploads/                 # saved fridge images
│   ├── requirements.txt
│   └── .env.example
├── frontend/                    # Streamlit UI
├── yolov8n.pt                   # YOLOv8 nano weights
└── README.md
```

## Getting started

### Prerequisites

- Python 3.11+
- MongoDB 6+ (local or Atlas), optional
- OpenAI API key, optional

### Install

```bash
git clone https://github.com/D123-cpu/expiry-iq.git
cd expiry-iq/backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env            # Windows: copy .env.example .env
```

```env
OPENAI_API_KEY=sk-your-key
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=fridge_ai
UPLOAD_DIR=uploads
YOLO_MODEL_PATH=../yolov8n.pt
```

### Run

```bash
# Terminal 1: backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: frontend (optional)
cd frontend
pip install streamlit requests
streamlit run streamlit_app.py
```

- Swagger docs: http://localhost:8000/docs
- Streamlit UI: http://localhost:8501

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/scan-fridge` | Upload an image (`multipart/form-data`, field `file`; JPG/PNG/WEBP, max 20 MB) |
| `GET` | `/api/scans?limit=10` | Recent scan history |
| `GET` | `/api/analytics` | Total scans, total waste cost, average health score |

### Example

```bash
curl -X POST http://localhost:8000/api/scan-fridge -F "file=@fridge.jpg"
```

```json
{
  "scan_id": "65f1a2b3c4d5e6f7a8b9c0d1",
  "detected_items": ["milk", "tomato", "bread"],
  "expiry": [
    {"item": "tomato", "days_left": 2, "status": "expiring soon", "estimated_expiry_date": "2026-11-04"}
  ],
  "expiring_items": ["tomato"],
  "recipes": ["1. Tomato toast: toast bread, top with sliced tomato and olive oil."],
  "waste_cost": 30.0,
  "cost_breakdown": [
    {"item": "tomato", "price_inr": 30.0, "is_expiring": true}
  ],
  "health_score": 72.0,
  "timestamp": "2026-11-02T10:30:00"
}
```

## Limitations

- The pretrained `yolov8n.pt` is trained on COCO, which covers only a handful of food classes (banana, apple, orange, broccoli, carrot, etc.). Dairy, eggs and packaged goods are not reliably detected.
- Expiry is estimated from typical shelf life, not read from labels or packaging dates.
- Prices are approximate INR retail averages.

## Roadmap

- Fine-tune YOLOv8 on a fridge-specific food dataset
- OCR for printed expiry dates
- Per-user accounts and expiry push notifications
- Editable price and shelf-life database
- Docker setup

## License

MIT
