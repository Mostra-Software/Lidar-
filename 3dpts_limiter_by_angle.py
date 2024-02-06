import open3d
import ouster.sdk 

import numpy as np

from ouster import client
from ouster.client import LidarMode


import argparse
from contextlib import closing

def configure_sensor_params(hostname: str) -> None:
    """Configure sensor params given hostname

    Args:
        hostname: hostname of the sensor
    """

    # [doc-stag-configure]
    # create empty config
    config = client.SensorConfig()

    # set the values that you need: see sensor documentation for param meanings
    config.operating_mode = client.OperatingMode.OPERATING_NORMAL
    config.lidar_mode = client.LidarMode.MODE_1024x10
    config.udp_port_lidar = 7502
    config.udp_port_imu = 7503

    # set the config on sensor, using appropriate flags
    client.set_config(hostname, config, persist=True, udp_dest_auto=True)
    # [doc-etag-configure]

    # if you like, you can view the entire set of parameters
    config = client.get_config(hostname)
    print(f"sensor config of {hostname}:\n{config}")

def fetch_metadata(hostname: str) -> None:
    """Fetch metadata from a sensor and write it to disk.

    Accurately reconstructing point clouds from a sensor data stream
    requires access to sensor calibration and per-run configuration
    like the operating mode and azimuth window.

    The client API makes it easy to read metadata and write it to disk
    for use with recorded data streams.

    Args:
        hostname: hostname of the sensor
    """
    # [doc-stag-fetch-metadata]
    with closing(client.Sensor(hostname, 7502, 7503)) as source:
        # print some useful info from
        print("Retrieved metadata:")
        print(f"  serial no:        {source.metadata.sn}")
        print(f"  firmware version: {source.metadata.fw_rev}")
        print(f"  product line:     {source.metadata.prod_line}")
        print(f"  lidar mode:       {source.metadata.mode}")
        print(f"Writing to: {hostname}.json")

        # write metadata to disk
        source.write_metadata(f"{hostname}.json")
    # [doc-etag-fetch-metadata]

def filter_3d_by_range_and_azimuth(hostname: str,
                                   lidar_port: int = 7502,
                                   range_min: int = 2) -> None:
    """Easily filter 3D Point Cloud by Range and Azimuth Using the 2D Representation

    Args:
        hostname: hostname of sensor
        lidar_port: UDP port to listen on for lidar data
        range_min: range minimum in meters
    """
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except ModuleNotFoundError:
        print("This example requires matplotlib and an appropriate Matplotlib "
            "GUI backend such as TkAgg or Qt5Agg.")
        exit(1)
    import math

    # set up figure
    plt.figure()
    ax = plt.axes(projection='3d')
    r = 3
    ax.set_xlim3d([-r, r])
    ax.set_ylim3d([-r, r])
    ax.set_zlim3d([-r, r])

    plt.title("Filtered 3D Points from {}".format(hostname))

    metadata, sample = client.Scans.sample(hostname, 2, lidar_port)
    scan = next(sample)[1]

    # [doc-stag-filter-3d]
    # obtain destaggered range
    range_destaggered = client.destagger(metadata,
                                         scan.field(client.ChanField.RANGE))

    # obtain destaggered xyz representation
    xyzlut = client.XYZLut(metadata)
    xyz_destaggered = client.destagger(metadata, xyzlut(scan))

    # select only points with more than min range using the range data
    xyz_filtered = xyz_destaggered * (range_destaggered[:, :, np.newaxis] >
                                      (range_min * 1000))

    # get first 3/4 of scan
    to_col = math.floor(metadata.mode.cols * 3 / 4)
    xyz_filtered = xyz_filtered[:, 0:to_col, :]
    # [doc-etag-filter-3d]

    [x, y, z] = [c.flatten() for c in np.dsplit(xyz_filtered, 3)]
    ax.scatter(x, y, z, c=z / max(z), s=0.2)
    plt.show()

def main() -> None :
    try:
        filter_3d_by_range_and_azimuth,
    except KeyboardInterrupt:
        print(f"No such example:")
        exit(1)
    
    

