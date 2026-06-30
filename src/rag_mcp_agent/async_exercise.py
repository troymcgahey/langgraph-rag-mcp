import asyncio
import time

def now(start_time: float) -> str:
    elapsed = time.perf_counter() - start_time
    return f"{elapsed:0.2f}s"

async def fake_network_call(name: str, delay_seconds: int, start_time: float) -> str:
    print(f"{now(start_time)} | {name}: start")

    print(f"{now(start_time)} | {name}: waiting for {delay_seconds} seconds")
    await asyncio.sleep(delay_seconds)

    print(f"{now(start_time)} | {name}: resumed after waiting")
    return f"{name} result"

async def run_sequential() -> None:
    print("\n--- Sequential async ---")
    start_time = time.perf_counter()

    result_1 = await fake_network_call("task-1", 2, start_time)
    result_2 = await fake_network_call("task-2", 2, start_time)

    print(f"{now(start_time)} | results: {result_1}, {result_2}")

async def run_concurrent() -> None:
    print("\n --- Concurrent async ---")
    start_time = time.perf_counter()

    result_1, result_2 = await asyncio.gather(
        fake_network_call("task-1", 2, start_time),
        fake_network_call("task-2", 2, start_time),
    )

    print(f"{now(start_time)} | results: {result_1}, {result_2}")

async def main() -> None:
    await run_sequential()
    await run_concurrent()

if __name__ == "__main__":
    asyncio.run(main())
