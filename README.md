# yshttl

a command-line tool that can:

0.  exploit a bug in the yonsei shuttle booking system
1.  auto-book yonsei shuttle based on a schedule
2.  book shuttles before the official booking hour
3.  make long term booking reservations (the program remembers to book in your stead)
4.  show booked shuttles
5.  cancel booked shuttles (not implemented yet in ver. 2.2)

## dependencies

### you need to run these before first launch:

```
pip install google-auth-oauthlib
pip install bs4
pip install google-api-python-client
pip install rsa
pip install rich
```

## how to use

run yshttl.py with python 3.11 or newer. use CLI to operate the program.

use command "help" to get started.

## configuration file values explanation:

**_(its a json file that is automatically created on first launch)_**

note that the configuration file contains configurations for multiple users.

### primary settings (the rest is set automatically)

every user entry should be registered in this format:

```
"USER_XX": {
    "ALIAS": "ALIAS",
    "USERID": "20YYYYYYYY",
    "USERPW": "PASSWORD"
}
```

- ALIAS stands for the name that you want to use to address the user.
- where XX stands for a user's index with a leading zero.
- 20YYYYYYYY stands for the user's student id.
- PASSWORD stands for the user's portal password.

### secondary settings (touch if you know what you are doing)

- **REFRESH_RATE_CLOCK**: _float_  
  time inbetween refreshes of clock thread  
  default: 0.25

- **REFRESH_RATE_SHTTL_LST**: _float_  
  time inbetween refreshes of shuttle list  
  default: 30.0

- **BOOK_TIME**: _string_  
  a string which is formatted to: "h m s" (hour minute second)
  this is the time at which schedule bookings will happen in bulk  
  default: "0 2 0" (12:02:00 AM)

- **DAYS_FROM_START**: _int_  
  how many days worth of schedule-drivven bookings should
  be done on startup  
  default: 7

- **AUTH_SESSION_LENGTH**: _float_  
  authentication session length  
  default: 300.0

- **EMAIL_SERVER**: _bool_
  defines whether the emailserver should be turned on
  default: false

### developer settings

- **DEBUG**: _bool_  
  defines whether the program should run in debug mode  
  default: false
- **CLEAN_SCHEDULE**: _bool_  
  if set to true schedule will be overridden to a clean schedule  
  default: false

- **IGNORE_3DAYS**: _bool_  
  if set to true first 3 days of schedule from start date will ignored  
  default: true

## schedule file format:

**_this is an example schedule (its a json file that is automatically created on first launch)_**

note that schedules should follow exactly this format! (each user has its own schedule)

```
{
    "USER_00": {
        "0": [
            {
                "origin": "S",
                "time": "09:30",
                "mode": "l"
            }
        ],
        "1": [
            {
                "origin": "S",
                "time": "07:40",
                "mode": "l"
            },
            {
                "origin": "I",
                "time": "17:20",
                "mode": "r"
            },
            {
                "origin": "I",
                "time": "17:30",
                "mode": "r"
            }
        ],
        "2": [
            {
                "origin": "S",
                "time": "09:30",
                "mode": "l"
            }
        ],
        "3": [],
        "4": [
            {
                "origin": "I",
                "time": "15:00",
                "mode": "l"
            },
            {
                "origin": "I",
                "time": "12:00",
                "mode": "l"
            },
            {
                "origin": "I",
                "time": "18:00",
                "mode": "l"
            }
        ],
        "5": [],
        "6": []
    }
}
```

### explanaiton:

this schdule will book the following shuttles for USER_01:

1.  on monday (day of the week 0) from **S**inchon at available times BEFORE (mode = l) 9:30
2.  on tuesday (day of the week 1) from **S**inchon at available times BEFORE (mode = l) 7:30
3.  on tuesday (day of the week 1) from **I**nternational at available times AFTER (mode = r) 17:20
4.  ....and so on

## authors

- [@spicymuffin](https://github.com/spicymuffin)
