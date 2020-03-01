# ext2 / ext4 文件系统


ext2 文件系统采用间接块映射(indirect block mapping)来保存文件偏移和磁盘逻辑块之间的映射关系；ext4则采用段树映射(extent tree mapping)的方式保存映射关系。