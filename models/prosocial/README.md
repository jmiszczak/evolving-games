Simulations of evolution based on [A. Szolnoki, M. Perc, Information sharing promotes prosocial behaviour, New Journal of Physics, Volume 15, May 2013](https://doi.org/10.1088/1367-2630/15/5/053010).

**NOTE**: The main goal was to get nice visualizations, so the scripts are not well suited to produce new data.

# Basic usage
Create `results` and `plots` directories before running the simulations.

`python run.py` will execute the default configuration with 20x20 periodic grid, temptation 1.1 and 1000 rounds. Only
sequential a execution is implemented.

# Visualization

`python plot.py` produces a series of matrix plots.

Run

`sh ../movies.sh`

in `plots` directory to produce dynamics visualizations. This requires `ffmpeg` and should result in some *.mp4 files in the same directory. 
