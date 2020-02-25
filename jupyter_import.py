%cd ..
%load_ext nb_black

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display

%matplotlib inline

plt.style.use('seaborn')
plt.rcParams['legend.frameon'] = True
sns.set_style("whitegrid", {'grid.linestyle': '--'})

pd.options.display.max_columns = 100

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