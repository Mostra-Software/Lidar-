
import numpy as np
import copy
import open3d as o3d
import matplotlib as plt
import math
import os

ply_point_cloud = ''


def demo_crop_geometry(pcd_path):
    print("Demo for manual geometry cropping")
    print(
        "1) Press 'Y' twice to align geometry with negative direction of y-axis"
    )
    print("2) Press 'K' to lock screen and to switch to selection mode")
    print("3) Drag for rectangle selection,")
    print("   or use ctrl + left click for polygon selection")
    print("4) Press 'C' to get a selected geometry and to save it")
    print("5) Press 'F' to switch to freeview mode")
    pcd = o3d.io.read_point_cloud(pcd_path)
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

def list_files():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return files

def choose_file(files):
    print("Please choose a file from the list by entering the corresponding number:")
    for i, file in enumerate(files):
        print(f"{i+1}: {file}")
    
    # Get user input
    choice = input("Enter your choice (number): ")
    try:
        choice_index = int(choice) - 1
        if choice_index >= 0 and choice_index < len(files):
            return files[choice_index]
        else:
            print("Invalid choice. Please enter a number from the list.")
            return None
    except ValueError:
        print("Please enter a number.")
        return None


def check_file_type(filename):
    if filename.endswith('.pcd') or filename.endswith('.ply'):
        print(f"You have selected a valid file: {filename}")
        # Here you can load the file into a pointcloud
    else:
        print("Error: Selected file is not a pcd or ply file.")  


def main():
    files = list_files()
    if not files:
        print("No files found in the current directory.")
        return
    
    chosen_file = choose_file(files)
    if chosen_file:
        check_file_type(chosen_file)
        demo_crop_geometry(chosen_file)


if __name__ == "__main__":
    main()
    




