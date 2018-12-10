# Temp developpement note

# Late command

d-i preseed/early_command string apt-get install curl
d-i preseed/early_command string curl -k http://service.alkante.al/newhost


# At start
/lib/systemd/system/te1.service
```
[Unit]
Description=The te1 script

[Service]
Type=oneshot
RemainAfterExit=true
ExecStart=/usr/local/bin/te1

[Install]
WantedBy=multi-user.target
```
sudo systemctl enable te1

# At stop
/lib/systemd/system/te1.service
```
[Unit]
Description=The te1 script

[Service]
Type=oneshot
RemainAfterExit=true
ExecStart=/bin/true
ExecStop=/usr/local/bin/te1

[Install]
WantedBy=multi-user.target
```
sudo systemctl enable te1

## toto Raspbian
Ne fonctionne pas :
fuseiso ../../iso/raspbian-9-strech-lite.img img

L'affichage fdisk de 2 partition
fdisk -l ../../iso/raspbian-9-strech-lite.img

```
Disque ../../iso/raspbian-9-strech-lite.img : 1,7 GiB, 1858076672 octets, 3629056 secteurs
Unités : sectors of 1 * 512 = 512 octets
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x37665771

Périphérique                          Amorçage Start     Fin Secteurs  Size Id Type
../../iso/raspbian-9-strech-lite.img1           8192   93236    85045 41,5M  c W95 FAT
../../iso/raspbian-9-strech-lite.img2          94208 3629055  3534848  1,7G 83 Linux
```
Start
- 1st partition 512 * 8192 = 4194304
- 2nd partition 512 * 94208 = 48234496

Size
- 1st partition 512 * 8192 = 43543040
- 2nd partition 512 * 94208 = 1809842176

mount -v -o offset=4194304 -t vfat ../../iso/raspbian-9-strech-lite.img img1
mount -v -o offset=48234496 -t ext4 ../../iso/raspbian-9-strech-lite.img img2



https://gist.github.com/jkullick/9b02c2061fbdf4a6c4e8a78f1312a689


https://raspberrypi.stackexchange.com/questions/855/is-it-possible-to-update-upgrade-and-install-software-before-flashing-an-image
lib piimg:
https://github.com/alexchamberlain/piimg

qemu rapberry
https://www.supinfo.com/articles/single/5429-emuler-une-raspberry-pi-linux-avec-qemu



raspberry-pi-chroot-armv7-qemu.md

# install dependecies
apt-get install qemu qemu-user-static binfmt-support



# download raspbian image
wget https://downloads.raspberrypi.org/raspbian_latest

# extract raspbian image
unzip raspbian_latest

# extend raspbian image by 1gb
dd if=/dev/zero bs=1M count=1024 >> 2016-05-27-raspbian-jessie.img

# set up image as loop device
losetup /dev/loop0 2016-05-27-raspbian-jessie.img

# check file system
e2fsck -f /dev/loop0p2

#expand partition
resize2fs /dev/loop0p2

# mount partitioncd
mount -o rw /dev/loop0p2  /mnt
mount -o rw /dev/loop0p1 /mnt/boot

# mount binds
mount --bind /dev /mnt/dev/
mount --bind /sys /mnt/sys/
mount --bind /proc /mnt/proc/
mount --bind /dev/pts /mnt/dev/pts

# ld.so.preload fix
sed -i 's/^/#/g' /mnt/etc/ld.so.preload

# copy qemu binary
cp /usr/bin/qemu-arm-static /mnt/usr/bin/

# chroot to raspbian
chroot /mnt /bin/bash
 # do stuff...
 exit

# revert ld.so.preload fix
sed -i 's/^#//g' /mnt/etc/ld.so.preload

# unmount everything
umount /mnt/{dev/pts,dev,sys,proc,boot,}

# unmount loop device
losetup -d /dev/loop0
#-----------------------------------------------------
apt-get install qemu qemu-user-static binfmt-support

# check qemu works
update-binfmts --display


# Check
fdisk -lu 2018-10-09-raspbian-stretch.img

# ???? 1G free ????
dd if=/dev/zero bs=1M count=1024 >> 2018-10-09-raspbian-stretch.img


# Check and get start and Fin multiply by 512
fdisk -lu 2018-10-09-raspbian-stretch.img

#Périphérique                     Amorçage Start     Fin Secteurs  Size Id Type
#2018-10-09-raspbian-stretch.img1           8192   97890    89699 43,8M  c W95 FAT32 (LBA)
#2018-10-09-raspbian-stretch.img2          98304 8077311  7979008  3,8G 83 Linux

8192*512 = 4194304
97890*512 = 50119680


98304 * 512 = 50331648
8077311 * 512 = 4135583232

# Mount partition
sudo losetup -v -f -o 50331648 --sizelimit 4135583232 2018-10-09-raspbian-stretch.img
sudo mount -v -t ext4 /dev/loop1 mnt
sudo losetup -v -f -o 4194304 --sizelimit 50119680 2018-10-09-raspbian-stretch.img
sudo mount -v -t vfat /dev/loop2 mnt/boot

#sudo cp /usr/bin/qemu-arm-static /mnt/rasp-pi-rootfs/usr/bin/

sudo mount --rbind /dev mnt/dev
sudo mount -t proc none mnt/proc
sudo mount -o bind /sys mnt/sys
sudo mount --bind /dev/pts mnt/dev/pts


# Some modification for chroot works
# ld.so.preload fix
sudo sed -i 's/^/#/g' mnt/etc/ld.so.preload
# Add arm bin
sudo cp /usr/bin/qemu-arm-static mnt/usr/bin


# Chroot in
cd mnt
chroot . bin/bash

# Check you are in the Chroot
uname -a

# Option : remove desktop env (for rasbian)

# Exit the Chroot
Exit
# ld.so.preload unfix
sudo sed -i 's/^#//g' mnt/etc/ld.so.preload
# Add arm bin (not necessary)
rm  mnt/usr/bin

# Clean

umount mnt/dev/pts
umount mnt/dev
umount mnt/sys
umount mnt/proc
umount mnt/boot
umount mnt



# set up image as loop device
sudo losetup /dev/loop0 2018-10-09-raspbian-stretch.img


# Verify
sudo fdisk -l /dev/loop0

# check file system
e2fsck -f /dev/loop0p2

#expand partition
resize2fs /dev/loop0p2



# unmount loop device
sudo losetup -d /dev/loop0


    sudo mount -o loop,offset=$((137216*512))  raspbian-9-strech-lite.img ./mnt
    sudo cp /usr/bin/qemu-arm-static /mnt/rasp-pi-rootfs/usr/bin/
    sudo mount --rbind /dev /mnt/rasp-pi-rootfs/dev
    sudo mount -t proc none /mnt/rasp-pi-rootfs/proc
    sudo mount -o bind /sys /mnt/rasp-pi-rootfs/sys
    sudo chroot /mnt/rasp-pi-rootfs


# ===============================================================
### Debug preseed tricks


In the future, if you face such an issue and you're not lucky enough to come across an answer that works, just go through the setup manually. On your new system, install the debconf-utils package:

 sudo apt-get install debconf-utils

This gives you access to the debconf-get-selections command. You can use it to generate a preseed configuration:

sudo debconf-get-selections --installer > preseed.cfg

You should note that, as recommended in the Debian Wiki you should not use the preseed.cfg file above as is, rather search for the entries you need (grep -i language preseed.cfg?) and add them to your own preseed file.
