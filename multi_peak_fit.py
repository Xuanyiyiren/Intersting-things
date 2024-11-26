import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel, LorentzianModel, VoigtModel

def multi_peak_fit(data, peaks, peak_type='Gaussian', xdata=None):
    """
    Fit multiple peaks in the given data using specified peak models.

    Parameters:
    -----------
    data : array-like
        The y-values of the data to be fitted.
    peaks : list of int
        Approximate positions of the peaks.
    peak_type : str, optional
        Type of peak model ('Gaussian', 'Lorentzian', 'Voigt'). Default is 'Gaussian'.
    xdata : array-like, optional
        The x-values of the data. If None, uses index.

    Returns:
    --------
    result : lmfit ModelResult object
        Contains the fitting result.
    """
    if xdata is None:
        xdata = np.arange(len(data))

    # Create individual models based on peak_type
    if peak_type == 'Gaussian':
        models = [GaussianModel(prefix=f'peak{i}_') for i in range(len(peaks))]
    elif peak_type == 'Lorentzian':
        models = [LorentzianModel(prefix=f'peak{i}_') for i in range(len(peaks))]
    elif peak_type == 'Voigt':
        models = [VoigtModel(prefix=f'peak{i}_') for i in range(len(peaks))]
    else:
        raise ValueError("Invalid peak_type. Choose 'Gaussian', 'Lorentzian', or 'Voigt'.")

    # Combine models into one composite model
    multi_peak_model = models[0]
    for model in models[1:]:
        multi_peak_model += model

    # Initialize parameters for the combined model
    params = multi_peak_model.make_params()

    # Estimate initial parameters for each peak
    for i in range(len(peaks)):
        # Determine the fitting range for each peak
        left_bound = 0 if i == 0 else (peaks[i - 1] + peaks[i]) // 2
        right_bound = len(xdata) - 1 if i == len(peaks) - 1 else (peaks[i] + peaks[i + 1]) // 2

        # Extract data segments for initial parameter estimation
        mask = (xdata >= left_bound) & (xdata <= right_bound)
        x_segment, y_segment = xdata[mask], data[mask]

        # Skip if the segment is empty
        if len(x_segment) == 0 or len(y_segment) == 0:
            continue

        # Use `guess()` to estimate initial parameters for the peak
        peak_guess = models[i].guess(y_segment, x=x_segment)
        for param_name in peak_guess:
            params[param_name] = peak_guess[param_name]

    # Fit the model to the data
    result = multi_peak_model.fit(data, params, x=xdata)
    return result

# # Generate synthetic test data with noise
# x = np.linspace(0, 100, 1000)
# y = (
#     10 * np.exp(-(x - 15)**2 / (2 * 1.5**2)) +   # First Gaussian peak
#     7 * np.exp(-(x - 40)**2 / (2 * 2.0**2)) +    # Second Gaussian peak
#     12 * np.exp(-(x - 65)**2 / (2 * 3.0**2)) +   # Third Gaussian peak
#     9 * np.exp(-(x - 85)**2 / (2 * 1.0**2)) +    # Fourth Gaussian peak
#     np.random.normal(0, 0.5, len(x))             # Add noise
# )

# # Assume `peaks` are known peak positions
# peaks = [15, 40, 65, 85]

# # Run the multi-peak fitting
# result = multi_peak_fit(y, peaks, peak_type='Gaussian', xdata=x)

# # Print fitting report
# print(result.fit_report(min_correl=0.25))

# # Plot the results
# plt.figure(figsize=(14, 7))
# plt.plot(x, y, 'b', label='Original Data')
# plt.plot(x, result.best_fit, 'r-', label='Fitted Model')
# plt.legend(loc='best')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Multi-Peak Fitting with Gaussian Models')
# plt.show()