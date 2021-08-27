# latlon-rain-forecast

## Installation

```
mkdir -p ~/git-clone
cd ~/git-clone
git clone https://github.com/vienai8d/latlon-rain-forecast.git
```

## crontab

```
*/5 * * * * python3 /home/pi/git-clone/latlon-rain-forecast/main.py '<yahooapi app_id>' <latitude> <longitude> -s '<slack_api>'
```
