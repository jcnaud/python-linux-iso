# Python linux iso

## Overviews
This programme provide a way to **deploy**, full **automatically**, from **scratch** an OS.
The second goal of this project is to never use linux root access to make this.

This programme have **three** parts :
 - download
 - custom
 - virtual box

Actually, you can custom:
 - debian 9
 - unbuntu 16 (UNDER TEST)
 - unbuntu 17 (UNDER TEST)

Each part can be use independently in different way like :
 - bash terminal
 - python module

This programme use python 3.5.4+

## Installation

This programme works only on **linux distribution**.

To avoid using root access, we need some tools for mount, unmount and build iso.

### Linux
For example, on debian, install theses paquages
```bash
apt-get install xorriso virtualbox
```
### Python
This programme use python 3.5.4+
A strongly advice you to use **virtualenv**.

Install virtualenv
```bash
apt-get install virtualenv
```

Mouv to the directory of the project and create virtualenv
```bash
cd python-linux-iso/
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -t requirements.txt
deactivate
```

pip install module
python setup.py install


## Run unit test

```
pip install pytest
```




## Principe

### Politique des modules

- Système de configuration
  - Avoir une configuration par défaut. Ex: .yaml, .json
  - Pouvoir charger la configuration manuellement. Ex: .yaml, .json, dict
  - Pouvoir charger la configuration via un programme Ex: .yaml, .json, dict
- Interactivité
  - Etre autonome à l'utilisation. Ex: Appel via ligne de command bash
  - Etre connectable via des standards de communication. Ex: API REST avec Swagger 3.0
- HA - Haute disponibilité
  - Configuration mise à jour à chaud sans perte. Ex: signal HUP comme "service xx restart"
  - Code mise à jour à chaud sans perte. Ex: signal HUP comme "service xx restart"
  - Multi host full support (Différent de MAster Slave). Ex: Zookeeper
- UX - User Expérience
  - Avoir un système de log de type (log4j)
  - Envoie des log vers un system de reception de données
- CI/DI - Intégration continue/Déploiement continue
  - Code comité avec système de version
  - Déploiement en mode service standalone automatisé. Ex: Ansible
  - Déploiement virutalisé. Ex: Docker, VM, ..
- Scalabilité
  - Exécution multi coeur sur une même machine
  - Exécution multi host
  - Ajout ou diminution du nombre de host et ou coeur
- Robustesse
  - Testable avec environnement fictif
  - Rétro compatible avec la version précédente

## Installation automatique

Non automatisable via ansible lors d'une installation, mais reconfigurable via ansible.
- Parametres par défaut d'installation. Ex: les paramètres par défault présent dans le preesed de Debian
- Paramétrage du réseau. Ex: les paramètres par défault présent dans le preesed de Debian
- Ajout et parametrage de l'utilisateur ansible
- Instalation des paquets standard de communication. Ex: ssh

Cas avec un DHPC/DNS sur le réseau.
- Nécessite de fixer l'IP lors de l'installation

Cas sans accès à un dépôt de paquets
- Blocage de l'intallation

Cas sans accès NTP.
- Problème de connexion avec le serveur de temps


### Automatisable via ansible

Contraintes minimal
- Réseau configuré
- Service ssh installé
- User ansible utilisable
- Accès à un dépôt de paquets

## TODO
 - introduction
 - tutorial
 - API reference (docstrings)
 - Developper documentation
 - Use sphinx
 - Deploy in ReadTheDocs

## CHANGELOG
- nothing


## Usage example

Simple server:
```bash
python custom.py -c Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso
python virtualbox.py -c testdeploy -e Debian-amd64-standard -i /home/jnaud/var/isocustom/Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso
python virtualbox.py -r testdeploy
```
  #   python custom.py -c Custom-FullAuto-Debian-9-strech-amd64-netinst-server-proliant.iso

    #   python virtualbox.py -c testdeploy -e Debian-amd64-standard -i /home/jnaud/var/isocustom/Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso
    #   python virtualbox.py -r testdeploy

    #   python virtualbox.py -c proliant -e Debian-amd64-raid -i /home/jnaud/var/isocustom/Custom-FullAuto-Debian-9-strech-amd64-netinst-server-proliant.iso
