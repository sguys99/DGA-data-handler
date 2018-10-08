import matplotlib.pyplot as plt


def show_h2_plot(date, h2):
    plt.close()
    plt.plot(date, h2, 'xr')
    plt.show()