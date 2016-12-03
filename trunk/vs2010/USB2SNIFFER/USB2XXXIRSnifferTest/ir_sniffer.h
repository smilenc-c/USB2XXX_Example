/**
  ******************************************************************************
  * @file    ir_sniffer.h
  * $Author: wdluo $
  * $Revision: 447 $
  * $Date:: 2013-06-29 18:24:57 +0800 #$
  * @brief   ir sniffer相关函数和数据类型定义.
  ******************************************************************************
  * @attention
  *
  *<center><a href="http:\\www.usbxyz.com">http://www.usbxyz.com</a></center>
  *<center>All Rights Reserved</center></h3>
  * 
  ******************************************************************************
  */
#ifndef __IR_SNIFFER_H_
#define __IR_SNIFFER_H_

#include <stdint.h>
#ifndef OS_UNIX
#include <Windows.h>
#else
#include <unistd.h>
#ifndef WINAPI
#define WINAPI
#endif
#endif

#define DECODE_WINDOW_SIZE  4

typedef struct _IRTimeSeries{
  int   DataTime;//输出DataType的时间，单位为0.25us
  char  DataType;//1-输出高电平或者调制波，0-输出低电平或者不输出调制波
}IRTimeSeries,*PIRTimeSeries;

//解析到I2C数据后的回调函数
typedef  int (WINAPI IR_GET_DATA_HANDLE)(int DeviceIndex,int Channel,PIRTimeSeries pIRData,int IRDataNum);

//定义函数返回错误代码
#define SUCCESS             (0)   //函数执行成功
#define ERR_NOT_SUPPORT     (-1)  //适配器不支持该函数
#define ERR_USB_WRITE_FAIL  (-2)  //USB写数据失败
#define ERR_USB_READ_FAIL   (-3)  //USB读数据失败
#define ERR_CMD_FAIL        (-4)  //命令执行失败

#ifdef __cplusplus
extern "C"
{
#endif
	int WINAPI IR_SnifferStart(int DevIndex,int Channel,unsigned int SampleRateHz,IR_GET_DATA_HANDLE *pGetIRDataHandle);
	int WINAPI IR_SnifferStop(int DevIndex);
#ifdef __cplusplus
}
#endif

#endif
