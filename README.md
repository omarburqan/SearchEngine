Given the input file with the raw data, the code creates an index that allows efficient access to information.
The index will be stored on disk so that it can be used when querying different products. 
Therefore, the index files will remain on disk even when the program is not running. The precise structure of the index is part of the planning decisions I made. 
the way that I built the index is explained in the analyze file.

Data set
The goal of the project to be built a search engine for product reviews Each product opinion is in the following structure:

product/productId: B001E4KFG0 

review/userId: A3SGXH7AUHU8GW 

review/profileName: delmartian 

review/helpfulness: 1/1 

review/score: 5.0 

review/time: 1303862400 

review/summary: Good Quality Dog Food 

review/text: I have bought several of the Vitality canned dog food products and have found them all to be of good quality. The product looks more like a stew than a processed meat and it smells better. My Labrador is finicky and she appreciates this product better than most. 
requirement
