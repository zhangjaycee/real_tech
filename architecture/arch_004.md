## FPGA及其架构

FPGA(field programmable gate arrays)相对ASIC(application-specific integrated circuit)来说更灵活。ASIC相对来说量产后会更廉价、节能，性能也更好。

### 组成

按逻辑门的实现原理，分为三种：**基于SRAM的FPGA**、**基于flash的FPGA**和**基于反熔丝(antifuse)的FPGA**[1]。

基于SRAM的是断电易失的，所以需要在开机(startup)时通过JTAG编程，或者通过内置/外置的非易失存储进行编程。

**基于flash的FPGA**的逻辑门本身就是非易失的。**antifuse FPGA**只能编程一次，不可逆。

---
[1] https://www.pdx.edu/nanogroup/sites/www.pdx.edu.nanogroup/files/FPGA-architecture.pdf

[2] FPGAs For Dummies, https://plan.seek.intel.com/PSG_WW_NC_LPCD_FR_2018_FPGAforDummiesbook