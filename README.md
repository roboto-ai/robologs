# robologs

## What is robologs

robologs is an open source library of containerized data transformations for the robotics and drone communities. With robologs, users are able to extract and transform slices of sensor data for a variety of use cases:

- Graph a subset of relevant time series signals
- Extract a subset of images for data labeling, annotation and model training workflows
- Convert binary data to formats that are supported by common tools
- Sample streams of sensor data for easier analysis
- Ingest filtered and transformed data into databases

If you are an engineer or scientist working in robotics, machine learning, computer vision or aerospace then you've probably had to write your own data extraction scripts from data formats such as ROS, PX4, ArduPilot etc. This can be tedious and time-consuming given the complexity of these data formats and their underlying system requirements. Even simple transformations such as converting a rosbag of images to a video, or creating a graph of battery data from a PX4 log can be challenging.

...well, not any more we say! 

## Python Quickstart<a name="python-quickstart" />

Installing robologs using the pip package manager is as easy as running `pip install robologs` in your terminal.

From here, you can type commands to transform data from log files:

```python
TBD
```

## Community

If you have any questions, comments, or want to chat, please join [our Slack channel](#).

## Contribute 
### How to Contribute

We welcome contributions to robologs. Please see our [contribution guide](#) and our [development guide](#) for details.

### Contributors

<a href="https://github.com/roboto-dev/robologs/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=roboto-dev/robologs" />
</a>

Made with [contrib.rocks](https://contrib.rocks).
