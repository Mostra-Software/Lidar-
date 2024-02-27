
import numpy as np
import copy
import open3d as o3d
import matplotlib as plt
import math


ply_point_cloud = 'frame_15.pcd'


def demo_crop_geometry():
    print("Demo for manual geometry cropping")
    print(
        "1) Press 'Y' twice to align geometry with negative direction of y-axis"
    )
    print("2) Press 'K' to lock screen and to switch to selection mode")
    print("3) Drag for rectangle selection,")
    print("   or use ctrl + left click for polygon selection")
    print("4) Press 'C' to get a selected geometry and to save it")
    print("5) Press 'F' to switch to freeview mode")
    pcd = o3d.io.read_point_cloud(ply_point_cloud)
    o3d.visualization.draw_geometries_with_editing([pcd])
    print("File found, opening...")
    print (pcd.points[0])


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])

def pick_points(pcd):
    print("")
    print(
        "1) Please pick at least three correspondences using [shift + left click]"
    )
    print("   Press [shift + right click] to undo point picking")
    print("2) After picking points, press 'Q' to close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points
    vis.destroy_window()
    picked_points = vis.get_picked_points()

    # Print the coordinates of the picked points with formatted floating-point numbers
    print("\nPicked points:")
    for i in picked_points:
        point = pcd.points[i]
        formatted_point = (f"({point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f})")
        print(f"Point {i}: {formatted_point}")
        quit 
    print("xd")

    return picked_points





def filter_points_by_angle(ply_point_cloud, max_angle_deg=45):
    try:
        pcd = o3d.io.read_point_cloud(ply_point_cloud)
        print("File found, opening...")
    except FileNotFoundError:
        print("FILE NOT FOUND")
        return None  # or handle the error as per your application's requirements

    points = np.asarray(pcd.points)
    if points.size == 0:
        print("No points in point cloud.")
        return None

    # Normalize points to get only direction vectors
    norms = np.linalg.norm(points, axis=1, keepdims=True)
    directions = points / norms

    # Z-axis direction vector
    z_axis = np.array([0, 0, 1])

    # Compute angles in radians between each point direction and the Z-axis
    # Need to ensure dot product is computed for each point individually
    angles = np.arccos(np.clip(np.sum(directions * z_axis, axis=1), -1.0, 1.0))

    # Convert max_angle_deg to radians
    max_angle_rad = np.radians(max_angle_deg)

    # Find points where the angle with the Z-axis is within the threshold
    valid_indices = np.where(angles <= max_angle_rad)[0]

    # Create a new point cloud with only the filtered points
    filtered_points = points[valid_indices]
    filtered_pcd = o3d.geometry.PointCloud()
    filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)

    return filtered_pcd


  


if __name__ == "__main__":
    demo_crop_geometry()
    




