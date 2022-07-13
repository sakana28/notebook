---
date created: 2022-07-13 10:22
---

#SD

[专栏-使用Vivado Block Design 进行逻辑设计 ZYNQ器件(FPGA培训视频，ZYNQ开发，VIVADO开发，FPGA视频课，V3学院)_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1u4411P7pL?p=8)

[FatFs - Generic FAT Filesystem Module](http://elm-chan.org/fsw/ff/00index_e.html)
FatFs 官网
Zynq PS端 SD卡的驱动

### 提供的API函数:

#### f_mount 挂载

The f_mount fucntion gives work area to the FatFs module.

```c
FRESULT f_mount (
  FATFS*       fs,    /* [IN] Filesystem object */
  const TCHAR* path,  /* [IN] Logical drive number */
  BYTE         opt    /* [IN] Initialization option */
);

FRESULT f_unmount (
  const TCHAR* path   /* [IN] Logical drive number */
);

```

##### Parameters

- fs
  Pointer to the filesystem object to be registered and cleared. Null pointer unregisters the registered filesystem object.

- path
  Pointer to the null-terminated string that specifies the [logical drive](http://elm-chan.org/fsw/ff/doc/filename.html). The string without drive number means the default drive.

- opt
  Mounting option. 0: Do not mount now (to be mounted on the first access to the volume), 1: Force mounted the volume to check if it is ready to work.

返回FRESULT 要有操作对象 只声明一个指针FATFS相当一个空地址，没有指向一个实体。
const TCHAR* path 是逻辑分区编号 SD卡只有一个分区
opt 填0代表最初挂载 填1代表已经挂载，强制再次挂载

```C
    fs = malloc(sizeof (FATFS));
```

分配内存函数

挂载好逻辑分区后可以读写

#### f_open

The f_open function opens a file.

```c
FRESULT f_open (
  FIL* fp,           /* [OUT] Pointer to the file object structure */
  const TCHAR* path, /* [IN] File name */
  BYTE mode          /* [IN] Mode flags */
);
```

##### Parameters

- fp
  Pointer to the blank file object structure.

- path
  Pointer to the null-terminated string that specifies the [file name](http://elm-chan.org/fsw/ff/doc/filename.html) to open or create.

- mode
  Mode flags that specifies the type of access and open method for the file. It is specified by a combination of following flags.
![[Pasted image 20220713102225.png]]
常用w+x
读时不要开CREATE ALWAYS 否则文件永远会被覆盖

#### f_lseek
移动读写指针 常用 zb移动到初始位置进行写

The f_lseek function moves the file read/write pointer of an open file object. It can also be used to expand the file size (cluster pre-allocation).


``` c
FRESULT f_lseek (
  FIL*    fp,  /* [IN] File object */
  FSIZE_t ofs  /* [IN] Offset of file read/write pointer to be set */
);

FRESULT f_rewind (
  FIL*    fp   /* [IN] File object */
);
```
####  f_write
 The f_write writes data to a file.

```c

FRESULT f_write (
  FIL* fp,          /* [IN] Pointer to the file object structure */
  const void* buff, /* [IN] Pointer to the data to be written */
  UINT btw,         /* [IN] Number of bytes to write */
  UINT* bw          /* [OUT] 实际写入SD卡字节的数量Pointer to the variable to return number of bytes written */
);
```
