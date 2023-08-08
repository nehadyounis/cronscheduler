A Cron scheduler in Python
This is my attempt to implement an in-process cron scheduler that accepts a job and executes it periodically. 

## Requirements
Clients should be able to specify:

- A single run expected interval, e.g. `30m`.
- Scheduling frequency, e.g. `1hr` for a job that should run every one hour.
- The job implementation, e.g. a function.
- A unique job identifier.

## Solution
This is a Python package that can schedule tasks and execute them in parallel at specific times, as well as logging all the jobs that have been done.

### Usage
To use this solution, import Scheduler to the project
```python
from scheduler import Scheduler
```

Then initialize a scheduler, add jobs to it, and put it to run, that's it.

```python
def print_hi():
    print('Hi')
    
s = Scheduler()
s.add_job(print_hi, identifier="job_hi", frequency='10s', max_times=5)
s.run()
```


You can set jobs intervals using two methods, the first is determining a frequency for the job using `frequency` attribute

```python
s.add_job(print_hi, identifier="job_hi1", frequency='10s') #Executes every 10 seconds, infinite number of times
s.add_job(print_hi, identifier="job_hi2", frequency='10s', max_times=5) #Executes every 10 seconds for 5 times.
s.add_job(print_hi, identifier="job_hi3", frequency='1m', max_times=5) #Executes every 1 minute for 5 times.
s.add_job(print_hi, identifier="job_hi4", frequency='3h3m10s') #Executes every 3 hours 30 minutes 10 seconds, infinite number of times
s.add_job(print_hi, identifier="job_hi5", frequency='1d', max_times=5) #Executes every day for 5 times.
```

Or you can use Cron Syntax to specify when the job shall be executed

```python
s.add_job(print_hi, identifier="hi1", cron="0 0 12 * * ?") #Fire at 12:00 PM (noon) every day
s.add_job(print_hi, identifier="hi2", cron="0 10,44 14 ? 3 WED") #Fire at 2:10 PM and at 2:44 PM every Wednesday in the month of March
s.add_job(print_hi, identifier="hi3", cron="0 0 12 1/5 * 2022,2023") #Fire at 12 PM (noon) every 5 days every month, starting on the first day of the month, years 2022 and 2023
s.add_job(print_hi, identifier="hi4", cron="0 15 10 ? * MON-FRI") #Fire at 10:15 AM every Monday, Tuesday, Wednesday, Thursday and Friday
```

Expected execution time can be added as an optional argument
```python
s.add_job(print_hi, identifier="job_hi1", frequency='10s', expected_time='1s')
```
Logging can be found in the file intervals.log, for example, this code produces the following log

```python
def print_hi():
    time.sleep(2) # hypothetical execution time
    print(f'Hi')
    return "I said hi"

if __name__ == '__main__':
    s = Scheduler()
    s.add_job(print_hi, identifier="job_hi", frequency='5s', max_times=5, expected_time="1s")
    s.run()
```

```log
02/12/2022 05:30:30: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
02/12/2022 05:30:35: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
02/12/2022 05:30:40: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
02/12/2022 05:30:45: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
02/12/2022 05:30:50: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
```


Some additional functions
```python
s.num_of_jobs() #returns the number of jobs this scheduler is currently executing
s.jobs_ids() # returns a list of job identifiers
s.kill_all() # deletes all the jobs
s.stop() #stops the schedule from doing any further jobs.
```


## Some Q&A

### Why are there two different ways to initiate a job (frequency or cron syntax)?
Frequency intervals are commonly used and easy to understand, yet it doesn't provide the full potential that can be easily provided by a cron syntax. Despite that fact, the cron syntax is sometimes over-complicated for certain tasks. Thus, each method has its own use cases.

### How was concurrency achieved?
By threading, The scheduler checker (that determines which job to execute now), is running on its own thread. Furthermore, each job runs on its own thread too.



