This is the trial information file for single tracking task outside the scanner with modifiable break (fixation) time in between trials. 

When you run create_trial_info_single_behavioral, subject number and day number are mandatory. 

To modify break time, change the trackingStart column in trial_info_single.csv. This will change when each tracking trial starts. Each trial is 13 seconds each, so if you want 5 seconds of break in between, you would put 13 + 5 = 18 seconds between each number. Assuming you want to start at 5 seconds, you would put 5, 23, 41, ...

When you run force_tracking_single_behavioral, subject number, day number, and run number are mandatory. 