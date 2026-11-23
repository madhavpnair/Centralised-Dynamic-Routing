import h5py
import numpy as np

file_path = './data/raw/fixed_sensor_data.h5'

with h5py.File(file_path, 'r') as f:
    # Print all groups and datasets inside the file
    def print_structure(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"Dataset: {name} | Shape: {obj.shape} | Type: {obj.dtype}")
        else:
            print(f"Group: {name}")
            
    f.visititems(print_structure)
    
    # Access a specific dataset's values
    data = f['metadata/features'][:]  # Loads data into a NumPy array
    print("\nFirst 5 values:\n", data[:5])
