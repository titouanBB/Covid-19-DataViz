# COVID-19 Simulator & Dashboard

## 1. Project Description
**COVID-19 Simulator** is an interactive Python application that visualizes the evolution of the COVID-19 pandemic worldwide.
The project offers two main modes:

1. **Global Curves**: visualize the progression of confirmed cases by country over time.
2. **Interactive Map**: a world map colored by the number of confirmed cases, with country details (cases, deaths, vaccines) on click.

The goal is to provide an **educational and interactive tool** to track the spread of the virus and compare countries.

---

## 2. Prerequisites
- Python 3.10 or higher
- Packages listed in `requirements.txt`:

```txt
streamlit==1.28.0
pandas==2.1.0
plotly==6.9.0
requests==2.32.0
streamlit-plotly-events==0.6.0
```

---

## 3. Installation
- git clone <project_url>
    cd covid_simulator
- python -m venv venv
    source venv/bin/activate  # Linux / Mac
    venv\Scripts\activate     # Windows
- pip install -r requirements.txt

---

## 4. Run the Application
- streamlit run src/main.py
