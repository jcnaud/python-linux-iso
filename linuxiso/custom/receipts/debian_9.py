# coding: utf-8
import os
import time
# from jinja2 import Environment,FileSystemLoader
from jinja2 import Template

# Local import
from linuxiso.ressources.tools import run_cmd


def custom_debian_9(iso_input, iso_ouput, dir_build, context):
    """
    Transform iso Debian 9
    
    params file_iso : Name of Debian 9 iso used
    """
    # Directory to mount the iso
    dir_loopdir = dir_build+os.sep+'loopdir'
    # Directory to copy and modify the iso
    dir_cd = dir_build+os.sep+'cd'
    # Directory to copy and modify the init.rd
    dir_irmod = dir_build+os.sep+'irmod'

    file_template = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'templates',
        'preseed-Debian-9-strech-amd64-srv.cfg.j2')

    try:
        # Create build temporry directory
        os.makedirs(dir_loopdir)
        os.chdir(dir_loopdir)

        # Mount iso with 'fuseiso' and not with 'mount -o loop'
        run_cmd('fuseiso '+iso_input+' '+dir_loopdir)

        time.sleep(1)  # Important to avoid some mount latence bug

        # Copy data from iso to 'dir_cd'
        os.makedirs(dir_cd)
        os.chdir(dir_cd)
        run_cmd(
            'rsync -a -H '
            '--exclude=TRANS.TBL '
            + dir_loopdir+os.sep+' '+dir_cd)

        # Umount iso
        run_cmd('fusermount -u '+dir_loopdir)

        # Extrate Init rd
        os.makedirs(dir_irmod)
        os.chdir(dir_irmod)
        run_cmd(
            'gzip -d < '+dir_cd+'/install.amd/initrd.gz |\
            fakeroot -s ../initrd.fakeroot cpio '
            '--extract --verbose '
            '--make-directories --no-absolute-filenames')

        # Tempale of preseed
        with open(file_template) as file:
            data = file.read()
        template = Template(data)

        data_preseed = template.render(context)

        os.chdir(dir_irmod)
        with open('./preseed.cfg', 'w') as file:
            file.write(data_preseed)

        # Compress and change the init rd
        run_cmd('chmod u+w '+dir_cd+'/install.amd/initrd.gz')
        run_cmd(
            ' find . | '
            'fakeroot -i ../initrd.fakeroot cpio '
            '-H newc --create --verbose | '
            'gzip -9 > '+dir_cd+'/install.amd/initrd.gz')
        run_cmd('chmod u-w '+dir_cd+'/install.amd/initrd.gz')

        # Modification of the start menu in order to boot on preseed
        os.chdir(dir_cd)
        run_cmd("chmod u+w isolinux")
        run_cmd("sed -i 's/^default.*$/default auto/m' isolinux/isolinux.cfg")
        run_cmd("sed -i 's/^prompt.*$/prompt 1/m' isolinux/isolinux.cfg")
        run_cmd("sed -i 's/^timeout.*$/timeout 100/m' isolinux/isolinux.cfg")
        run_cmd("chmod u-w isolinux")

        # Update the file containt all md5 hash of diferent file
        os.chdir(dir_cd)
        run_cmd('chmod u+w ./')
        run_cmd('chmod u+w md5sum.txt')
        run_cmd('rm md5sum.txt')
        run_cmd('md5sum `find -follow -type f` > md5sum.txt')
        run_cmd('chmod 444 md5sum.txt')
        run_cmd('chmod u-w ./')

        # Build iso/image
        os.chdir(dir_build)
        run_cmd('chmod u+w cd/isolinux/isolinux.bin')
        run_cmd(
            'fakeroot genisoimage '
            '-o '+iso_ouput+' '
            '-r -J '
            '-no-emul-boot '
            '-boot-load-size 4 '
            '-boot-info-table '
            '-b isolinux/isolinux.bin '
            '-c isolinux/boot.cat ./cd')

        run_cmd('chmod u-w cd/isolinux/isolinux.bin')

    finally:
        # defore clean build directory
        if os.path.isdir(dir_cd):
            run_cmd('chmod -R u+rw '+dir_cd)
        if os.path.isdir(dir_loopdir):
            if os.path.ismount(dir_loopdir):
                run_cmd('fusermount -u '+dir_loopdir)


