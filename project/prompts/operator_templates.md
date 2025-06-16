# 🧭 Operator Prompt Templates

These reusable prompts help you collect specific data from your health portal using OpenAI Operator. After opening Operator, paste one of the templates below and follow the steps. Downloads should be saved as `portal_date_type.pdf` (e.g. `mychart_2024-05-01_lab.pdf`). Return to Copilot after each download.

---

## 📄 Visit Summary
```
1. Log in to the portal manually.
2. Go to the **Visits** or **Visit Summary** section.
3. Open the desired visit and download the summary as **PDF** (use HTML if PDF unavailable).
4. Save the file as `portal_DATE_visit.pdf` where DATE is the visit date.
5. When done, return to Copilot.
```

## 🧪 Lab Results
```
1. Log in and navigate to **Lab Results** or **Test Results**.
2. Choose the specific test and download the report as **PDF** (HTML if needed).
3. Name the file `portal_DATE_lab.pdf` using the result date.
4. Return to Copilot after the download.
```

## 💳 Billing Statements
```
1. Log in and open the **Billing** or **Statements** section.
2. Locate the statement you need and download it as **PDF**.
3. Save the file as `portal_DATE_bill.pdf`.
4. Once saved, return to Copilot.
```

## 📦 All Records (Optional)
```
1. After logging in, search for an **Export** or **Download All Records** option.
2. Request an export in **PDF** format if available, otherwise use HTML.
3. Save the file as `portal_DATE_all.pdf`.
4. Return to Copilot when complete.
```

## ❓ CSV Export
Operator cannot generate CSV files directly. Save the page as HTML or print to PDF,
then convert it locally or copy the table content manually.
