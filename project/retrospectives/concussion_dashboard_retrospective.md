# Retrospective: ConcussionGPT Dashboard Build (May 2025)

## 🎯 Objective
Design and deliver a blog-ready Power BI dashboard using data from the ConcussionGPT app to help sport system leaders understand concussion trends across Canada.

---

## ✅ What Went Well
- **Fast Iteration**: We defined the full dashboard scope and had mock data + visuals working within an hour.
- **Test Data Generation**: `generate_mock_incidents.py` enabled a rich test dataset with realistic symptoms, ages, sports, and roles.
- **Cross-platform Adaptation**: When Power BI Desktop wasn't supported on Mac, we seamlessly pivoted to a CSV + Power BI Web flow.
- **Visual Polish**: Delivered multiple polished layouts, with labeled versions and clear KPI visuals tailored for an executive audience.
- **Documentation**: Setup guide and all artifacts were versioned under `/dashboard/` and ready for reuse or onboarding.

---

## 🤔 What Could Be Improved
- **Power BI Access Limitations**: Microsoft’s restrictions on personal accounts delayed the original Power BI Web plan.
- **Realism of Timestamps**: Some inflated `days_to_clear` values due to synthetic timestamp generation logic.
- **Export Complexity**: Converting mock data into blog-quality visuals took extra care with layout and font sizing.

---

## 💡 Lessons Learned
- MVP dashboards can be built quickly with mock data and SQL-driven logic.
- CSV-based workflows offer platform-agnostic flexibility.
- Clarity in axis labels, visual titles, and legends is crucial for non-technical audiences.

---

## 🔁 Future Recommendations
- Introduce an **AnalyticsPod** to handle data modeling, test data simulation, and executive reporting across pods.
- Add a utility to simulate return-to-play flows and timestamps more realistically.
- Build reusable dashboard templates for blog, investor, and internal reporting use cases.

---

*Prepared by ProductPod – May 2025*