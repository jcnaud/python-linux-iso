import logging
import re
import subprocess



def run_cmd(cmd):
    """
    Run a command
    if error, print and raise it
    params cmd : String commande
    return out
    """
    logging.debug('Run command "'+cmd+'"')
    try:
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process.check_returncode()
        
    except Exception as e:
        logging.exception(str(e) +"\nCMD_SHELL : "+cmd+"\nSTDOUT : "+process.stdout.decode()+"\nSTDERR : "+process.stderr.decode(), exc_info=True)
        #logging.critical("{CDM : "+cmd+", "} : "+cmd)
        #logging.critical("STDOUT : "+process.stdout.decode())
        #logging.critical("STDERR : "+process.stderr.decode())
        #raise e

    return process.stdout.decode()
