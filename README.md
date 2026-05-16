<div align="center">

# Movielens-End-To-End-Data-Pipeline

### From raw CSV files to a Power BI dashboard — built with a modern data stack

<br/>

<!-- ── TOOL ICONS — replace each src path with your downloaded PNG ── -->
<table>
  <tr>
    <td align="center">
      <img width="60" height="60" alt="amazon-s3-svgrepo-com" src="https://github.com/user-attachments/assets/a406d595-7cf3-4d38-b5fe-9f2f778bb8e7" /><br/>
      <sub><b>AWS S3</b></sub>
    </td>
    <td align="center" width="30"></td>
    <td align="center">
      <img width="60" height="60" alt="snowflake-data-cloud-icon" src="https://github.com/user-attachments/assets/fee697ae-fba9-4d21-b9b8-4a60f45cafe9" /><br/>
      <sub><b>Snowflake</b></sub>
    </td>
    <td align="center" width="30"></td>
    <td align="center">
       <img width="60" height="60" alt="dbt-icon" src="https://github.com/user-attachments/assets/f1cebf7e-3f51-4165-87eb-c5616c332ce2" /><br/>
      <sub><b>dbt</b></sub>
    </td>
    <td align="center" width="30"></td>
    <td align="center">
      <img width="60" height="60" alt="Microsoft-Power-Bi--Streamline-Svg-Logos" src="https://github.com/user-attachments/assets/bb34e1a7-949b-4183-ad0e-66b034b6e75f" /><br/>
      <sub><b>Power BI</b></sub>
    </td>
  </tr>
</table>

<br/>

![Star Schema](https://img.shields.io/badge/Star_Schema-✓-2f9e44?style=flat-square)
![Medallion Architecture](https://img.shields.io/badge/Medallion_Architecture-Bronze_·_Silver_·_Gold-gold?style=flat-square)
![dbt tests](https://img.shields.io/badge/dbt_tests-passing-2f9e44?style=flat-square)
![dbt models](https://img.shields.io/badge/dbt_models-14-FF694B?style=flat-square&logo=dbt&logoColor=white)

</div>

---

## 📌 Overview

This project builds a complete end-to-end data pipeline using the [MovieLens dataset](https://grouplens.org/datasets/movielens/) — a well-known dataset containing 20+ millions of movie ratings, tags, and genome scores.

The pipeline follows the **Medallion Architecture** (Bronze → Silver → Gold), ingesting raw CSV files through **AWS S3** into **Snowflake**, transforming them with **dbt**, and delivering a **Power BI** dashboard for business insights.

---

## 🏗️ Architecture Diagram

<div align="center">

  <img width="1692" height="930" alt="diagram" src="https://github.com/user-attachments/assets/7c591f0b-a946-41a4-bfba-e59fff65b97f" />


*End-to-end pipeline: CSV → S3 → Snowflake → dbt → Power BI*

---

## 🥉🥈🥇 Medallion Architecture

| Layer | Storage | What happens |
|-------|---------|--------------|
| 🥉 **Bronze** | AWS S3 + `MOVIELENS.RAW` | Raw files loaded as-is — no transformation, original column names and types |
| 🥈 **Silver** | `MOVIELENS.STAGING` + `MOVIELENS.ANALYTICS` | Renamed columns, type casting, surrogate keys, business logic |
| 🥇 **Gold** | `MOVIELENS.ANALYTICS` (marts) | Pre-aggregated, dashboard-ready tables |

---
##  STAR SCHEMA DIAGRAM

<img width="3989" height="2911" alt="star_schema" src="https://github.com/user-attachments/assets/34297cd9-17b8-45ec-8031-66e5c8b109a0" />

---

<div align="LEFT">
  
## ❄️ Snowflake Setup

Run all steps in a Snowflake Worksheet as `ACCOUNTADMIN`.

1. **Create a role** for dbt transformations and grant it to `ACCOUNTADMIN`
2. **Create a warehouse** and grant operate permissions to the role
3. **Create a dbt service user** with the role as default and set `TYPE=LEGACY_SERVICE`
4. **Create the database and schemas** for each layer of your pipeline
5. **Grant permissions** on the database, all schemas, and future tables to the role
6. **Create an external stage** pointing to your s3 bucket with the required credentials
7. **Create your raw tables** in the RAW schema matching your source file structure
8. **Load data** using `COPY INTO` for each table from the stage

---


## 📊 Power BI Dashboard

<img width="1325" height="885" alt="DASHBOARD" src="https://github.com/user-attachments/assets/720189df-954b-4215-9ef9-d88a2b543233" />

---


  
## 🚀 How to Run

**Prerequisites:** Snowflake account with `MOVIELENS.RAW` loaded · dbt Core installed (`pip install dbt-snowflake`) · credentials in `~/.dbt/profiles.yml`

```bash
# Clone the repo
git clone https://github.com/Ahmed-Hassan111/movielens-end-to-end-project.git
cd movielens-end-to-end-data-pipeline

# Install packages
dbt deps

# Verify connection
dbt debug

# Build all models
dbt run

# Run all tests
dbt test

# View documentation and lineage
dbt docs generate && dbt docs serve
```

**Full pipeline in one command:**
```bash
dbt deps && dbt snapshot && dbt run && dbt test
```



## 📁 Project Structure

```bash
.
├── models/
│   ├── staging/        # Raw data 
│   ├── dim/            # Dimension tables 
│   ├── fct/            # Fact tables 
│   ├── bridge/         # Bridge tables (handling many-to-many relationships)
│   ├── mart/           # Final business-ready data models (Gold layer)
│   ├── sources.yml     # Source definitions (raw data locations)
│   └── schema.yml      # Tests, documentation, and model metadata
│
├── powerbi/            # Power BI dashboards and reports
│
├── dbt_project.yml     # dbt project configuration
├── packages.yml        # dbt package dependencies
├── README.md           # Project documentation
```


<div align="center">


## 👨‍💻 Author

**Ahmed Hassan**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)]([https://linkedin.com/in/abdallahahmed7](https://www.linkedin.com/in/ahmed-hassan-dataeng/))

**Collaborate with**

**Abdallah Ahmed**
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/AbdallahAhmed7)
**Mohamed Ashraf**
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/mohamedashraf1012)


</div>
