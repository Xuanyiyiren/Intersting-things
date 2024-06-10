# the peak_fitting function written in peak_fitting.py
def peak_fitting(data,prominence,xdata = None ,peak_type='gaussian',
                plotting = True, ax = None, datafmt='-', fitfmt='-',
                **peakfinding_params):
    '''
    data: 1D array, the data to be fitted
    prominence: float, the prominence of peaks, used by scipy.find_peaks()
    xdata: 1D array, the x-axis data, default is None, if None, use np.arange(len(data))
    peak_type: str, the type of peak to be fitted, default is 'gaussian', options are 'gaussian', 'lorentzian', 'voigt'
    peakfinding_params: dict, parameters used by scipy.find_peaks()

    ax: matplotlib.axes.Axes, the axes to plot the data and peaks, default is None, if None, create a new figure
    datafmt: str, the format of data plot, default is '-' but other people prefer 'o'
    fitfmt: str, the format of fitted data plot, default is '-'

    return:
        if plotting == True:
            return a tuple, lmfit.model.ModelResult object, the result of the fitting and the number of peaks
        else:
            return a tuple, the lmfit.model.ModelResult object and ax.
    '''
    import numpy as np
    from scipy.signal import find_peaks
    if xdata is None:
        xdata = np.arange(len(data))
    # print(len(data))
    peaks,info = find_peaks(data,prominence=prominence,**peakfinding_params)
    # print(peaks)
    # print(info)
    peak_number = len(peaks)
    corrected_left_bases = []
    corrected_right_bases = []
    for i in range(peak_number):
        # Left_bases correction
        if i>0:
            if info['left_bases'][i]<peaks[i-1]:
                corrected_left_bases.append(info['right_bases'][i-1])
            else:
                corrected_left_bases.append(info['left_bases'][i])
        else:
            corrected_left_bases.append(info['left_bases'][i])
        # Right_bases correction
        if i<peak_number-1:
            if info['right_bases'][i]>peaks[i+1]:
                corrected_right_bases.append(info['left_bases'][i+1])
            else:
                corrected_right_bases.append(info['right_bases'][i])
        else:
            corrected_right_bases.append(info['right_bases'][i])
    corrected_left_bases = np.array(corrected_left_bases)
    corrected_right_bases = np.array(corrected_right_bases)


    if peak_type[0] in ['g','G']:
        from lmfit.models import GaussianModel
        peak_models = [GaussianModel(prefix=f'G{i}_') for i in range(peak_number)]
    elif peak_type[0] in ['l','L']:
        from lmfit.models import LorentzianModel
        peak_models = [LorentzianModel(prefix=f'L{i}_') for i in range(peak_number)]
    elif peak_type[0] in ['v','V']:
        from lmfit.models import VoigtModel
        peak_models = [VoigtModel(prefix=f'V{i}_') for i in range(peak_number)]
    total_model = peak_models[0]
    for i in range(1,peak_number):
        total_model += peak_models[i]

    from lmfit import Parameters
    params = Parameters()
    for i in range(peak_number):
        params.update(peak_models[i].guess(data[corrected_left_bases[i]:corrected_right_bases[i]],
                                           xdata[corrected_left_bases[i]:corrected_right_bases[i]]))
    if peak_type[0] in ['v','V']:
        for i in range(peak_number):
            params[f'V{i}_gamma'].set(value = 0.7,vary=True,min = 0)

    fitresult = total_model.fit(data,params,x=xdata)
    if plotting:
        print(f'{peak_number} peaks found.')
        if ax == None:
            ax = fitresult.plot_fit(datafmt = '-')
        else:
            fitresult.plot_fit(ax=ax,datafmt = '-')
        return fitresult,peak_number,ax
    else:
        return fitresult,peak_number