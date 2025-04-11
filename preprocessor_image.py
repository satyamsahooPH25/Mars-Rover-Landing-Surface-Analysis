import os
import numpy as np
import rasterio
import open3d as o3d
from tqdm import tqdm

# Directory paths
INPUT_FOLDER = "./images"  # Change this to your folder containing .tif files
OUTPUT_FOLDER = "./preprocessed_images"  # Change this to where you want to save point clouds

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to generate a point cloud from a depth map
def depth_to_point_cloud(depth_map, scale=1.0):
    """
    Convert a depth map into a 3D point cloud.
    Assumes a simple pinhole camera model with an orthographic projection.
    
    Args:
        depth_map (np.array): Depth map (2D numpy array)
        scale (float): Scaling factor for depth values
    
    Returns:
        np.array: (N, 3) point cloud (x, y, depth)
    """
    height, width = depth_map.shape
    x, y = np.meshgrid(np.arange(width), np.arange(height))  # Create pixel grid

    # Flatten and stack to get (x, y, depth)
    points = np.vstack((x.flatten(), y.flatten(), depth_map.flatten() * scale)).T

    # Remove invalid depth points (if any)
    points = points[~np.isnan(points[:, 2])]  # Remove NaN values
    points = points[points[:, 2] > 0]  # Remove zero or negative depths (if any)
    
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
