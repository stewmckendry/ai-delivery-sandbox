# No-op formatter for now – fields already normalized by API utils

def format_results(results: list) -> list:
    # Passthrough – already normalized to:
    # title, snippet, url, source, date
    return results