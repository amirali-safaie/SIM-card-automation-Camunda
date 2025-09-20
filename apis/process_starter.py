import asyncio
from pyzeebe import ZeebeClient, create_insecure_channel

async def main():
    channel = create_insecure_channel(grpc_address="localhost:26500")
    client = ZeebeClient(channel)

    # Use 'await' to run the process and wait for the result
    await client.run_process("Process_0lw1eff")
    print("Process started successfully!")

if __name__ == "__main__":
    # Use asyncio.run() to execute the main async function
    asyncio.run(main())