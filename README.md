# Eve Energy Visualizer
Visualize Eve Energy consumption data.

## Usage

1. Clone this repository to a location accessable from an iOS device (iCloud, Nextcloud, etc.).

2. Export data from each Eve Energy device via the Eve App to the `data` directory. In the Eve App, open the Energy Accessory > "i" > "Measurements" > Share > Save to Files and select the `data` directory.

3. Run `python main.py` with arguments of visualizations you would like to output.


### Arguments

| Argument | Details |
| --- | --- |
| --date | outputs a line graph visualizing energy usage over time |
| --heatmap | outputs a heatmap of total energy usage by day of week and time of day |


[TODO](TODO.md)
