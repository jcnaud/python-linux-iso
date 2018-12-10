# Todo List


## General
- [ ] Improve config from simple to expert modification
  - [x] Simple config file with simples and minimals functions
  - [ ] Config file with advanced functions
  - [ ] Expert configuration with personnal preseed or kickstart

- [ ] Configuration validation
  - [ ] Use **schema** with lamba function or **jsonschema** to validate configuration ?
      - jsonschema
          - Validation level 1
          - No loading on swagger but look like
      - schema
          - Validation level 2 (fonction lamba) + Modification (fonction lamba)
          - Totaly uncompatible swagger
          - Validation level 2 totaly uncompatible swagger
- [x] Architecture
  - [x] Define code structure
- [ ] Unit test
  - [x] Use travis and deploy on it
  - [x] Basic tests
  - [ ] Advanced tests (full iso custom)
- [x]Documentation
  - [x] Make compilation documentation
  - [x] Deploy on readthedoc.io

- [x] LICENSE
- [ ] Packaging python

### Download
- [x] Download via wget like
- [x] Verify Checksum
- [ ] Check signature

### Custom
- Linux install supported
  - [x] Preseed Debian 9 server
  - [ ] Preseed Debian 9 server with raid+lvm
  - [x] Preseed Ubuntu 18 server
  - [ ] Preseed Ubuntu 18 desktop
  - [ ] Preseed Linux Mint 19 desktop
  - [ ] Kickstart Centos
- Linux image supported
  - [ ] Raspbian img

### Virtualbox
- [x] Create/Run new VM with custom iso
- [ ] Option for configuring network
