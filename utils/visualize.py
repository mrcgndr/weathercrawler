import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from .weatherfilestack import WeatherFileStack


def plotTemperature(wstack: WeatherFileStack, unit: str, feelslike: bool):
    assert unit in ["celsius", "fahrenheit"], "Unknown degree unit. Choose 'celsius' or 'fahrenheit'"

    time = [f.current.obs_datetime_loc for f in wstack.files]
    if unit == "celsius":
        T = [f.current.weather.temp.celsius for f in wstack.files]
        if feelslike:
            Tf = [f.current.weather.feelslike.celsius for f in wstack.files] 
    elif unit == "fahrenheit":
        T = [f.current.weather.temp.fahrenheit for f in wstack.files]
        if feelslike:
            Tf = [f.current.weather.feelslike.fahrenheit for f in wstack.files] 

    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    xfmt = mdates.DateFormatter('%y-%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    ax.plot(time, T, label="real")
    if feelslike:
        ax.plot(time, Tf, label="feels like")
    ax.set(title=wstack.location, ylabel=f"Temperature [{'C' if unit == 'celsius' else 'F'}]")
    ax.legend()

    return fig, ax
