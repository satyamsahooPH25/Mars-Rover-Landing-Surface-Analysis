import cv2
import open3d as o3d
import numpy as np
from scipy.spatial import cKDTree

# ----------------------------
# 1. Load and Downsample the Point Cloud
# ----------------------------
pcd = o3d.io.read_point_cloud("preprocessed_images\\images_020.ply")
# Choose a voxel size appropriate for your data; here we use 20.0 units
voxel_size = 20.0
pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
points = np.asarray(pcd_down.points)
print(f"Downsampled point count: {len(points)}")

# ----------------------------
# 2. Estimate Curvature on the Downsampled Point Cloud
# ----------------------------
k = 40  # number of neighbors
tree = cKDTree(points)
curvatures = np.zeros(len(points))

for i, p in enumerate(points):
    # Query k-nearest neighbors
    dist, idx = tree.query(p, k=k)
    neighbors = points[idx]
    centroid = np.mean(neighbors, axis=0)
    cov = np.cov((neighbors - centroid).T)
    eigvals, _ = np.linalg.eig(cov)
    eigvals = np.sort(eigvals)
    if np.sum(eigvals) > 1e-9:
        curvatures[i] = eigvals[0] / (eigvals[0] + eigvals[1] + eigvals[2])
    else:
        curvatures[i] = 0

# ----------------------------
# 3. Color Function
# ----------------------------
def color_by_threshold(pcd_obj, curvatures, tau):
    """
    Colors points green if curvature <= tau (smooth region),
    and red otherwise.
    """
    colors = np.zeros((len(curvatures), 3))
    mask = (curvatures <= tau)
    colors[mask] = [0, 1, 0]   # Green for "smooth"
    colors[~mask] = [1, 0, 0]  # Red for "rough"
    pcd_obj.colors = o3d.utility.Vector3dVector(colors)

# Initialize tau (in the same units as our curvature measure)
tau = 0.01
color_by_threshold(pcd_down, curvatures, tau)

# ----------------------------
# 4. Setup OpenCV Trackbar to Control tau
# ----------------------------
# We'll use an OpenCV window named "Control" with a trackbar "tau".
# The trackbar value is scaled (e.g., 0 to 10000 corresponds to 0.0000 to 1.0)
trackbar_scale = 10000

# ----------------------------
# 5. Open3D Visualization Loop with OpenCV Trackbar
# ----------------------------
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="Interactive Curvature Thresholding", width=1024, height=768)
vis.add_geometry(pcd_down)

def on_trackbar(val):
    global tau, vis
    tau = val / trackbar_scale  # convert trackbar value to tau
    color_by_threshold(pcd_down, curvatures, tau)
    print(f"Updated tau: {tau:.4f}")
    vis.update_geometry(pcd_down)  # update the visualizer with the new colors

cv2.namedWindow("Control", cv2.WINDOW_NORMAL)
cv2.createTrackbar("tau", "Control", int(tau * trackbar_scale), trackbar_scale, on_trackbar)

# Main loop: update Open3D renderer and process OpenCV events.
while True:
    vis.poll_events()
    vis.update_renderer()
    cv2.imshow("Control", np.zeros((100, 400), dtype=np.uint8))
    if cv2.waitKey(50) & 0xFF == 27:  # exit on ESC key press
        break

vis.destroy_window()
cv2.destroyAllWindows()
