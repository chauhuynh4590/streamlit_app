import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from py3dbp import Packer, Bin, Item, Painter
import time
import random
import numpy as np
def hex_code_colors(seed):
    random.seed(seed)
    a = hex(random.randrange(0,256))
    b = hex(random.randrange(0,256))
    c = hex(random.randrange(0,256))
    a = a[2:]
    b = b[2:]
    c = c[2:]
    if len(a)<2:
        a = "0" + a
    if len(b)<2:
        b = "0" + b
    if len(c)<2:
        c = "0" + c
    z = a + b + c
    return "#" + z.upper()

st.title("Bin Packing Problem")

# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
df = pd.read_csv("../Downloads/test.csv")
st.header("INPUT")
st.write(df)
packer = Packer()
st.header("OUTPUT")
#  init bin 
for i in range(7):
    box = Bin(f'Bin{i}', (5, 5, 5), 100,0,0)
    packer.addBin(box)

for index, row in df.iterrows():
    packer.addItem(Item(partno=row["name"], name=f'test{index}', typeof='cube', WHD=(row["w"], row["h"], row["d"]), weight=1, level=1,loadbear=100, updown=True, color=hex_code_colors(index)))

# calculate packing 
packer.pack(
    bigger_first=True,
    distribute_items=True,
    fix_point=True, # Try switching fix_point=True/False to compare the results
    check_stable=True,
    support_surface_ratio=0.75,
    number_of_decimals=0
)
packer.putOrder()
for box in packer.bins:

    volume = box.width * box.height * box.depth
    print(":::::::::::", box.string())

    print("FITTED ITEMS:")
    volume_t = 0
    volume_f = 0
    unfitted_name = ''

    # '''
    output_df = pd.DataFrame()
    name = []
    position = []
    rotation = []
    for item in box.items:
        name.append(item.partno)            
        position.append(str(tuple(item.position)))
        rotation.append(item.rotation_type)
    output_df["name"] = np.array(name)
    output_df["position"] = np.array(position)
    output_df["rotation"] = np.array(rotation)

    painter = Painter(box)
    fig = painter.plotBoxAndItems(
        title=box.partno,
        alpha=0.2,
        write_num=True,
        fontsize=10
    )
    col_csv, col_fig = st.columns(spec = [0.6, 0.4], gap="small")
    with col_csv:
        st.header("csv")
        st.write(output_df)
    with col_fig:
        st.header("figure")
        st.pyplot(fig)