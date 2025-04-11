import os
import numpy as np
import rasterio
import open3d as o3d
from tqdm import tqdm

# Directory paths
INPUT_FOLDER = "./depth"  # Change this to your folder containing .tif files
OUTPUT_FOLDER = "./preprocessed_depth"  # Change this to where you want to save point clouds

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to generate a point cloud from a depth map
def depth_to_point_cloud(depth_map, fx=1000, fy=1000, cx=None, cy=None, scale=1.0):
    """
    Convert a depth map into a 3D point cloud using pinhole camera model.

    Args:
        depth_map (np.array): Depth map (2D numpy array)
        fx (float): Focal length in x direction
        fy (float): Focal length in y direction
        cx (float): Principal point x (default: image center)
        cy (float): Principal point y (default: image center)
        scale (float): Depth scaling factor
    
    Returns:
        np.array: (N, 3) point cloud (X, Y, Z)
    """
    height, width = depth_map.shape

    # Set principal points to the image center if not provided
    if cx is None:
        cx = width / 2
    if cy is None:
        cy = height / 2

    # Create a meshgrid of pixel coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Compute X, Y, Z coordinates
    Z = depth_map * scale  # Apply scale
    X = (x - cx) * Z / fx
    Y = (y - cy) * Z / fy

    # Stack into (N, 3) format
    points = np.vstack((X.flatten(), Y.flatten(), Z.flatten())).T

    # Remove invalid points (zero depth)
    points = points[points[:, 2] > 0]  

    return points


# Process all .tif files in the input folder
for filename in tqdm(os.listdir(INPUT_FOLDER), desc="Processing TIFF files"):
    if filename.endswith(".tif"):
        file_path = os.path.join(INPUT_FOLDER, filename)
        
        # Read depth data from the .tif file
        with rasterio.open(file_path) as dataset:
            depth_map = dataset.read(1)  # Read first band

        # Convert depth map to point cloud
        point_cloud = depth_to_point_cloud(depth_map)

        # Convert to Open3D format
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_cloud)

        # Save point cloud as .ply
        output_file = os.path.join(OUTPUT_FOLDER, filename.replace(".tif", ".ply"))
        o3d.io.write_point_cloud(output_file, pcd)

        print(f"Saved point cloud: {output_file}")

print("Processing complete! All point clouds are saved.")
