# Power BI Dashboard Setup Guide for ConcussionGPT (CSV Flow for Mac)

This guide walks you through exporting data from Azure SQL, visualizing it via CSV, and creating a blog-ready dashboard using Power BI — fully compatible with macOS.

---

## 🛠 Step 1: Export Data to CSV

1. Open the script `dashboard/export_to_csv.py`
2. Replace `DB_URL` with your Azure SQL connection string
3. Run the script in VS Code terminal:
   ```bash
   python dashboard/export_to_csv.py
   ```
4. This will create a file `incident_data_export.csv` in your local directory

---

## 📊 Step 2: Visualize in Power BI Web (app.powerbi.com)

1. Go to [https://app.powerbi.com](https://app.powerbi.com) and sign in
2. Click **Workspaces > My Workspace > New Report > Upload a File**
3. Upload your `incident_data_export.csv`
4. Choose "Auto-create report" or click **+ New Report** to build your own

### Use SQL Queries to Build Charts
Refer to the SQL queries in `dashboard/powerbi_queries.sql` to guide your chart building:
- These queries define how data should be grouped and summarized
- In Power BI, use the **Fields panel** to manually recreate these aggregations using drag-and-drop or DAX (Power BI formulas)

Example:
- For the "Incidents by Sport" bar chart:
  - Use `sport_type` as axis
  - Use `Count of sport_type` or `Count of incident_id` as value
- For "Avg Days to Clearance":
  - Create a new measure: `AvgDays = AVERAGE(DATEDIFF([injury_date], [timestamp], DAY))`

### Suggested Charts
- **Bar Chart**: Incidents by Sport
- **Stacked Bar**: Diagnosed vs Not Diagnosed by Age Group
- **Line Chart**: Incidents Over Time
- **Pie Chart**: Cleared vs Still Symptomatic
- **Card/Box**: Avg Days to Clearance (create as a custom measure)

### Combine Into One Dashboard
1. After creating charts, save each as a visual in the report
2. Arrange them all onto **one Power BI page** (drag and resize as needed)
3. Use headings, separators, and layout spacing for a clean design

---

## 📸 Step 3: Export for Blog

1. With your dashboard open, click **File > Export > PDF**
2. Or use your Mac's screenshot tool to capture the full page
3. Embed the export into your blog post

---

## 🧠 Tips
- Add chart titles and axis labels
- Use color to group by outcome, age, or sport
- Align charts and avoid clutter to improve blog-readiness

You're now ready to create a clean, blog-ready dashboard on concussion insights — even from a Mac!

---

*Created by ProductPod – 2025-05-15*