#!/usr/bin/env python3
import os
import shutil
import stat

def run_clean():
    # Set execution permissions for itself
    os.chmod(__file__, os.stat(__file__).st_mode | stat.S_IEXEC)

    # List of directories to remove completely
    dirs_to_remove = ['postProcessing', 'logs', 'dynamicCode']
    
    # List of patterns to remove i.e. catches processor0, processor1, etc.
    cwd = os.getcwd()
    for item in os.listdir(cwd):
        # Remove processor directories
        if item.startswith('processor') and os.path.isdir(item):
            shutil.rmtree(item)
        
        # Remove time directories (numbers), but preserves the '0' folder
        try:
            val = float(item)
            if val != 0 and os.path.isdir(item):
                shutil.rmtree(item)
        except ValueError:
            pass

    # Remove specific directories from the list
    for d in dirs_to_remove:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"Removed directory: {d}")

    # Clean the polyMesh but keep the directory structure if needed
    mesh_dir = os.path.join('constant', 'polyMesh')
    if os.path.exists(mesh_dir):
        shutil.rmtree(mesh_dir)
        print("Removed constant/polyMesh")

    # Remove stray log files in the main directory
    for file in os.listdir(cwd):
        if file.startswith('log.') or file.endswith('.log'):
            os.remove(file)

    print("Cleanup complete. '0' directory and system/constant dictionaries preserved.")

if __name__ == "__main__":
    run_clean()