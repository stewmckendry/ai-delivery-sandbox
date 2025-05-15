# Power BI Dashboard Setup Guide for ConcussionGPT

This guide walks you through installing Power BI, connecting it to the Azure SQL database, and building a blog-ready dashboard.

---

## 🧰 Step 1: Install Power BI Desktop

1. Go to [Power BI Desktop Download](https://powerbi.microsoft.com/desktop/)
2. Click **Download Free** and install via the Microsoft Store or EXE
3. Launch Power BI Desktop after installation

---

## 🔌 Step 2: Connect to Azure SQL Database

1. Open Power BI Desktop
2. Click **Home > Get Data > SQL Server**
3. Enter the server and database info:
   - **Server**: `concussiondbserver.database.windows.net`
   - **Database**: `concussiondb`
4. Click **Advanced options** and paste this query from your file:
   ```sql
   SELECT sport_type, COUNT(*) AS incident_count FROM incident_report_export GROUP BY sport_type;
   ```
   *(You can repeat this for each saved SQL query.)*
5. For authentication:
   - Choose **Database**
   - Username: `sqladmin`
   - Password: `shamrock201627!`
6. Click **Connect** (use encrypted connection)

---

## 📊 Step 3: Build Your Visuals

Repeat these steps for each of the 5 queries in `dashboard/powerbi_queries.sql`:

### 1. Incidents by Sport
- **Visual**: *Bar Chart*
- Fields: sport_type (X-axis), incident_count (Y-axis)

### 2. Diagnosed vs Not by Age Group
- **Visual**: *Stacked Bar*
- Fields: age_group (X), count (Y), diagnosed_concussion (Legend)

### 3. Incidents Over Time
- **Visual**: *Line Chart*
- Fields: date (X), incident_count (Y)

### 4. Clearance Outcomes
- **Visual**: *Pie Chart*
- Fields: cleared_to_play (Legend), count (Values)

### 5. Avg Days to Clearance
- **Visual**: *Card*
- Field: avg_days_to_clear

---

## 📸 Step 4: Export for Blog

1. Arrange your visuals in a 1-page layout
2. Click **File > Export > Export to PDF** or use a snipping tool to screenshot
3. Save the image and embed it in your blog post

---

## 💡 Tips for New Users
- Use **Data View** to explore raw tables
- Use **Format** panel (paint roller icon) to customize chart styles
- Use **Refresh** to update your visuals after running the data insert script

You're now set to build a clean, informative concussion dashboard for sport leaders!

---

*Created by ProductPod – 2025-05-15*