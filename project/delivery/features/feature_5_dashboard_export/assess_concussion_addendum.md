## 🧠 Addendum – Assessing Concussion Responsibly

This tool (`assess_concussion.py`) flags risk indicators based on structured symptom metadata in the YAML files. It does not provide a diagnosis or replace medical judgment.

### 🎯 Purpose
To help users and clinicians identify when symptom patterns may suggest a need for further clinical evaluation.

### 🛡️ Clinical Alignment
- **Red flag symptoms** (e.g., seizure, loss of consciousness) trigger urgent guidance.
- **High- and medium-risk symptoms** are scored from the user's responses.
- A concussion is *suggested*, not diagnosed, if:
  - Any red flag is present
  - Any high-risk symptom is rated ≥1
  - ≥3 medium-risk symptoms are rated ≥1

### 📋 Inputs
- `answers`: symptom_id → severity rating (0–5)
- Matches symptoms against YAML definitions from:
  - `symptoms_red_flag.yaml`
  - `symptoms_physical.yaml`
  - `symptoms_emotional.yaml`
  - `symptoms_sleep.yaml`

### 📤 Output Fields
- `concussion_likely: bool`
- `red_flags_present: List[str]`
- `high_risk_symptoms: List[str]`
- `moderate_risk_count: int`
- `summary: str` (non-diagnostic advice)

### 🗣️ Framing Language
- "This response suggests symptoms *consistent with* a potential concussion."
- "Please seek clinical evaluation."
- "No red flags... Monitor closely and consult a provider if symptoms worsen."

This framing ensures the tool supports clinical workflows without overstepping its scope.