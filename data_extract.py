
COLUMNS_DATA_HEADERS = ["x", "dx", "y", "dy"]

def extract_data(data_lines):
    data_matrix = [line.lower().strip().split(" ") for line in data_lines]

    if is_columns_data(data_matrix):
        extracted_data = extract_col_data(data_matrix)
    else:
        extracted_data = extract_row_data(data_matrix)

    # Convert data from strings to floats
    for key, val in extracted_data.items():
        extracted_data[key] = [float(number) for number in val]

    validate_data(extracted_data)

    return extracted_data

def is_columns_data(data_matrix):
    return data_matrix[0] == COLUMNS_DATA_HEADERS

def extract_col_data(data_matrix):
    extracted_data = {}

    for col in range(len(data_matrix[0])):
        col_data = []
        for row in range(1, len(data_matrix)):
            try:
                col_data.append(data_matrix[row][col])
            except IndexError:
                # An exception is thrown here on invalid length of data
                # We will validate and handle that later
                pass

        extracted_data[data_matrix[0][col]] = col_data

    return extracted_data

def extract_row_data(data_matrix):
    extracted_data = {}

    for row in range(len(data_matrix)):
        extracted_data[data_matrix[row][0]] = data_matrix[row][1:]

    return extracted_data

def validate_data(extracted_data):
    # Get all the arrays' length from each data column into a Set
    data_arrays_length_set = {len(data_array) for data_array in extracted_data.values()}

    # If all data arrays are in the same length, the Set will be of length 1.
    if len(data_arrays_length_set) > 1:
        raise Exception("Input file error: Data lists are not the same length.")

    # Check that all uncertainties values are positive
    for key in ["dx", "dy"]:
        if not all([number > 0 for number in extracted_data[key]]):
            raise Exception("Input file error: Not all uncertainties are positive.")

