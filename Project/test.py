import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import fftconvolve


def bearing_signal_model_local(d, D, contact_angle, n, fault_type, fr, fc, fd, fm, N, variance_factor, fs, k, zita, fn, Lsdof, SNR_dB, qAmpMod=1):
    def sdof_response(fs, k, zita, fn, Lsdof):
        t = np.arange(0, Lsdof / fs, 1 / fs)
        w0 = 2 * np.pi * fn
        wd = w0 * np.sqrt(1 - zita**2)
        A = 1 / (k - w0**2)
        x = A * np.exp(-zita * w0 * t) * np.sin(wd * t)
        return x

    if fault_type == 'inner':
        geometry_parameter = 1 / 2 * (1 + d / D * np.cos(contact_angle))
    elif fault_type == 'outer':
        geometry_parameter = 1 / 2 * (1 - d / D * np.cos(contact_angle))
    elif fault_type == 'ball':
        geometry_parameter = 1 / \
            (2 * n) * (1 - (d / D * np.cos(contact_angle))**2) / (d / D)

    Ltheta = len(fr)
    theta = np.arange(0, Ltheta) * 2 * np.pi / N

    delta_theta_fault = 2 * np.pi / (n * geometry_parameter)
    number_of_impulses = int(np.floor(theta[-1] / delta_theta_fault))
    mean_delta_theta = delta_theta_fault
    var_delta_theta = (variance_factor * mean_delta_theta)**2
    delta_theta_fault = np.sqrt(
        var_delta_theta) * np.random.randn(1, number_of_impulses - 1) + mean_delta_theta
    theta_fault = np.concatenate(([0], np.cumsum(delta_theta_fault)))
    fr_theta_fault = np.interp(theta_fault, theta, fr)

    delta_t_imp = delta_theta_fault / (2 * np.pi * fr_theta_fault[1:])
    t_t_imp = np.concatenate(([0], np.cumsum(delta_t_imp)))

    L = int(np.floor(t_t_imp[-1] * fs))
    t = np.arange(0, L) / fs
    fr_time = np.interp(t, t_t_imp, fr_theta_fault)

    delta_t_imp_index = np.round(delta_t_imp * fs).astype(int)
    error_delta_t_imp = delta_t_imp_index / fs - delta_t_imp

    index_impulses = np.concatenate(([1], np.cumsum(delta_t_imp_index)))
    index = len(index_impulses) - 1
    while index_impulses[index] / fs > t[-1]:
        index -= 1
    index_impulses = index_impulses[:index]

    mean_delta_t = np.mean(delta_t_imp)
    var_delta_t = np.var(delta_t_imp)
    mean_delta_t_imp_over = np.mean(delta_t_imp_index / fs)
    var_delta_t_imp_over = np.var(delta_t_imp_index / fs)

    x = np.zeros(L)
    x[index_impulses] = 1

    if fault_type == 'inner':
        if len(fc) > 1:
            theta_time = np.zeros(len(fr))
            for index in range(1, len(fr)):
                theta_time[index] = theta_time[index - 1] + \
                    (2 * np.pi / N) / (2 * np.pi * fr[index])
            fc_time = np.interp(t, theta_time, fc)
            fd_time = np.interp(t, theta_time, fd)
            fm_time = np.interp(t, theta_time, fm)

            q = 1 + qAmpMod * np.cos(2 * np.pi * fc_time * t + 2 * np.pi *
                                     fd_time * np.cumsum(np.cos(2 * np.pi * fm_time * t) / fs))
        else:
            q = 1 + qAmpMod * np.cos(2 * np.pi * fc * t + 2 * np.pi *
                                     fd * np.cumsum(np.cos(2 * np.pi * fm * t) / fs))
        x = q * x

    sdof_resp_time = sdof_response(fs, k, zita, fn, Lsdof)
    x = fftconvolve(sdof_resp_time, x)[:L]

    np.random.seed(0)
    SNR = 10**(SNR_dB / 10)
    E_sym = np.sum(np.abs(x)**2) / L
    N0 = E_sym / SNR
    noise_sigma = np.sqrt(N0)
    nt = noise_sigma * np.random.randn(L)
    x_noise = x + nt

    return (t, x, x_noise, fr_time, mean_delta_t, var_delta_t, mean_delta_t_imp_over, var_delta_t_imp_over, error_delta_t_imp)


def main():

    # Bearing geometry
    d = 21.4  # bearing roller diameter [mm]
    D = 203  # pitch circle diameter [mm]
    n = 23  # number of rolling elements
    contact_angle = 9 * np.pi / 180  # contact angle
    fault_type = 'inner'

    # Speed profile
    N = 2048  # number of points per revolution
    Ltheta = 10000 * N  # signal length
    theta = np.arange(0, Ltheta) * 2 * np.pi / N
    fc = 10
    fd = 0.08 * fc
    fm = 0.1 * fc
    fr = fc + 2 * np.pi * fd * np.cumsum(np.cos(fm * theta) / N)

    # Localized fault
    variance_factor = 0.04
    fs = 20000  # sample frequency [Hz]
    k = 2e13
    zita = 5 / 100
    fn = 6e3  # natural frequency [Hz]
    Lsdof = 2**8
    SNR_dB = 0
    qAmpMod = 0.3

    (t_local, x_local, x_noise_local, fr_time_local, mean_delta_t_local, var_delta_t_local, mean_delta_t_imp_over_local,
     var_delta_t_imp_over_local, error_delta_t_imp_local) = bearing_signal_model_local(
        d, D, contact_angle, n, fault_type, fr, fc, fd, fm, N, variance_factor, fs, k, zita, fn, Lsdof, SNR_dB, qAmpMod)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(t_local, x_noise_local)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Simulated Bearing Signal with Localized Fault')
    plt.grid()
    plt.show()
