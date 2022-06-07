# PCR-primer

This is an application created by Alfons Edbom Devall during the the course "Advanced Bioinformatics" at Umeå University 2022.

PCR-primer can be used to obtain unique PCR primer pairs that can be used to identify a user-specified genome. The maximum genome size is recommended to a couple of 100 kbps.

## Download this repository
To download this repository:
- Click the `Code` button in the upper right corner
- Either:
  - Copy the HTTPS or SSH link to the repository and create a clone using the following command in a terminal window:
    - ```bash
      git clone <HTTPS/SSH-link>
      ```
  - `Download ZIP` to download the entire repository as a ZIP-file

## Running the program

This application can be run as a normal python script with the run parameters found in `config.json` and the resulting primer pairs in the `output.txt` file.

It can also be run as a GUI where the user gives the parameters in the GUI and can view the resulting primer paris in a new GUI window.

### Script 

To run this application as a python script, open a terminal window and enter the following command:
```bash
python main.py
```

**Note**: Make sure that the settings in the `config.json` file is correct before running the script. For the script to be able to run, change the filename to a path on your system containing a fasta-file.

The other parameters can also be changed under the `settings` object, but is not required. 

**Note**: The performance of the program depends on which settings are used, if it takes too long, consider going back to the default settings.

### GUI

To run this application in a GUI, open a terminal window and enter the following command:
```bash
python app.py
```

This will open a GUI window where the user can choose which file as well as which settings are to be used. After clicking the `Get primers`, the program will load for a couple of seconds before it opens up another window containing the resulting primer pairs. 