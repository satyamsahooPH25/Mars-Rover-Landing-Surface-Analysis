import open3d as o3d
import multiprocessing as mp

def show_point_cloud(file_path, title):
    pcd = o3d.io.read_point_cloud(file_path)
    o3d.visualization.draw_geometries([pcd], window_name=title)

if __name__ == '__main__':
    # Define file paths and window titles
    image_file = "./preprocessed_images/images_020.ply"
    depth_file = "./preprocessed_depth/depth_020.ply"

    # Create two processes for the visualizations
    p1 = mp.Process(target=show_point_cloud, args=(image_file, "Image Point Cloud"))
    p2 = mp.Process(target=show_point_cloud, args=(depth_file, "Depth Point Cloud"))

    # Start the processes
    p1.start()
    p2.start()

    # Optionally, wait for both to finish
    p1.join()
    p2.join()
