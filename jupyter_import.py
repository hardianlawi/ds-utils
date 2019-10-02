%cd ..

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display

plt.style.use('seaborn')

plt.rcParams['figure.figsize'] = [9.0, 6.0]
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['text.color'] = 'white'
plt.rcParams['legend.edgecolor'] = 'black'
plt.rcParams['legend.facecolor'] = 'black'
plt.rcParams['legend.frameon'] = True

%matplotlib inline
%config InlineBackend.figure_format = 'retina'


# Useful Add-ons for Jupyter Notebooks
# pip install jupyter_contrib_nbextensions && jupyter contrib nbextension install --user
# pip install ipywidgets && jupyter nbextension enable --py widgetsnbextension
# pip install jupyterthemes
# jt -t onedork -fs 9 -tfs 10 -kl -N
# dark
# jt -t onedork -fs 95 -altp -tfs 11 -nfs 115 -cellw 88% -T -kl -N
# light
# jt -t grade3 -fs 95 -altp -tfs 11 -nfs 115 -cellw 88% -T -kl -N


# Useful link
# https://github.com/dunovank/jupyter-themes
# https://towardsdatascience.com/bringing-the-best-out-of-jupyter-notebooks-for-data-science-f0871519ca29

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
