# Data_analytics_projects
This repository demonstrates my ability to build data pipelines and statistical tools using both **Python** and **Shell Scripting**.

## 📂 Projects Overview

| Project | Type | Description |
| :--- | :--- | :--- |
| **1. Social Media Demographics** | Python | Analyzes user data to correlate age with income and segment usage by demographic (Urban/Rural). |
| **2. Engagement Statistics** | Python | A comparative study of engagement scores between "Students" and "Non-students" using statistical variance and pooled standard deviation. |
| **3. Global Tobacco Analysis** | Bash | A CLI tool to query WHO data trends by gender, year, and country using Unix tools. |
| **4. Happiness Predictors** | Bash | An ETL pipeline that merges GDP and Health data to find the strongest predictor of national happiness. |

---

## 🐍 Python Projects
*Demonstrating algorithmic logic and statistical implementation in pure Python.*

### 1. Social Media Demographics Analysis
This tool processes raw CSV data to uncover insights about user behavior based on age and location.
- **Key Features:**
  - **Demographic Segmentation:** Aggregates time spent and income data across Rural, Urban, and Sub-urban groups.
  - **Correlation Algorithms:** Manually implements Pearson correlation formulas to measure the relationship between **Age** and **Income** for specific platforms.
  - **Data Filtering:** Custom functions to slice data by Country and Age Group.

### 2. User Engagement Comparative Study
A statistical analysis tool that compares how different professions (Student vs. Non-Student) engage with digital content.
- **Key Features:**
  - **Metric Calculation:** Computes a composite "Engagement Time" metric based on hours spent and engagement scores.
  - **Statistical profiling:** Calculates Mean, Variance, and Standard Deviation from scratch without using libraries like NumPy.
  - **Pooled Deviation:** Determines the `Pooled Standard Deviation` to compare variability across different profession groups.

---

## 🐚 Bash / Shell Projects
*Focusing on CLI automation and text processing.*

### 3. Global Tobacco Control Analysis
**File:** `tobacco_nation.sh`
A command-line utility that queries World Health Organization (WHO) datasets.
- **Functionality:** Instantly finds the country with the highest tobacco usage for any given year or gender without opening Excel.
- **Tech:** Uses `grep`, `sort`, and pipe chaining for rapid data extraction.

### 4. Global Happiness & GDP Analysis
**File:** `cantril_data_cleaning`, `best_predictor`
An end-to-end **ETL (Extract, Transform, Load)** pipeline.
- **Pipeline:**
  1. **Clean:** Normalizes headers and merges three distinct datasets (GDP, Homicide Rate, Life Expectancy).
  2. **Analyze:** Mathematically determines which factor has the highest correlation with the "Cantril Ladder" (Happiness Score).

---

## 💻 Tech Stack

- **Languages:** Python, Bash (Shell)
- **Concepts:** ETL Pipelines, Statistical Analysis (Correlation, Variance), Unix Streams
