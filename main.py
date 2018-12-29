from chi_calculator import ChiCalculator
from data_extract import extract_data
from data_plotter import make_linear_min_chi2_plot
from headers_extract import extract_headers

def fit_linear(input_file, fit_interval=0):
    with open(input_file) as data_file:
        file_data = data_file.readlines()

    empty_line_index = file_data.index("\n")
    data_lines = file_data[0:empty_line_index]
    headers_lines = file_data[empty_line_index:]

    try:
        data = extract_data(data_lines)
        print(data)
        x_header, y_header = extract_headers(headers_lines)

        chi_calc = ChiCalculator(x=data['x'],
                                 dx=data['dx'],
                                 y=data['y'],
                                 dy=data['dy'])
        a, da, b, db, chi_squared, chi_squared_red = chi_calc.get_linear_min_chi_squared()

        output = "a = {0} +- {1} \n\nb = {2} += {3} \n\nchi2 = {4} \n\nchi2_reduced = {5}\n"\
            .format(a, da, b, db, chi_squared, chi_squared_red)

        make_linear_min_chi2_plot(data, a, b, x_header, y_header, fig_num=fit_interval)
    except Exception as ex:
        # raise
        output = str(ex)

    print(output)
