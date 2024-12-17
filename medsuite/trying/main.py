# import usb.core
import usb.util
import usb.core
import libusb
print(libusb.context)

dev = usb.core.find(find_all=True , backend=libusb )

for i, e in enumerate(dev):
    print(i,e)

# for d in dev:
#     print(1)
#     print(f"device:{d.idVendor}:{d.idProduct}")