# Realtime Airspace Data Pipeline

**Författare:** Masoud  
**Kurs:** Data Engineering 2024  
**Skola:** Stockholms Tekniska Institut  
**Handledare:** Kokchun Giang  
**Datum:** 2025-02-03

## Beskrivning
Detta projekt är en end‑to‑end‑datapipeline för insamling, bearbetning, lagring och visualisering av realtidsflygdata från OpenSky Network. Målet är att demonstrera hur moderna data engineering‑verktyg kan kombineras för att skapa en automatiserad och skalbar lösning som kontinuerligt hämtar flygdata, transformerar den och presenterar den i en interaktiv dashboard.

## Funktioner
**Ingestion:** Hämtning av realtidsdata från OpenSky Network.  
**Transformation:** Datavalidering och förberedelse i Python (Pandas).  
**Lagring:** Snowflake som centralt datalager; dbt för modellering.  
**Orkestrering:** Dagster för schemaläggning och pipeline‑körningar.  
**Visualisering:** Streamlit‑dashboard med interaktiv HTML‑karta som visar flygpositioner, höjd och hastighet i realtid.

## Installation och förutsättningar
Projektet kräver Python 3.9 eller senare, Git och åtkomst till en Snowflake‑instans. Rekommenderat arbetsflöde för lokal utveckling:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
pip install -r requirements.txt

