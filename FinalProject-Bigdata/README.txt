Chunksday: ride data split by time chunks for new year day. Also contains pairsmod.py which is our main mapreduce file we run on dataproc
Chunksweek: ride data split by time chunks for a week. Takes too long to run, so we don't run it.
Reduced: results from dataproc in .txt format
ReducedCSV: running Txt to csv parsing, we get Reduced in CSV form ready for heatmap. Also contains the Jupyter Notebook file for heatmap generation.
ScreenshotresultIN: screenshot of all the 16 chunks zoomed in at manhattan and a gif animating them
ScreenshotresultOUT: screenshot of all the 16 chunks zoomed out and a gif animating them