DROP TABLE IF EXISTS structured_records;
CREATE TABLE structured_records (
    id INTEGER PRIMARY KEY,
    portal VARCHAR,
    type VARCHAR,
    clinical_type VARCHAR,
    code VARCHAR,
    code_system VARCHAR,
    display VARCHAR,
    text TEXT,
    source_url VARCHAR,
    session_key VARCHAR DEFAULT NULL,
    source VARCHAR DEFAULT 'operator',
    capture_method VARCHAR DEFAULT '',
    user_notes VARCHAR DEFAULT '',
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP
);
