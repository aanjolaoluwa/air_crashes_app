# **Air Crashes Data Analysis & Visualization App**

An interactive **Streamlit** web application for exploring and analyzing global air crash data.  
The project combines **data cleaning, exploratory data analysis (EDA)** in Jupyter Notebook, and an intuitive dashboard to uncover trends, patterns, and insights on air accidents worldwide.

---

## 📂 Project Structure
├── air_crashes_cleaned_data.xlsx # Cleaned dataset of global air crashes

├── aircrahes_analysis.ipynb # Jupyter Notebook for data exploration & analysis

├── app.py # Streamlit dashboard application

├── requirements.txt # text file containing all libaries used


---

## 📊 Dataset Overview

- **Rows:** 5,035  
- **Columns:** 15  
- **Time Span:** Multiple decades of global air crash records  

**Key Columns:**
- `Year`, `Quarter`, `Month`, `Day`
- `Country/Region`, `Country`
- `Aircraft Manufacturer`, `Aircraft`
- `Location`, `Operator`
- `Ground`, `Fatalities (air)`, `total_fatalities`
- `Aboard`, `Survivors`

The dataset contains air fatalities, ground fatalities, and survival counts, enabling a comprehensive analysis of crash severity and patterns.

---

## 📈 Features & Analysis

The app and notebook provide:

1. **Dynamic Filtering** — Filter data by **Year, Month, Aircraft Type, Manufacturer, Country**.
2. **Key Metrics** — View total crashes, fatalities, passengers aboard, and survivors.
3. **Trend Analysis**  
   - Crashes per year  
   - Total fatalities per year  
   - Monthly & quarterly crash patterns
4. **Correlation Insights** — Relationship between passengers aboard and survivors.
5. **Top Lists**  
   - Most crash-prone manufacturers  
   - Most frequent aircraft types in crashes  
   - Countries with highest fatalities  
   - Aircraft with most survivors
6. **Visualizations** — Built using **Altair**, **Matplotlib**, **Seaborn**, and **Squarify**:
   - Bar charts
   - Line charts
   - Scatter plots with regression lines
   - Treemaps
   - Donut chart

---

## 🔍 Key Insights from Analysis

Based on the analysis in `analysis.ipynb`, notable findings include:

- **Annual Trends:** Certain years recorded significantly higher numbers of crashes, highlighting peaks during specific decades.
- **Fatalities:** Some years also saw unusually high total fatalities (both in-air and on-ground), pointing to particularly catastrophic events.
- **Passenger Survival:** There is a positive correlation between the number of passengers aboard and survivors, though survival rates vary widely.
- **Seasonality:** Monthly and quarterly patterns suggest that certain months and quarters experience more crashes than others.
- **Geographic Impact:** A small group of countries account for the highest death tolls in recorded history.
- **Aircraft Manufacturers:** A few manufacturers dominate the list of crash-prone aircraft, possibly due to fleet size or operational history.
- **Aircraft Types:** Some aircraft models appear disproportionately often in crash records.
- **Survivorship:** Specific aircraft types have historically had the highest survivor counts, possibly due to aircraft size, design, or type of incidents.
- **Passenger Volume:** The most passenger-heavy aircraft types also align with commercial long-haul and high-capacity planes.

---

## 🛠️ Technologies Used

- **Python**
- **Pandas** — Data manipulation  
- **Matplotlib & Seaborn** — Static data visualization  
- **Altair** — Interactive visualizations  
- **Squarify** — Treemap visualizations  
- **Streamlit** — Interactive dashboard deployment  
- **Jupyter Notebook** — EDA and prototyping

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/aanjolaoluwa/air-crashes-analysis.git
cd air-crashes-analysis
```
#### 2. Install dependencies
pip install -r requirements.txt

#### 3. Run the Streamlit app (For the best experience, please view this app in Dark Mode)
streamlit run app.py

---

## ✍️ Author

Developed by Anjolaoluwa Adekomi

📧 Contact: aadekomi.2201826@stu.cu.edu.ng

🔗 GitHub: https://github.com/aanjolaoluwa/

🔗 LinkedIn: https://linkedin.com/in/anjolaoluwa-adekomi-7b2548343/

🔗 Portfolio: https://anjolaoluwadekomiportfolio.my.canva.site/




