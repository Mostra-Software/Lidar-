import open3d as o3d

# Load the PCD file
pcd = o3d.io.read_point_cloud("frame_126.pcd")

# Extract points
points = pcd.points

# Write points to a text file, including point number
with open("output_points_with_numbers.txt", "w") as file:
    for idx, point in enumerate(points, start=1):  # start=1 makes the enumeration start at 1
        # Format the output to include point number and its x, y, z values
        file.write(f"{idx},{point[0]},{point[1]},{point[2]}\n")

print("Points with their numbers have been written to output_points_with_numbers.txt")
