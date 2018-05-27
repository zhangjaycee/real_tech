# 存储设备/接口/传输协议


## 1. 设备

[[distri_006_p1.png]]

最新的3D XPoint存储器比DRAM慢10倍，便宜2倍；比NAND FLASH快1000倍，贵5倍左右，性能比其他PCIe和NVMe的SSD快10倍左右。并且它是一种NVM。


下表摘自[2]

|Type|	Volatile?|	Writeable?|	Erase Size|	Max Erase Cycles|	Cost (per Byte)|	Speed|
|-|-|-|-|-|-|-|
|SRAM	|Yes	|Yes	|Byte	|Unlimited|	Expensive|	Fast|
|DRAM	|Yes	|Yes	|Byte	|Unlimited|	Moderate|	Moderate|
|Masked ROM	|No	|No|	n/a|	n/a|	Inexpensive|	Fast|
|PROM	|No	|Once, with a device programmer	|n/a|	n/a|	Moderate|	Fast|
|EPROM	|No	|Yes, with a device programmer	|Entire Chip	|Limited (consult datasheet)	|Moderate	|Fast
|EEPROM	|No	|Yes	|Byte	|Limited (consult datasheet)	|Expensive	|Fast to read, slow to erase/write|
|Flash	|No	|Yes	|Sector	|Limited (consult datasheet)	|Moderate	|Fast to read, slow to erase/write|
|NVRAM	|No	|Yes	|Byte	|Unlimited	|Expensive (SRAM + battery)|	Fast|


## 2. 接口

#### 2.1 分类和发展
```
(P)ATA(Parallel AT Attachment)/IDE(Integrated Drive Electronics) --> SATA(Serial ATA) --> mSATA(mini-SATA) --> SATAe(SATA Express)

SCSI(Small Computer System Interface) --> SAS(Serial Attached SCSI)

PCIe

NGFF(Next Generation Form Factor, M.2)
```

* mSATA / PCIe / NGFF 一般都是用于NVM(如SSD)，不用于HDD。

* mSATA慢于SATA，但是接口和体积大大减小。

* NGFF是最新的，同时比mSATA更小，也是最快的。

* SATAe接口兼容SATA和PCIe

#### 2.2 速度：

NGFF > PCIe > SAS > SATA > SCSI > ATA/IDE

## 3. 协议

IDE, AHCI和NVMe等都是传输协议，它们在传输接口(PCIe, SATA, ATA等)之上工作。

一般来说，AHCI在host chip set （**硬件中**）实现为Host Bust Adapter (HBA)。如下示意图展示了这种分层：AHCI和NVMe都在OS中有对应的driver；host chip set中，对应于设备的AHCI和PCIe的adapter被实现；最后基于PCIe或SATA物理、链路层、和传输层协议的不同的设备连入Host。[6]

[[distri_006_p2.png]]

* IDE(Integrated Drive Electronics)是IDE接口的一种“协议”，它表示磁盘控制器集成到了硬件驱动器中，无需host进行移动磁道臂等低层次的控制。

* AHCI(Advanced Host Controller Interface)一般用作SATA盘的协议，不过也有些情况SATA盘用IDE协议(老版本的Windows中默认的IDE/legacy模式就是这样)来模拟。

* SAS的协议向下兼容SATA盘。

* NVMe支持PCIe接口或者NGFF接口的盘。

下图还对比了AHCI和NVMe协议：

[[distri_006_p3.png]]


### 参考
[1] Breakthroughs in Memory Technology, http://www.intelsalestraining.com/memorytimeline/

[2] Types of Memory in Embedded Systems, https://barrgroup.com/Embedded-Systems/How-To/Memory-Types-RAM-ROM-Flash


[3] What’s the difference between SATA, PCIe and NVMe?, http://www.userbenchmark.com/Faq/What-s-the-difference-between-SATA-PCIe-and-NVMe/105

[4] https://www.intel.com/nvm

[5] Hard disk drive interface, Wikipedia, https://en.wikipedia.org/wiki/Hard_disk_drive_interface

[6] https://sata-io.org/sites/default/files/documents/NVMe%20and%20AHCI%20as%20SATA%20Express%20Interface%20Options%20-%20Whitepaper_.pdf