# coding: utf-8
import os
import time
# from jinja2 import Environment,FileSystemLoader
from jinja2 import Template

# Local import
from linuxiso.ressources.tools import run_cmd


def generate_option_file(template_name, context, output_file):
    """
    Generate preseed or kickstart file
    """
    template_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'templates',
        template_name)

    # Template render with context
    with open(template_file) as file:
        data = file.read()
    template = Template(data)

    data_option = template.render(context)

    # Write file
    with open(output_file, 'w') as file:
        file.write(data_option)

def custom_ubuntu_18(iso_input, iso_ouput, dir_build, receipt, context):
    """
    Transform iso Ubuntu 18
    params file_iso : Name of Ubuntu 18
    """
    # Directory to mount the iso
    dir_loopdir = dir_build+os.sep+'loopdir'
    # Directory to copy and modify the iso
    dir_cd = dir_build+os.sep+'cd'
    # Directory to copy and modify the init.rd
    dir_irmod = dir_build+os.sep+'irmod'

    try:
        # == Mount iso on loopdir
        os.makedirs(dir_loopdir)
        os.chdir(dir_loopdir)

        run_cmd('fuseiso '+iso_input+' '+dir_loopdir)
        #run_cmd('mount -o loop '+iso_input+' '+dir_loopdir)
        time.sleep(1)  # Important to avoid some mount latence bug

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
            "    menu label ^Install auto via preseed \n"
            "    menu default \n"
            "    kernel /install/vmlinuz \n"
            "    append auto=true vga=normal file=/cdrom/preseed.cfg initrd=/install/initrd.gz console-setup/ask_detect=false keyboard-configuration/xkb-keymap=fr\n"
            "")
        # data_grub_menu = ("\n"
        #     "default autoinstall \n"
        #     "label autoinstall \n"
        #     "    menu label ^Automatically install Ubuntu \n"
        #     "    kernel /install/vmlinuz\n"
        #     "    append vga=788 ks=cdrom:/ks.cfg initrd=/install/initrd.gz locale=fr_FR.UTF-8 console-keymaps-at/keymap=fr-latin9 quiet ---\n"
        #     "")

        with open("isolinux/txt.cfg") as f:
            s = f.read()
        s = s.replace('default install', data_grub_menu)

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

        # == Kickstart
        os.chdir(dir_cd)
        run_cmd('chmod u+w .')
        file_template = generate_option_file(
            receipt['template'],
            context,
            './preseed.cfg')
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
        os.chdir(dir_build)
        run_cmd('chmod u+w cd/isolinux/isolinux.bin')
        #run_cmd('fakeroot genisoimage -o '+iso_ouput+os.sep+file_iso+' -r -J -no-emul-boot -boot-load-size 4 \
        #    -boot-info-table -b isolinux/isolinux.bin -c isolinux/boot.cat ./cd')
        run_cmd(
            'xorriso -as mkisofs \
            -r -J \
            -c isolinux/boot.cat \
            -b isolinux/isolinux.bin \
            -no-emul-boot \
            -partition_offset 16  \
            -boot-load-size 4 \
            -boot-info-table \
            -joliet-long -l -cache-inodes \
            -A "Custom Debian 9 soft" \
            -isohybrid-gpt-basdat \
            -isohybrid-mbr "/usr/lib/ISOLINUX/isohdpfx.bin" \
            -o '+iso_ouput+' \
            ./cd')
        run_cmd('chmod u-w cd/isolinux/isolinux.bin')

    finally:
        # defore clean build directory
        if os.path.isdir(dir_cd):
            run_cmd('chmod -R u+rw '+dir_cd)
        if os.path.isdir(dir_loopdir):
            if os.path.ismount(dir_loopdir):
                run_cmd('fusermount -u '+dir_loopdir)
