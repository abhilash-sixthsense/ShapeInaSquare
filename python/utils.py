import os


backup_file_path = "/tmp/stop_shape"  # Replace with the path to the file you want to check


def is_stop_flag_on():
    if os.path.exists(backup_file_path):
        print("Stop flag found, stopping.")
        print("Deleting the stop flag")
        os.remove(backup_file_path)
        return True
    else:
        print(f"To stop create a file at {backup_file_path} , \n touch {backup_file_path}")
        return False


def get_file_size_in_gb(file_path):
    file_size_bytes = os.path.getsize(file_path)

    # Convert bytes to gigabytes
    file_size_gb = file_size_bytes / (1024**3)
    return file_size_gb
