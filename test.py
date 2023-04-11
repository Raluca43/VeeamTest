#import necesary libraries
import os
import sys
import time
import filecmp
import logging

# Set up logging
logging.basicConfig(filename='sync_log.txt', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()

# Function to log messages to file and console
def log(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
    log_message = timestamp + message
    print(log_message)
    logger.info(log_message)

# Function to perform synchronization
def sync_folders(source, replica):
    log("Synchronizing folders...")
    dcmp = filecmp.dircmp(source, replica)
    for name in dcmp.left_only:
        src_path = os.path.join(source, name)
        dest_path = os.path.join(replica, name)
        if os.path.isfile(src_path):
            with open(src_path, 'rb') as src_file, open(dest_path, 'wb') as dest_file:
                dest_file.write(src_file.read())
            log(f"File created/copied: {name}")
        elif os.path.isdir(src_path):
            os.mkdir(dest_path)
            log(f"Folder created: {name}")
    for name in dcmp.right_only:
        path = os.path.join(replica, name)
        if os.path.isfile(path):
            os.remove(path)
            log(f"File removed: {name}")
        elif os.path.isdir(path):
            os.rmdir(path)
            log(f"Folder removed: {name}")
    log("Synchronization complete")

# Main function
def main():
    # Get command line arguments
    if len(sys.argv) != 5:
        print("Usage: python test.py <source_folder> <replica_folder> <sync_interval_seconds> <log_file>")
        return
    source = sys.argv[1]
    replica = sys.argv[2]
    sync_interval = int(sys.argv[3])
    log_file_path = sys.argv[4]

    # Set up log file
    try:
        logger.addHandler(logging.FileHandler(log_file_path))
    except IOError as e:
        print(f"Failed to open log file: {e}")
        return

    # Perform initial synchronization
    sync_folders(source, replica)

    # Start periodic synchronization
    while True:
        time.sleep(sync_interval)
        sync_folders(source, replica)

if __name__ == "__main__":
    main()


'''command line order in my computer:     python test.py C:/Users/Andrei/PycharmProjects/modules/images/Veeam/source C:/Users/Andrei/PycharmProjects/modules/images/Veeam/replica 60 C:/Users/Andrei/PycharmProjects/modules/images/Veeam/sync_log.txt
'''
