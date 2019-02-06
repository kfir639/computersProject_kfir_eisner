# ==================== Main Part - fit linear =======================
def fit_linear(input_file, fit_interval=0, is_bonus_file=False):
    with open(input_file) as data_file:
        file_data = data_file.readlines()

    # Get the different sections of the input file
    data_lines, headers_lines, bonus_lines = get_sections(file_data, is_bonus_file)

    try:
        # Extract data from the raw lines
        data = extract_data(data_lines)
        x_header, y_header = extract_headers(headers_lines)

        chi_calc = ChiCalculator(x=data['x'],
                                 dx=data['dx'],
                                 y=data['y'],
                                 dy=data['dy'])

        if is_bonus_file:
            # Calculate numerically
            a, da, b, db, chi_squared, chi_squared_red, \
                lowest_chi2_a_list, lowest_chi2_as_func_of_a = chi_calc.get_numeric_min_chi(bonus_lines)

            # Plot Chi2 as func of a for the best value of b
            make_fit_of_chi2_as_a_func_of_a(lowest_chi2_a_list, lowest_chi2_as_func_of_a, b, fig_num=fit_interval)
        else:
            # Calculate by analytically
            a, da, b, db, chi_squared, chi_squared_red = chi_calc.get_linear_min_chi_squared()

        output = "a = {0} +- {1} \n\nb = {2} +- {3} \n\nchi2 = {4} \n\nchi2_reduced = {5}\n"\
            .format(a, da, b, db, chi_squared, chi_squared_red)

        # Plot function with minimized chi2
        make_linear_min_chi2_plot(data, a, b, x_header, y_header, fig_num=fit_interval)
    except DataInvalidException as ex:
        output = str(ex)

    print(output)
# ==================== END: Main Part - fit linear =======================


# ==================== Bonus Function =======================
def search_best_parameter(filename):
    fit_linear(filename, is_bonus_file=True)
# ==================== END: Bonus Function =======================


# ==================== Data - Extraction ====================
def get_sections(file_data, get_bonus_lines=False):
    empty_line_index = file_data.index("\n")
    data_lines = file_data[0:empty_line_index]
    headers_lines = file_data[empty_line_index:empty_line_index+2]

    bonus_lines = None
    if get_bonus_lines:
        second_empty_line_index = file_data.index("\n", empty_line_index+1)
        bonus_lines = file_data[second_empty_line_index+1:]

    return data_lines, headers_lines, bonus_lines


COLUMNS_DATA_HEADERS = sorted(["x", "dx", "y", "dy"])

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
    return sorted(data_matrix[0]) == COLUMNS_DATA_HEADERS

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
        raise DataInvalidException("Input file error: Data lists are not the same length.")

    # Check that all uncertainties values are positive
    for key in ["dx", "dy"]:
        if not all([number > 0 for number in extracted_data[key]]):
            raise DataInvalidException("Input file error: Not all uncertainties are positive.")

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

# This is a special Exception for our unique validations
class DataInvalidException(Exception): pass
# ==================== END: Data - Extraction ====================


# ==================== Chi-Calculator ====================
import math
import numpy as np

class ChiCalculator():

    def __init__(self, x, dx, y, dy):
        self.x = x
        self.dx = dx
        self.y = y
        self.dy = dy

        self.N = len(x)
        self.dy_sum_of_squares = sum([1/(dy_i**2)for dy_i in self.dy])
        self.x_avg = self._get_avg(self.x)
        self.x_squared_avg = self._get_avg([x_i**2 for x_i in self.x])
        self.y_avg = self._get_avg(self.y)
        self.xy_avg = self._get_avg([self.x[i]*self.y[i] for i in range(self.N)])
        self.dy_squared_avg = self._get_avg([dy_i**2 for dy_i in self.dy])

    def _get_avg(self, data_array):
        return sum([data_array[i]/(self.dy[i]**2) for i in range(self.N)]) / self.dy_sum_of_squares

    def get_linear_min_chi_squared(self):
        a = ( self.xy_avg - self.x_avg*self.y_avg ) / ( self.x_squared_avg - self.x_avg**2 )
        da = math.sqrt(
            self.dy_squared_avg / (self.N * ( self.x_squared_avg - self.x_avg**2 ))
        )

        b = self.y_avg - a * self.x_avg
        db = math.sqrt(
            self.dy_squared_avg * self.x_squared_avg / (self.N * ( self.x_squared_avg - self.x_avg**2 ))
        )

        # Calculating Chi2 according to Eq. (3)
        chi_squared = sum([((self.y[i] - a*self.x[i] - b) / self.dy[i])**2 for i in range(self.N)])
        chi_squared_reduced = chi_squared / (self.N - 2)

        return a, da, b, db, chi_squared, chi_squared_reduced

    def get_numeric_min_chi(self, bonus_lines):
        a_initial, a_final, a_step = [float(i) for i in bonus_lines[0].lower().strip().split()[1:]]
        b_initial, b_final, b_step = [float(i) for i in bonus_lines[1].lower().strip().split()[1:]]

        min_chi2 =  self._calc_chi2_by_equation_1(a_initial, b_initial)
        min_a = a_initial
        min_b = b_initial

        # Calculate numerically the lowest chi2
        for a in list(np.arange(a_initial, a_final, a_step)):
            for b in list(np.arange(b_initial, b_final, b_step)):
                chi2 = self._calc_chi2_by_equation_1(a, b)
                if chi2 < min_chi2:
                    min_chi2 = chi2
                    min_a = a
                    min_b = b
        min_chi2_reduced = min_chi2 / (self.N - 2)

        # For the lowest Chi2's b parameter, calculate Chi2-as-a-func-of-a
        lowest_chi2_a_list = list(np.arange(a_initial, a_final, a_step))
        lowest_chi2_as_func_of_a = [self._calc_chi2_by_equation_1(a, min_b) for a in lowest_chi2_a_list]

        return min_a, abs(a_step), min_b, abs(b_step), min_chi2, min_chi2_reduced, \
               lowest_chi2_a_list, lowest_chi2_as_func_of_a

    def _calc_chi2_by_equation_1(self, a, b):
        # Calculating Chi2 according to Eq. (1)
        chi_squared = sum([(
                               (self.y[i] - a * self.x[i] - b) / math.sqrt(self.dy[i]**2 + (2*a*self.dx[i])**2)
                           )**2
                           for i in range(self.N)])

        return chi_squared
# ==================== END: Chi-Calculator ====================


# ==================== Data-Plotting ====================
import matplotlib.pyplot as plt

def make_linear_min_chi2_plot(data, a, b, x_header, y_header, fig_num=0):
    f_of_x = [a * x_i + b for x_i in data['x']]
    plt.figure(fig_num + 1)
    plt.plot(data['x'], f_of_x, 'r')
    plt.errorbar(data['x'], data['y'], xerr=data['dx'], yerr=data['dy'], fmt='b,')
    plt.title("Linear Min Chi^2 Plot")
    plt.xlabel(x_header)
    plt.ylabel(y_header)
    plt.savefig("linear_fit{0}.svg".format(str(fig_num + 1)))

def make_fit_of_chi2_as_a_func_of_a(a_list, chi2_of_a, min_b, fig_num=0):
    plt.figure(0)
    plt.plot(a_list, chi2_of_a, 'b')
    plt.title("Chi^2 vs a Plot")
    plt.xlabel('a')
    plt.ylabel('chi2(a,b={0})'.format(round(min_b, 2)))
    plt.savefig("numeric_sampling.svg")
# ==================== END: Data-Plotting ====================