# Task 500: Blob ETL FHIR Integration

- extend `run_etl_from_blobs` to parse labs and visits, assign codes and FHIR JSON
- update `structuring.py` insert helpers to store codes and FHIR resources
- added unit test coverage verifying FHIR data for blob ETL
- revised ETL to call an LLM for detecting labs and visits, coding them, and generating FHIR resources
