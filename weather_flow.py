import httpx
from prefect import task, flow
from prefect.tasks import task_input_hash

# Queries from a DB can be cached !!!
@task(retries=2, retry_delay_seconds=0.5, persist_result=True) #cache_key_fn=task_input_hash,
def fetch_weather(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    # breakpoint()
    temps = weather.json()["hourly"]["temperature_2m"]
    # print(f"Most recent temp C: {most_recent_temp} degrees")
    return temps

@flow(retries=2, retry_delay_seconds=1, persist_result=True)
def display_temps():
    temps = fetch_weather(39, -77.0)
    for i in temps:
        print(i)

if __name__ == "__main__":
    display_temps()
