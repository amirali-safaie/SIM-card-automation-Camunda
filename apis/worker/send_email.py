from pyzeebe import ZeebeWorker, create_secure_channel
import grpc
import asyncio
import requests

token_url = "http://identity:8084/realms/camunda-platform/protocol/openid-connect/token"
data = {"grant_type": "client_credentials", "client_id": "zeebe", "client_secret": "zecret", "audience": "zeebe-api"}

resp = requests.post(token_url, data=data)
resp.raise_for_status()
access_token = resp.json()["access_token"]
print("Token fetched successfully")

credentials = grpc.metadata_call_credentials(lambda context, callback: callback([("authorization", f"Bearer {access_token}")], None))
channel = create_secure_channel("localhost", 26500, channel_credentials=grpc.composite_channel_credentials(grpc.ssl_channel_credentials(), credentials))

worker = ZeebeWorker(channel)

@worker.task(task_type="send_email")
def send_email(national_code: str, mail_type="confirmation"):
    print(f"email sent to {national_code}")
    return {"status": "SENT"}

async def main():
    await worker.work()

if __name__ == "__main__":
    asyncio.run(main())
