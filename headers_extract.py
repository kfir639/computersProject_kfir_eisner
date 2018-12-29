X_HEADER_PREFIX = "x axis:"
Y_HEADER_PREFIX = "y axis:"

def extract_headers(headers_lines):
    x_header = None
    y_header = None

    for i, line in enumerate(headers_lines):
        line = line.lower().strip()
        if line.startswith(X_HEADER_PREFIX):
            x_header = headers_lines[i][len(X_HEADER_PREFIX):].strip()
        elif line.startswith(Y_HEADER_PREFIX):
            y_header = headers_lines[i][len(Y_HEADER_PREFIX):].strip()

    return x_header, y_header