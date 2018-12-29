import matplotlib.pyplot as plt

def make_linear_min_chi2_plot(data, a, b, x_header, y_header, fig_num=0):
    f_of_x = [a * x_i + b for x_i in data['x']]
    plt.figure(fig_num + 1)
    plt.plot(data['x'], f_of_x, 'r')
    plt.errorbar(data['x'], data['y'], xerr=data['dx'], yerr=data['dy'], fmt='b,')
    plt.title("Linear Min Chi^2 Plot")
    plt.xlabel(x_header)
    plt.ylabel(y_header)
    # plt.show()
    plt.savefig("linear_fit{0}.svg".format(str(fig_num + 1)))
