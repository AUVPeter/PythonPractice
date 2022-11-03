# Dealing with Date Time

Very often we want to know what time it is, display what time it is, or process what time it is based on some data we have. Python provides the `datetime` library which handles most of what we need.

## Datetime
The most common parts of the DateTime library are the `datetime` object, and the `timezone` sub-module

~~~python
from datetime import datetime, timezone
~~~

## Displaying and formatting time
To get the computers time, we can simply request a `datetime` object representing the current time in either the timezone of the computer, or UTC, using the `now` or `utcnow` functions

~~~python
dt = datetime.now()
dt_utc = datetime.utcnow()
~~~

Once we have a `datetime` object, we can use it to display its contents in a variety of formats. 

The simplest format is the UNIX timestamp, which is a single number representing elapsed seconds since an epoch, and is a fairly standard way of storing time and allowing simple arithmetic. we access it by using the `timestamp()` function of a `datetime` object

~~~python
ts = datetime.utcnow().timestamp()
print(ts)
~~~
~~~
1667413595.278321
~~~

The 'strftime', short for 'String Format Time', is a way to define how the time should be written as text. We give it a format string and include some tags where we wish to insert various time elements. Some common ones are:

- %Y, 4 digit year
- %m, 2 digit month (01 to 12)
- %d, 2 digit day (01 to 31)
- %H, 2 digit hour (00 to 23)
- %M, 2 digit minute (00 to 59)
- %S, 2 digit second (00 to 59)
- %f, nanoseconds (000000 to 999999)

The string can have any additional text, but any character following a `%` will be treated as a format element. An example of a standard time string is

~~~python
dt = datetime.now()
print(dt.strftime('%Y-%m-%dT%H-%M-%S'))
~~~
~~~
2022-11-03T05-00-32
~~~

or more creatively
~~~python
dt = datetime.utcnow()
print(dt.strftime('The time in UTC is %f nanoseconds past %H:%M:%S'))
~~~
~~~
The time in UTC is 064404 nanoseconds past 05:22:45
~~~

## Reading and parsing date time
Often when we read data, there will be time information included which would like to parase into something useful. If it is presented as a string, we can use the `strptime', or `String Parse Time' function, which uses the same format tags as `strftime`. For example 

~~~python
date_string = "20 October, 1977 at 5:30PM"

dt = datetime.strptime(date_string, '%d %B, %Y at %I:%M%p')
print(dt)
~~~
~~~
1977-10-20 17:30:00
~~~
