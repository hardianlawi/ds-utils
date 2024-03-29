import os
import random as python_random

import numpy as np
import torch


def seed_everything(seed):
    os.environ["PYTHONHASHSEED"] = str(seed)
    python_random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
