# yshttl
 a command-line tool that can:
 1. auto-book yonsei shuttle based on a schedule
 2. book shuttles before the official booking hour
 3. make long term booking reservations (the program remembers to book in your stead)
 4. show booked shuttles
 5. cancel booked shuttles (not implemented yet in ver. 2.2)
 
 ## configuration file values explanation:
   ***(its a json file that is automatically created on first launch)***
 ### primary settings (the rest is set automatically)
 
  * **USERID**: *string*  
    yonsei portal id
    
  * **USERPW**: *string*  
    yonsei portal password

 ### secondary settings (touch if you know what you are doing)
 
  * **REFRESH_RATE_CLOCK**: *float*  
    time inbetween refreshes of clock thread  
    default: 0.25
  
  * **REFRESH_RATE_SHTTL_LST**: *float*  
    time inbetween refreshes of shuttle list  
    default: 30.0
  
  * **BOOK_TIME**: *string*  
    a string which is formatted to: "h m s" (hour minute second)
    this is the time at which schedule bookings will happen in bulk  
    default: "0 2 0" (12:02:00 AM)
                        
  * **DAYS_FROM_START**: *int*  
    how many days worth of schedule-drivven bookings should 
    be done on startup  
    default: 7
                           
  * **AUTH_SESSION_LENGTH**: *float*  
    authentication session length  
    default: 300.0
 
 ### developer settings
 
  * **DEBUG**: *bool*  
    defines whether the program should run in debug mode  
    default: false
    
  * **CLEAN_SCHEDULE**: *bool*  
    if set to true schedule will be overridden to a clean schedule  
    default: false
  
  * **IGNORE_3DAYS**: *bool*  
    if set to true first 3 days of schedule from start date will ignored  
    default: true
    
## schedule file format:
***this is an example schedule (its a json file that is automatically created on first launch)***
```
{
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
```
### explanaiton:
this schdule will book:  
 1. on monday (day of the week 0) from **S**inchon at available times BEFORE (mode = l) 9:30  
 2. on tuesday (day of the week 1) from **S**inchon at available times BEFORE (mode = l) 7:30  
 3. on tuesday (day of the week 1) from **I**nternational at available times AFTER (mode = r) 17:20  
 4. ....and so on  

## authors

- [@spicymuffin](https://github.com/spicymuffin)
