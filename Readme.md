# Planting Advisor

Even with advancement in planting technology, many farmers across Ghana rely heavily on Nature's assistance to grow crops. With climate change, rainy seasons are becoming unpredictable. 

Planting Advisor is an AI-powered web app that helps farmers decide whether it's the right time to plant a specific crop — based on real weather patterns, historical climate data, and geographical compatibility. Advice is also translated into **Asanti Twi** for local accessibility.

---

## What It Does

1. Takes a **country**, **place**, and **crop** as input
2. Determines the **geolocation** of the given place
3. Analyses **past and forecasted weather** (4 weeks each way) for that location
4. Advises whether conditions are suitable for planting the crop
5. Translates the full advice into **Asanti Twi**

---

## Project Structure

```
planting-advisor/
├── planting_advisor.py       # Streamlit frontend
├── utils2.py                 # Core logic: geolocation, advice, translation
├── planting_advisor.ipynb    # Jupyter notebook (prototyping/exploration)
├── requirements.txt          # Python dependencies
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- An [OpenAI API key](https://platform.openai.com/api-keys)
- An [OpenCageGeocode API key] (https://opencagedata.com/api)

### Installation

```bash
git clone https://github.com/rick-a-commits/planting-advisor.git
cd planting-advisor
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory and add your OpenAI key:

```
OPENAI_API_KEY=your_key_here
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### Run the App

```bash
streamlit run planting_advisor.py
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app interface |
| `openai` | GPT API calls for advice and translation |
| `opencage` | Opencage API calls for geo location |
| `python-dotenv` | Loads API key from `.env` |
| `ipython` | Notebook support |

Install all with:

```bash
pip install -r requirements.txt
```

---

## How It Works

The app makes three sequential API calls:

1. **Geolocation** (`opencage`) — converts the country and place name into coordinates
2. **Planting advice** (`gpt-4o`) — uses the coordinates to assess weather and soil compatibility for the crop
3. **Translation** (`gpt-4o-mini`) — translates the advice into Asanti Twi

---

## Notes

- Advice is intended for **subsistence and nature-reliant farmers**, not industrial agriculture
- The app will flag if a crop is geographically incompatible with the location (e.g. strawberries in a tropical climate)
- Response quality depends on OpenAI's ability to retrieve current weather context for the given coordinates
-- This would be better suited for mobile apps and whatsapp extensions for better accessibily.

---

## License

This project does not currently specify a license. Contact the repository owner for usage terms.
