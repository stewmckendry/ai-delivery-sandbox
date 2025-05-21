## WP1a Deployment Instructions – Scaffolding & Assembly

### 🔧 Prerequisites
- Python 3.8+
- `PyYAML` (for YAML parsing)

```bash
pip install pyyaml
```

---

### 🪜 Steps

#### 1. Run the Scaffolder
```bash
python app/tools/gate_section_scaffolder.py \
  --gate_id gate_01 \
  --artifact_id business_case \
  --output scaffold.json
```

#### 2. Run the Expander
```bash
python app/tools/gate_section_expander.py \
  --scaffold_path scaffold.json \
  --session_id test_session_001 \
  --output expanded.json
```

#### 3. Run the Assembler
```bash
python app/templates/final_document_assembler.py \
  --expanded_path expanded.json \
  --doc_id demo_bc_001
```

---

### 📁 Outputs
- `docs/working/demo_bc_001.md`
- `docs/working/demo_bc_001_gateblock.json`

These show markdown and structured gateblock versions of a mock policy document scaffold.