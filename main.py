from bleak import BleakClient
from datetime import datetime, timezone
import asyncio

iphone_addresses = {
                    "87F4F875-2B0B-E872-6B1A-5583E3435FE9",  # Rahnng
                    "fc:66:cf:bd:6f:75" # Ryygt ???
                    } 

time_now = datetime.now(timezone.utc).strftime("%H%M%S")
date_now = datetime.now(timezone.utc).strftime("%d%m%y")
nmea_sentence = f"$GPRMC,{time_now},A,3116.0390,N,09744.5860,W,0.00,0.0,{date_now},,,*1A\r\n"

async def send_nmea_sentence(iphone_address):
    async with BleakClient(iphone_address) as client:
        try:
            await client.connect()
            print(f"Connected to iPhone at {iphone_address}")

            # Find the correct characteristic to write to
            services = await client.get_services()
            for service in services:
                for characteristic in service.characteristics:
                    if "write" in characteristic.properties:
                        # Send the NMEA sentence to this characteristic
                        await client.write_gatt_char(characteristic.uuid, nmea_sentence.encode())
                        print(f"NMEA sentence sent to {iphone_address} on characteristic {characteristic.uuid}")
        except Exception as e:
            print(f"Failed to send NMEA sentence to {iphone_address}: {e}")

async def send_to_all():
    for address in iphone_addresses:
        await send_nmea_sentence(address)

# Assuming you have an event loop to run send_to_all in an async context
# import asyncio
# asyncio.run(send_to_all())
if __name__ == "__main__":
    asyncio.run(send_to_all())