def custom_debian_9_soft(iso_input, iso_ouput, dir_build, context):
    """
    Transform iso Debian 9
    params file_iso : Name of Debian 9 iso used
    """
    # Directory to mount the iso
    dir_loopdir = dir_build+os.sep+'loopdir'
    # Directory to copy and modify the iso
    dir_cd = dir_build+os.sep+'cd'
    # Directory to copy and modify the init.rd
    dir_irmod = dir_build+os.sep+'irmod'

    file_template = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'templates',
        'preseed-Debian-9-strech-amd64-srv.cfg.j2')

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
            "label netinstall \n"
            "    menu label ^Install auto via preseed \n"
            "    menu default \n"
            "    kernel /install.amd/vmlinuz \n"
            "    append auto=true vga=normal file=/cdrom/preseed.cfg initrd=/install.amd/initrd.gz locale=fr_FR.UTF-8 console-keymaps-at/keymap=fr-latin9\n"
            "")

        run_cmd('chmod u+w isolinux/txt.cfg')
        with open("isolinux/txt.cfg", "a") as f:
            f.write(data_grub_menu)
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
        with open('./preseed.cfg', 'w') as file:
            file.write(data_preseed)
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

# xorriso -as mkisofs \
#   -r -J -V "luma-wheezy" \
#   -b isolinux/isolinux.bin \
#   -c isolinux/boot.cat \
#   -no-emul-boot \
#   -partition_offset 16 \
#   -boot-load-size 4 \
#   -boot-info-table \
#   -isohybrid-mbr "/usr/lib/syslinux/isohdpfx.bin" \
#   -o $ISOFILE_FINAL \
# ./$ISODIR_WRITE
#
#     xorriso
#     -as mkisofs \
#         -isohybrid-mbr /usr/lib/syslinux/mbr/isohdpfx.bin \
#     -c isolinux/boot.cat \
#     -b isolinux/isolinux.bin \
#     -no-emul-boot \
#     -boot-load-size 4 \
#     -boot-info-table \
#         -eltorito-alt-boot \
#         -e boot/grub/efi.img \
#     -isohybrid-gpt-basdat \
#     -o /path/to/tmp.iso \
#     /path/to/tmp
#

        # -part
        # -hard-disk-boot
        # isohybrid --uefi my-amd64.iso

        # fakeroot
        #xorriso -as mkisofs -r -J -joliet-long -l -cache-inodes -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin
        #-partition_offset 16 -A "Debian Live" -b isolinux/isolinux.bin
        #-c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o debianlive.iso image

        #https://askubuntu.com/questions/625286/how-to-create-uefi-bootable-iso

        # xorriso -as mkisofs \
        #   -isohybrid-mbr /usr/lib/syslinux/mbr/isohdpfx.bin \
        #   -c isolinux/boot.cat \
        #   -b isolinux/isolinux.bin \
        #   -no-emul-boot \
        #   -boot-load-size 4 \
        #   -boot-info-table \
        #   -eltorito-alt-boot \
        #   -e boot/grub/efi.img \
        #   -no-emul-boot \
        #   -isohybrid-gpt-basdat \
        #   -o /path/to/tmp.iso \
        #   /path/to/tmp

    finally:
        # defore clean build directory
        if os.path.isdir(dir_cd):
            run_cmd('chmod -R u+rw '+dir_cd)
        if os.path.isdir(dir_loopdir):
            if os.path.ismount(dir_loopdir):
                run_cmd('fusermount -u '+dir_loopdir)
