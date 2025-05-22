# 🌲 AI-Driven Forest Management

This project presents a comprehensive, AI-powered forest monitoring system designed specifically for Kazakhstan’s forests. It integrates satellite remote sensing, machine learning, and an interactive chatbot to help researchers, policymakers, and conservationists monitor forest health, deforestation, and fire damage in near-real-time.

## 📌 Project Objectives

- Build an automated forest monitoring pipeline using Sentinel-2 and LANDSAT imagery.
- Generate biweekly forest masks and vegetation indices (e.g., NDVI, NBR).
- Integrate burned area detection and deforestation tracking.
- Develop a mobile application with interactive map visualizations.
- Deploy a retrieval-augmented generation (RAG) chatbot to assist users.

## 🛰️ Data Sources

- **Sentinel-2 (ESA Copernicus)** – 10m resolution, biweekly images.
- **LANDSAT 8 (NASA)** – 30m resolution, used for cloud gaps and interpolation.

## 🛠️ Technologies Used

- **Backend**: Django, Django REST Framework, SQLite
- **Frontend**: Flutter (cross-platform for Android/iOS)
- **AI Chatbot**: LangChain + OpenAI API (RAG-based retrieval)
- **Remote Sensing**: Google Earth Engine, Rasterio, NumPy
- **Storage**: Google Drive for satellite images and masks

## 📊 Features

### 🌲 Forest Monitoring
- Generate and visualize forest cover masks using NDVI thresholds.
- Burned area detection with NBR index.
- Gap filling through temporal interpolation.

### 🔥 Deforestation Detection
- Pixel-wise comparison of mask images to highlight cleared areas.
- Visual overlays for changes.

### 🧠 AI Chatbot (RAG)
- Queryable assistant for forest metrics, trends, and context explanations.
- Uses domain-specific data and OpenAI’s LLM for responses.

### 📈 Vegetation Metrics
- Compute and analyze indices: NDVI, EVI, NDWI, NBR, GNDVI, etc.
- Time-series analysis for forest health.

### 📱 Mobile App
- Forest selection, visual dashboards, chatbot interaction
- Responsive, user-friendly UI built in Flutter

## 🗂️ Dataset Overview

- ~300 TIFF images (Sentinel-2 + LANDSAT), ~1.3 GB in total.
- Includes:
  - Forest masks
  - Burned area masks
  - Vegetative index values over time

## 🧮 Key Algorithms

- NDVI/NBR threshold-based classification
- Cloud masking using SCL and QA bands
- Nearest neighbor reprojection for resolution harmonization
- Deforestation pixel differencing
- Mean vegetation index aggregation

## 🧪 Evaluation

- **Accuracy**: Visual validation with Google Earth Pro imagery
- **Usability**: System Usability Score: **86.6 / 100**
- **Performance**: 2–5s load time (visualizations), 4s chatbot latency




