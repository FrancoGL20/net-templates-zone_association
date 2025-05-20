# TMS Zone Association Tool

This tool automates the process of associating zones with locations in the TMS BY system.

## Prerequisites

- **Python 3.8 or higher (Recommended 3.12)**: This tool requires Python. You can download it from the Microsoft Store.
  - To check if Python is installed and added to the PATH, open a command prompt and run `python --version` (if it's not installed, you will get an error, otherwise it will show the version).

- **Microsoft Edge**: The tool uses Microsoft Edge for automation.

## Initial Configuration

Before start using the tool, this configuration is required to be done only once:

1. Download repository from GitHub

2. Extract the downloaded ZIP file to a location of your choice

   NOTE: It is recommended to create a folder in a location that is not synchronized with OneDrive or Google Drive since the tool may generate temporary files that will be synchronized.

   For example, you can create a folder for the tips inside the C: drive, for example C:\Net_tips\Net-template-zone-association

3. Create a **`.env`** file with the following content:
   ```
   ENV_URL="THE_URL_OF_YOUR_TMS_SYSTEM"
   ENV_USER="YOUR_USERNAME"
   ENV_PASS="YOUR_PASSWORD"
   ```
   IMPORTANT: Replace the values between quotes with the real information of your TMS BY system. This file is critical for the tool's operation, as it contains the credentials necessary to access the system.

## Configuration before every execution

Before start using the tool, this configuration is required to be done every time the tool is executed:

1. Create a **`zone_location.csv`** file with the following format:
   ```
   ZONE_CODE,LOCATION_CODE
   ZONE_CODE,LOCATION_CODE
   ZONE_CODE,LOCATION_CODE
   ...
   ```

   TECHNICAL NOTE: Each line represents an association to be made. The first value is the zone code and the second is the location code, separated by a comma. Do not include headers in the file.

2. Inside the TMS, in the user specified in the .env file, enter the zones menu and make sure that all the zones to be modified specified in the zone_location.csv file are visible on the same page.

    To avoid TMS pagination, there are two possible solutions:
    
    - In the search page, mark the "Select All" check to make all zones visible
    - In the zones page, search by the ids of the zones to be modified


## Usage

1. Simply double-click the `Associate_zones.bat` file, no need to open any terminal or run additional commands.

    NOTE: In case a windows screen like the one below is displayed, click on "More info" and "Run anyway"

2. The tool will check if Python is installed, create a virtual environment, and install the necessary dependencies.
3. It will then run the main script that automates the association process. During this process, you will see how Microsoft Edge opens and performs the necessary operations in the TMS BY system.
4. When finished, press "Enter" to close the window.

    NOTE: This pause at the end of the script execution is to make visible all the actions executed in the previous steps.
5. When finished, a `temp_zone_location.csv` file will be generated with the results of the associations. This file will include the same codes as the original file, but with an additional column that indicates if the association was successful (TRUE), failed (FALSE) or if an error occurred (ERROR).

    ADVICE: Review this file to identify which associations were successfully made and which require additional attention.


## Troubleshooting

If you encounter issues while using the tool, check the following common problems and their solutions:

### Installation and Setup Issues

- **Python Not Installed or Not in PATH**
  - Error: `ERROR: Python is not installed or not in PATH.`
  - Solution: Install Python 3.8 or higher from the Microsoft Store and ensure it is added to the PATH by opening a new command prompt and running `python --version`.

- **Incompatible Python Version**
  - Error: `ERROR: Python version may not be compatible. Python 3.8 or higher is required.`
  - Solution: Update your Python installation to version 3.8 or higher by downloading it from the Microsoft Store.

- **Missing Content Directory**
  - Error: `ERROR: Content directory not found.`
  - Solution: Ensure the `Content` directory exists in the same location as the batch file, if it doesn't, download the tool again and extract it to the same location.

- **Virtual Environment Issues**
  - Error: `ERROR: Could not create virtual environment.` or `ERROR: Could not activate virtual environment.`
  - Solution: Ensure you have permissions to create directories and files in the tool's location. Try running the batch file as administrator.

- **Dependencies Installation Issues**
  - Error: `ERROR: Could not install dependencies.`
  - Solution: Check your internet connection and ensure the `requirements.txt` file exists in the Content directory, if it doesn't, download the tool again and extract it to the same location.

### Configuration Issues

- **Missing .env File**
  - Error: `Error reading .env file: [Errno 2] No such file or directory: '.env'`
  - Solution: Create a `.env` file in the same directory as the batch file with the required environment variables (ENV_URL, ENV_USER, ENV_PASS).

- **Missing zone_location.csv File**
  - Error: `Error: zone_location.csv file not found`
  - Solution: Create a `zone_location.csv` file in the same directory as the batch file with the correct format (ZONE_CODE,LOCATION_CODE).

### Browser and Automation Issues

- **Edge Browser Issues**
  - Error: `Error initializing browser`
  - Solution: Ensure Microsoft Edge is installed and up to date. Try closing all Edge browser instances before running the tool.

- **Login Issues**
  - Problem: The tool cannot log in to the TMS system.
  - Solution: Verify your credentials in the `.env` file are correct and that you have access to the TMS system.

- **Navigation Issues**
  - Problem: The tool cannot navigate to the correct page in the TMS system.
  - Solution: Verify the URL in the `.env` file is correct and that you have the necessary permissions to access the zone association functionality.

### Error Logs

If the tool encounters errors during execution, an error log file will be created at `Content\error_log.txt`. Check this file for detailed error information.

For any other issues not covered here, please contact the author (francisco.gutierrez@netlogistik.com) with the error log file attached.

## Support

For any issues or inquiries, please contact the author (francisco.gutierrez@netlogistik.com).