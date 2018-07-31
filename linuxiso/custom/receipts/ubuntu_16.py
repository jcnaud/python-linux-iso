# coding: utf-8
import os
import time
# from jinja2 import Environment,FileSystemLoader
from jinja2 import Template
import tempfile

# Local import
from linuxiso.ressources.tools import run_cmd


def custom_ubuntu_16_soft(iso_input, iso_ouput, dir_build, context):
    """
    Transform iso Ubuntu 16
    params file_iso : Name of Debian 16 iso used
    """

    # Create build directory
    if not os.path.isdir(dir_build):
        os.makedirs(dir_build)
    dir_build_tmp = tempfile.mkdtemp(dir=dir_build)
    dir_loopdir = dir_build_tmp + os.sep + 'loopdir'  # Directory to mount the iso
    dir_cd = dir_build_tmp + os.sep + 'cd'            # Directory to copy and modify the iso
    # dir_irmod = dir_build_tmp + os.sep + 'irmod'      # Directory to copy and modify the init.rd

    file_template = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'templates',
        'kickstart-Ubuntu-16-xenial-amd-64-desktop.cfg.j2')

    try:
        # == Mount iso on loopdir
        os.makedirs(dir_loopdir)
        os.chdir(dir_loopdir) # Important

        run_cmd('fuseiso '+iso_input+' '+dir_loopdir)
        #run_cmd('mount -o loop '+iso_input+' '+dir_loopdir)

        time.sleep(1) # Important to avoid some mount latence bug

        # == Copy iso to cd
        os.makedirs(dir_cd)
        os.chdir(dir_cd)
        #run_cmd('7z x '+iso_input)
        run_cmd('rsync -a -H --exclude=TRANS.TBL '+dir_loopdir+os.sep+' '+dir_cd)

        # == Umount iso
        run_cmd('fusermount -u '+dir_loopdir)
        #run_cmd('umount '+dir_loopdir)

        # == Custom grub menu
        os.chdir(dir_cd)
        data_grub_menu = ("\n"
            "default autoinstall \n"
            "label autoinstall \n"
            "    menu label ^Automatically install Ubuntu \n"
            "    kernel /install/vmlinuz\n"
            "    append vga=788 ks=cdrom:/ks.cfg initrd=/install/initrd.gz locale=fr_FR.UTF-8 console-keymaps-at/keymap=fr-latin9 quiet ---\n"
            "")
        s = open("isolinux/txt.cfg").read()
        s = s.replace('default install', data_grub_menu)

        #"    append auto=true vga=normal file=/cdrom/preseed.cfg initrd=/install.amd/initrd.gz locale=fr_FR.UTF-8 console-keymaps-at/keymap=fr-latin9\n"
        run_cmd('chmod u+w isolinux/txt.cfg')
        with open("isolinux/txt.cfg", "w") as f:
            f.write(s)
        run_cmd('chmod u-w isolinux/txt.cfg')

        # == Menu start modification
        os.chdir(dir_cd)
        run_cmd("chmod u+w isolinux")
        #run_cmd("sed -i 's/^default.*$/default auto/m' isolinux/isolinux.cfg")
        #run_cmd("sed -i 's/^prompt.*$/prompt 1/m' isolinux/isolinux.cfg")
        run_cmd("sed -i 's/^timeout.*$/timeout 100/m' isolinux/isolinux.cfg")
        run_cmd("chmod u-w isolinux")

        # == Tempale preseed
        with open(file_template) as file:
            data = file.read()
        template = Template(data)

        data_preseed = template.render(context)

        os.chdir(dir_cd)
        run_cmd('chmod u+w .')
        with open('./ks.cfg','w') as file:
            file.write(data_preseed)
        run_cmd('chmod 644 ./ks.cfg')
        run_cmd('chmod u-w .')

        # == Rebuild md5
        os.chdir(dir_cd)
        run_cmd('chmod u+w ./')
        run_cmd('chmod u+w md5sum.txt')
        run_cmd('rm md5sum.txt')
        run_cmd('md5sum `find -follow -type f` > md5sum.txt')
        run_cmd('chmod 444 md5sum.txt')
        run_cmd('chmod u-w ./')

        # == Create image
        os.chdir(dir_build_tmp)
        run_cmd('chmod u+w cd/isolinux/isolinux.bin')
        run_cmd('fakeroot genisoimage -o '+iso_ouput+' -r -J -no-emul-boot -boot-load-size 4 \
            -boot-info-table -b isolinux/isolinux.bin -c isolinux/boot.cat ./cd')
        #-boot-info-table


    finally:
        # == Big clean ==
        if os.path.isdir(dir_cd):
            run_cmd('chmod -R u+rw '+dir_cd)
            #run_cmd('rm -r '+dir_cd)
        if os.path.isdir(dir_loopdir):
            if os.path.ismount(dir_loopdir):
                run_cmd('fusermount -u '+dir_loopdir)
            #run_cmd('rm -r '+dir_loopdir)
