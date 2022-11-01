# Using Pandas
Pandas allows loading CSV file(s) with columns assigned to a name, and no requirement that columns be of the same type (int, float, string, etc.)

~~~python
import pandas as pd
~~~

## Loading a single file
We can use the built in read_csv function. The most common options are:

- filename, the full filename and path
- delimiter, use ',' if comma
- header, the line number with the header row, if present. None otherwise. First line is 0, second is 1, etc.
- names, can manually provide a list of names for each column as ['name1', 'name2', ... ,'nameN']
- skipinitialspace, sometimes headers have a space before the name which can cause issues, not a bad idea to set to True in most cases

### example
loading an ISE logfile, where the column names are given on the third line

~~~python
log = pd.read_csv('logfiles/log_20220408_001.csv', delimiter=',',header=2,skipinitialspace=True)
~~~

## access data
using Pandas allows us to access columns by their names, in our example if I wanted the pitch feedback I would simply use

~~~python
log.vcc_pos_pitch_fb_deg
~~~

The column names can be access by using

~~~python
log.columns.values
~~~

# Loading multiple files
building on the the read_csv function, we use the builtin concat function. concat creates a single DataFrame from a list of DataFrames. We can create this list of DataFrames by calling read_csv on a set of filenames using the Python glob function. 

glob essentially allows wildcard actions on filenames in the same manner as you would in the OS command line

~~~python
from glob import glob
filenames = glob('logfiles/log_*.csv')
~~~

The Python list comprehension is an easy way to now build the list of DataFrames, one for each file, using the same arguments we used for a single file

~~~python
sub_frames = [pd.read_csv(f,delimiter=',',header=2,skipinitialspace=True) for f in filenames]
~~~

this list can now be used in the concat function. The only other option we use is the ignore_index, this is to avoid the issue that each individual log file re-starts their indexing at 1, so we woudl prefer to ignore that and let the combined DataFrame have it's own index

~~~python
log_data = pd.concat(sub_frames, ignore_index=True)
~~~