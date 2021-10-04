# Assignment 2

# Installation

- Install Python
- Install the virtual environment package: `pip install virtualenv`
- Create a virtual environment in this directory: `virtualenv env`
- Activate the virtual environment:
  - Linux:
    - `source env/bin/activate`
  - Windows:
    - `env/Scripts/activate.bat`
- Install the dependencies: `pip install requests bokeh`
- Optionally install selenium and geckodriver to output pngs (not recommended since interactive visualizations are better): `pip install selenium`
- Run `python get_data.py` to scrape the data and save it locally (not necessary since zip should include the needed data)
- Run `python visualize_data.py` to create the visualizations in the form of html files (also not necessary since they should already be built in the zip)
- Open the html files in a browser to view and interact with them