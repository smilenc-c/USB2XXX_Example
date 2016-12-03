"""
文件说明：USB2XXX ADC相关函数测试程序
更多帮助：www.usbxyz.com
"""
from ctypes import *
import platform
from time import sleep
from usb_device import *
from usb2spi import *


if __name__ == '__main__': 
    DevIndex = 0
    # Scan device
    ret = USB_ScanDevice(0)
    if(ret == 0):
        print("No device connected!")
        exit()
    else:
        print("Have %d device connected!"%ret)
    # Open device
    ret = USB_OpenDevice(DevIndex)
    if(bool(ret)):
        print("Open device success!")
    else:
        print("Open device faild!")
        exit()
    # Get device infomation
    USB2XXXInfo = DEVICE_INFO()
    USB2XXXFunctionString = (c_char * 256)()
    ret = USB_GetDeviceInfo(DevIndex,byref(USB2XXXInfo),byref(USB2XXXFunctionString))
    if(bool(ret)):
        print("USB2XXX device infomation:")
        print("--Firmware Name: %s"%bytes(USB2XXXInfo.FirmwareName).decode('ascii'))
        print("--Firmware Version: v%d.%d.%d"%((USB2XXXInfo.FirmwareVersion>>24)&0xFF,(USB2XXXInfo.FirmwareVersion>>16)&0xFF,USB2XXXInfo.FirmwareVersion&0xFFFF))
        print("--Hardware Version: v%d.%d.%d"%((USB2XXXInfo.HardwareVersion>>24)&0xFF,(USB2XXXInfo.HardwareVersion>>16)&0xFF,USB2XXXInfo.HardwareVersion&0xFFFF))
        print("--Build Date: %s"%bytes(USB2XXXInfo.BuildDate).decode('ascii'))
        print("--Serial Number: ",end='')
        for i in range(0, len(USB2XXXInfo.SerialNumber)):
            print("%08X"%USB2XXXInfo.SerialNumber[i],end='')
        print("")
        print("--Function String: %s"%bytes(USB2XXXFunctionString.value).decode('ascii'))
    else:
        print("Get device infomation faild!")
        exit()
    # Initialize spi
    SPIConfig = SPI_CONFIG()
    SPIConfig.Mode = SPI_MODE_SOFT_HDX      # 硬件半双工模式
    SPIConfig.Master = SPI_MASTER    # 主机模式
    SPIConfig.CPOL = 0
    SPIConfig.CPHA = 0
    SPIConfig.LSBFirst = SPI_LSB
    SPIConfig.SelPolarity = SPI_SEL_LOW
    SPIConfig.ClockSpeedHz = 500000
    ret = SPI_Init(DevIndex,SPI2_CS0,byref(SPIConfig))
    if(ret != SPI_SUCCESS):
        print("Initialize spi faild!")
        exit()
    else:
        print("Initialize spi success")
    # SPI write bits
    ret = SPI_WriteBits(DevIndex,SPI2_CS0,b"10110100100101")
    if(ret != SPI_SUCCESS):
        print("SPI write bits faild!")
        exit()
    else:
        print("SPI write bits success!")
    
    # SPI read bits
    ReadBuffer = create_string_buffer(b"\0"*10240)
    ret = SPI_ReadBits(DevIndex,SPI2_CS0,ReadBuffer,20)
    if(ret != SPI_SUCCESS):
        print("SPI read bits faild!")
        exit()
    else:
        print("SPI read bits:")
        print(ReadBuffer.value)
        print("")
    # SPI write read bits
    ret = SPI_WriteReadBits(DevIndex,SPI2_CS0,b"10110100100101",ReadBuffer,10)
    if(ret != SPI_SUCCESS):
        print("SPI write&read bits faild!")
        exit()
    else:
        print("SPI write&read bits:")
        print(ReadBuffer.value)
        print("")
    # Close device
    ret = USB_CloseDevice(DevIndex)
    if(bool(ret)):
        print("Close device success!")
    else:
        print("Close device faild!")
        exit()
