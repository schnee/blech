import asyncio
from bleak import BleakScanner, BleakClient

known_devices = {"44B5704C-8642-8CDB-001F-1E8024DAD95D",
                 "D6C7DEF1-E500-F7E3-4E56-241EE4ED17B7",
                 "4B189525-13D3-B58E-07A8-C9FA572A4902",
                 "2E755DA9-94F1-C538-8862-2E82E3EB2559",
                 "10CBC1BE-511E-4235-E7D6-EF9BD088918C",
                 "46158AE2-C83F-F5A8-0B3C-539440504E76",
                 "1AACD0AE-8134-58BB-76FE-C0EE241FC39C"
}

async def scan_ble_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name is None:
            continue
        if device.address in known_devices:
            continue
        print(f"Device: {device.name}, Address: {device.address}, RSSI: {device.rssi}")
        try:
            async with BleakClient(device) as client:
                services = await client.get_services()
                for service in services:
                    print(f"  Service UUID: {service.uuid}")
                    for char in service.characteristics:
                        print(f"   Characteristic UUID: {char.uuid}, Properties: {char.properties}")
        except Exception as e:
            print(f"Could not connect to device: {device.name}, Address: {device.address}, Error: {e}")

if __name__ == "__main__":
    asyncio.run(scan_ble_devices())
