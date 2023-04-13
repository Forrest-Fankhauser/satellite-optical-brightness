# Imports
import numpy as np
import lumos.brdf.library as brdf_library
import lumos.brdf.fit_tools
import lumos.plot.brdf as brdf_plotter
import matplotlib.pyplot as plt

# |||||||||||| Fits BRDF data to Binomial Model |||||||||||||||||
def binomial_fit(
        data_file,
        n = 1,
        m = 1,
        l1 = 1,
        l2 = 1):
    
    helper = brdf_library.BinomialHelper(n, m, l1, l2)
    N_params = helper.N_params

    def model_func(*params):
        B, C, d = helper.pack_params(*params)
        brdf = brdf_library.BINOMIAL(B, C, 0.3, l1)
        return brdf

    popt = lumos.brdf.fit_tools.fit_model(
        data_file,
        model_func,
        p0 = -1 * np.ones(N_params),
        bounds = (-1e3, 1e3))

    B, C, d = helper.pack_params(*popt)

    fig = plt.figure()
    ax = fig.gca()
    brdf_plotter.plot1D(ax, model_func(*popt))
    ax.set_title("Water BRDF")
    plt.show()

def phong_fit(data_file):

    def model_func(*params):
        Kd, Ks, n = params
        brdf = brdf_library.PHONG(Kd, Ks, n)
        return brdf

    popt = lumos.brdf.fit_tools.fit_model(
        data_file,
        model_func,
        p0 = 1 * np.ones(3),
        bounds = (0, 200))
    
    Kd, Ks, n = popt
    print(f"{Kd = :0.3f}", f"{Ks = :0.3f}", f"{n = :0.3f}")

    fig = plt.figure()
    ax = fig.gca()
    brdf_plotter.plot1D(ax, model_func(*popt), log_space = False)
    ax.set_title("Water BRDF")
    plt.show()

    # fig = plt.figure()
    # ax = plt.subplot(polar = True)
    # brdf_plotter.plot2D(ax, model_func(*popt), 70)
    # plt.show()

phong_fit("earthshine_brdf_fitting/processed_data/vegetation.csv")
