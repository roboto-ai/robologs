# ROS Connectors

## Build the ROS docker image locally

```bash
# Go to the robologs base directory
cd ~/Code/robologs/
docker build --network=host -t robologs-ros-noetic-image --file ingestion/ros/docker/Dockerfile .
```

## Examples

### Get ROSbag metadata
The following command extracts ROSbag metadata and stores it to a .json file. 
```bash
# Go to the robologs base directory
docker run --volume /home/yves/Desktop/scratch:/input  robologs-ros-noetic-image /function/ingestion/ros/src/get_summary_from_bag.py --input /input --output /input```
```