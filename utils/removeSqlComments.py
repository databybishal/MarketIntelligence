import re
def remove_sql_comments(sql_text):
    """Remove -- line comments and /* */ block comments."""
    sql_text = re.sub(r'/\*.*?\*/', '', sql_text, flags=re.DOTALL)
    lines = []
    for line in sql_text.split('\n'):
        idx = line.find('--')
        if idx >= 0:
            line = line[:idx]
        if line.strip():
            lines.append(line)
    return '\n'.join(lines)
