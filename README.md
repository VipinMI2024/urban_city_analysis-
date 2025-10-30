# Urban City Analysis

**Author:** Vipin Mishra  
**Project Type:** Predictive Analysis for Sustainable Urban Development  
**Frontend:** Jupyter Notebook  
**Backend:** Overpass Turbo API  
**Dataset Used:** Brain Stroke CT Dataset (Kaggle)

---

## Project Overview
The Urban City Analysis project focuses on leveraging data science and API-driven spatial analysis to understand and predict urban development patterns.  
By integrating real-time city data from the Overpass Turbo API with health and demographic datasets, the project aims to identify trends influencing urban sustainability, infrastructure efficiency, and citizen well-being.

---

## Objectives
- Analyze spatial and demographic data to assess urban sustainability.  
- Predict high-risk or underdeveloped city zones using machine learning models.  
- Visualize infrastructure density, population patterns, and environmental metrics.  
- Combine health data (Brain Stroke CT dataset) with urban indicators to explore the relationship between city conditions and public health outcomes.

---

## Tech Stack
- **Language:** Python  
- **Tools & Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Folium, Requests, JSON  
- **APIs:** Overpass Turbo (OpenStreetMap data)  
- **Environment:** Jupyter Notebook  

---

## Methodology
1. **Data Collection:**  
   - Extracted geospatial data via Overpass Turbo API (roads, buildings, green areas).  
   - Integrated health and demographic datasets for cross-domain insights.  

2. **Data Cleaning & Preprocessing:**  
   - Handled missing values and standardized location coordinates.  
   - Encoded categorical variables and normalized numerical features.  

3. **Exploratory Data Analysis (EDA):**  
   - Visualized city-level density, healthcare access, and pollution factors.  
   - Mapped data using Folium for real-time geospatial visualization.  

4. **Predictive Modeling:**  
   - Implemented regression and classification models (Random Forest, Logistic Regression).  
   - Evaluated model accuracy and feature importance.  

5. **Insights & Recommendations:**  
   - Identified zones with potential urban stress indicators.  
   - Proposed sustainability-driven strategies for city planning and health management.

---

## Key Findings
- Strong correlation between healthcare accessibility and city population density.  
- Urban areas with lower greenery index show higher predicted health risks.  
- Predictive models achieved approximately 86% accuracy in identifying high-risk zones.  
- Overpass Turbo integration enabled real-time map visualization of analyzed city sectors.  

---

## Files in This Repository
- `urban_city_analysis.ipynb` – Main Jupyter notebook with code and visualizations  
- `data/` – Contains datasets used for analysis  
- `plots/` – Generated charts and map visuals  
- `report.pdf` – Summary of insights and model performance  

---

## Future Scope
- Integrate satellite imagery for enhanced spatial predictions.  
- Develop a Streamlit dashboard for interactive urban analytics.  
- Incorporate live IoT or weather data streams for real-time monitoring.

---

## References
- [Overpass Turbo API Documentation](https://overpass-turbo.eu/)  
- [OpenStreetMap](https://www.openstreetmap.org/)  
- [Brain Stroke CT Dataset – Kaggle](https://www.kaggle.com/)  

---

© 2025 Vipin Mishra | Urban City Analysis | MCA Data Science Project
