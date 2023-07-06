import httpx
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash

@task(retries=4, retry_delay_seconds=1)
def try_again():
    log = get_run_logger()
    result = httpx.get("https://httpstat.us/Random/200,500", verify=False)
    if result.status_code >= 400:
        log.info("Failed")
        raise Exception()
    log.info(result.text)


@task(retries=4, retry_delay_seconds=0.1)
def fetch_cat_fact():
    log = get_run_logger()
    cat_fact = httpx.get("https://f3-vyx5c2hfpq-ue.a.run.app/")
    if cat_fact.status_code >= 400:
        raise Exception()
    log.info(cat_fact.text)

@task(retries=4, retry_delay_seconds=0.1, cache_key_fn=task_input_hash)
def fetch_weather(lat: float, lon: float):
  base_url = "https://api.open-meteo.com/v1/forecast/"
  weather = httpx.get(
    base_url,
    params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
  )
  most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
  return most_recent_temp


@flow
def fetch():
    log = get_run_logger()
    fetch_cat_fact()
    weather = fetch_weather(39.7589,84.1916)
    log.info(str(weather))
    try_again()

if __name__ == "__main__":
    fetch()