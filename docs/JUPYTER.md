# Useful Codes on Jupyter

```python
%cd ..
%load_ext lab_black
%load_ext nb_black
%load_ext google.cloud.bigquery
%load_ext autoreload
%autoreload 2

import os
import random as python_random

import datatable as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch
from IPython.display import display

%matplotlib inline

plt.style.use("seaborn-v0_8-deep")

plt.rcParams["figure.figsize"] = [20.0, 10.0]
plt.rcParams["agg.path.chunksize"] = 10000
plt.rcParams["legend.frameon"] = True
sns.set_style("whitegrid", {'grid.linestyle': '--'})

pd.options.display.max_columns = 200
pd.options.display.max_rows = 200
pd.options.display.max_colwidth = 200


def inspect(df):
    print('df size:', df.shape)
    display(df.head())
    print("\nStatistics")
    display(df.describe([.05, .25, .5, .75, .95, .99]))
    print("\nMissing values")
    display(df.isnull().sum())
    print(f"Any missing values: {df.isnull().any()}")
    display(df.dtypes)


def seed_everything(seed):
    os.environ['PYTHONHASHSEED'] = str(seed)
    python_random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    print(f'Set seed = {seed}')

# Load from BQ
# %%bigquery sg_reward_log --params {"start_date": '2020-12-02', "end_date": '2020-12-18'}

# Hide ALL Codes
# http://blog.nextgenetics.net/?e=102
# https://chris-said.io/2016/02/13/how-to-make-polished-jupyter-presentations-with-optional-code-visibility/
from IPython.display import HTML

HTML('''<script>
code_show=true;
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
}
$( document ).ready(code_toggle);
</script>
The raw code for this IPython notebook is by default hidden for easier reading.
To toggle on/off the raw code, click <a href="javascript:code_toggle()">here</a>.''')

plt.style.use('seaborn')

plt.rcParams["figure.figsize"] = [20.0, 10.0]
plt.rcParams["agg.path.chunksize"] = 10000
plt.rcParams["legend.frameon"] = True
sns.set_style("whitegrid", {'grid.linestyle': '--'})

pd.options.display.max_columns = 200
pd.options.display.max_rows = 200
pd.options.display.max_colwidth = 200

%load_ext google.cloud.bigquery

# Load from BQ
%%bigquery sg_reward_log --params {"start_date": '2020-12-02', "end_date": '2020-12-18'}
```
