import datetime

def get_time(dt):
    now = datetime.datetime.now(datetime.timezone.utc)
    time = now - dt
    sec = time.total_seconds()
    day = divmod(sec, 24*60*60)[0]
    hour = divmod(sec, 60*60)[0] - day*24
    mins = divmod(sec, 60)[0] - hour*60
    sec = sec - mins*60
    return day, hour, mins, sec

def select_time_to_show(day, hour, mins, sec):
    if(day<1):
        if(hour<1):
            if(mins<1):
                return str(int(sec))+' seconds ago'
            return str(int(mins))+' mins ago'
        return str(int(hour))+' hour ago'
    return str(int(day))+' day ago'