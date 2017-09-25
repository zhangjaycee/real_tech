# 存储设备/接口/传输协议


## 设备

[[distri_006_p1.png|height = 512px]]

最新的3D XPoint存储器比DRAM慢10倍，便宜2倍；比NAND FLASH快1000倍，贵5倍左右，性能比其他PCIe和NVMe的SSD快10倍左右。并且它是一种NVM。


下表摘自[2]

|Type|	Volatile?|	Writeable?|	Erase Size|	Max Erase Cycles|	Cost (per Byte)|	Speed|
|------------------------------------------------------------------------------------|
|SRAM	|Yes	|Yes	|Byte	|Unlimited|	Expensive|	Fast|
|DRAM	|Yes	|Yes	|Byte	|Unlimited|	Moderate|	Moderate|
|Masked ROM	|No	|No|	n/a|	n/a|	Inexpensive|	Fast|
|PROM	|No	|Once, with a device programmer	|n/a|	n/a|	Moderate|	Fast|
|EPROM	|No	|Yes, with a device programmer	|Entire Chip	|Limited (consult datasheet)	|Moderate	|Fast
|EEPROM	|No	|Yes	|Byte	|Limited (consult datasheet)	|Expensive	|Fast to read, slow to erase/write|
|Flash	|No	|Yes	|Sector	|Limited (consult datasheet)	|Moderate	|Fast to read, slow to erase/write|
|NVRAM	|No	|Yes	|Byte	|Unlimited	|Expensive (SRAM + battery)|	Fast|


## 接口

ATA --> SATA

SCSI --> SAS




## 协议
NVMe, AHCI和IDE等都是传输协议，它们在传输接口(PCIe, SATA等)之上工作。

### 参考
[1] Breakthroughs in Memory Technology, http://www.intelsalestraining.com/memorytimeline/

[2] Types of Memory in Embedded Systems, https://barrgroup.com/Embedded-Systems/How-To/Memory-Types-RAM-ROM-Flash


[3] What’s the difference between SATA, PCIe and NVMe?, http://www.userbenchmark.com/Faq/What-s-the-difference-between-SATA-PCIe-and-NVMe/105

[4] https://www.intel.com/nvm