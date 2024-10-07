import datetime


def load_color():
    # Determine whether it's daytime or nighttime
    current_time = datetime.datetime.now().time()
    is_daytime = current_time >= datetime.time(6, 0) and current_time <= datetime.time(19, 11)

    # Load color based on the time of day
    if is_daytime:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    return color