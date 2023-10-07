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


items = st.slider('Number of demo items?', 30, 100, 50)
if st.button('Run demo'):
    df = pd.DataFrame()
    w = np.random.randint(low = 1, high = 5, size=items)
    h = np.random.randint(low = 1, high = 5, size=items)
    d = np.random.randint(low = 1, high = 5, size=items)
    name = []
    for i in range(items):
        name.append(f"Box-{i}")
    name = np.array(name)
    df["name"] = name
    df["w"] = w
    df["h"] = h
    df["d"] = d
    
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
            item.position = [int(i) for i in item.position]
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
