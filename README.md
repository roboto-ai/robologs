# robologs

## What is robologs

`robologs` is an open-source library of data transformations for the robotics and drone communities.

If you're an engineer or scientist working in robotics, machine learning, computer vision or aerospace then you've probably had to write your own scripts to process data from ROS, PX4, ArduPilot etc. This can be tedious and time-consuming given the complexity of these data formats and their underlying system requirements. Even simple actions like converting a rosbag of images to a video can be challenging.

...well, not any more we say! With `robologs`, you can process sensor data for a variety of use cases:

- Graph a subset of relevant timeseries signals
- Extract images for data labeling, annotation and model training workflows
- Convert binary data to formats supported by common tools
- Sample streams of sensor data for easier analysis
- Ingest filtered data into databases for search

## Quickstart<a name="quickstart" />

`robologs` is organized into a collection of sub-packages: 

- `robologs-*-actions` packages contain containerized *actions* for specific data formats.
- `robologs-*-utils` packages contain corresponding utility functions.

Have a look at the packages below for more details.

## Data Formats<a name="data-formats" />

`robologs` currently has transformations for the following data formats:

| Package                                                                             | Extensions          | Description                                                  | Support 
|:------------------------------------------------------------------------------------|:--------------------|:-------------------------------------------------------------|:--------|
| [robologs-ros-actions](https://github.com/roboto-ai/robologs-ros-actions)           | .bag / .mcap / .db3 | Containerized actions to transform ROS data  | 🛠      |

Utility packages:

| Package                                                                             | Description                                                  |
|:------------------------------------------------------------------------------------|:-------------------------------------------------------------|
| [robologs-timeseries-utils](https://github.com/roboto-ai/robologs-timeseries-utils) | Utility functions for working with timeseries data |


Do you have a request for a data format that's not listed above? Raise an issue or join our [Discord community](https://discord.gg/YFenn4Ww5F) and make a request!

## Community

If you have any questions, comments, or want to chat, please join our [Discord community](https://discord.gg/YFenn4Ww5F).

## Contribute 
### How to Contribute

We welcome contributions to `robologs`. We are in the process of creating a [contribution guide](#) and [development guide](#).

### Contributors

<a href="https://github.com/roboto-dev/robologs/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=roboto-dev/robologs" />
</a>

Made with [contrib.rocks](https://contrib.rocks).
