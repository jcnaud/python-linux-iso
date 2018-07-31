# Todo List

## Importantes question
- Use **schema** with lamba function or **jsonschema** to validate configuration
    - jsonschema
        - Validation niveau 1
        - Pas de chargement dans swagger mais semblable
    - schema
        - Validation niveau 2 (fonction lamba) + Modification (fonction lamba)
        - Totalement imcompatible swagger
        - Validation niveau 2 totalement incompatible swagger


## Features

### Download
- [x] Download via wget
- [ ] Verify Checksum
- [ ] Check signature

### Custom
- [x] Preseed Debian 9 with open init.rd
- [x] Preseed Debian 9 without open init.rd
- [ ] Kickstart Ubuntu


### Virtualbox
- [x] Créate/Run new VM with custom iso
- [ ] Option for configuring network


## Publication

### Code
- [ ] Define structure
- [ ] Unit test

### Documentation
- [ ]

### Other
- [x] editorconfig
- [x] LICENSE
- [ ] Packaging python
- [ ] travis





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
