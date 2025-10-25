# IR - TRC
Data: <br>
The new energy minerals international trade networks dataset used in this article is sourced from the United Nations Comtrade Database (https://comtradeplus.un.org/). The feature data include countries' population, GDP, and high-tech levels are from the World Bank (https://data.worldbank.org.cn/); political risk data are from the PRS Group (https://www.prsgroup.com/); and the resource reserves and production datasets are from USGS (https://www.usgs.gov/). You can also search for the needed data in the Data folder.


TRC Phenomenon identification： <br>
Take Co as an example. You can find the distribution of relevant indicators about the Co ore network and the local TRC coefficients at different time intervals in the `Co-TRC.py` file.


DII DII feature selection and weighting： <br>
The DII feature selection and weighting procedures depend on the DADApy library. Please ensure that DADApy is properly installed before running `DII FWE.py`, which contains the implementation of the corresponding algorithms. 
A detailed tutorial and example notebook can be found in the official DADApy documentation: https://dadapy.readthedocs.io/en/latest/jupyter_example_6.html


Other scripts that support the analysis of temporal rich-club (TRC) phenomena and the evolution of international trade networks:

`P_birth.py` and `S&P1.py`: Calculate the network evolution rates.<br>
`Random_t.py`: Generate randomized reference networks for comparison and robustness analysis.<br>
`Uk_Comparian.py`: Evaluate whether a temporal rich-club effect exists (u > 1).<br>
`x feature.py` and `y1 feature.py`: Extract structural features from trade networks, including degree-related and connectivity-based indicators.<br>
`Z-score.py`: Standardize and centralize extracted features using Z-score normalization.<br>
Additional features are provided in the Feature folder.
