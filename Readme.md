# Next Word Predictor
Training a deep learning based simple predictor model which predicts the next word in a given sentence to make the best sense. <br> 

Ex: Given the string "What doesn't kill us makes us str"<br>
It predicts ["onger", "ength", "ive", "ange"] and give result like: <br>

["What doesn't kill us makes us stronger",<br>
"What doesn't kill us makes us strength",<br>
"What doesn't kill us makes us strive",<br>
"What doesn't kill us makes us strange"]<br>

**Bonus Task:**
* Built a API with Python Flask and offered as Postman collection for testing
* Created a local PostgreSQL server and using python Psycopg2 to store the feeded string and the result

## Repo Contain:
* **trainingText(2).txt - The actual Data used.**
* **Text Prediction Model Train 01.ipynb - Model design and the training steps involved.**
    >After preprocessing and tokenizing data, a Feature extraction is performed to generate the feature and label.<br>
Using a simple LSTM model with only one hidden layer with 128 neurons and softmax function for activation and Compiling the model with RMSprop optimizer and loss as categorical_crossentropy.<br>
Trained the Model with 20 epochs with validation split of 0.05 and batch_size of 128
* **Corpus_for_trainig.csv - The cleaned data used for training.**
* **WTP_model.h5 & WTPhistory.p - Trained model and history.**
* **char_index.npy, index_char.npy & chars.pckl - Variables for prediction**
* **ML_Prediction.py - Model prediciton which can be used to make predictions.**
    >Defining multiple functions to clean and convert the provided string into vectors which can be further used in prediction fuction in which the Python Enchant Library will check if the predicited word makes sense in english dictionary and remove predicited words if that does not make a proper sense.
* **app.py - Flask app.**
    >Flask API with Psycopg2 for storing the provided string and the predicted result in local PostgreSQL database.
* **postgresql_table_query.txt - SQL Query.**
* **requirements.txt - Python Dependencies.**

## Installation
Downlaod the Repo Clone the base repo onto your desktop with `git` as follows:
```
$ git clone https://github.com/shinigamiloveapple/Text-Word-Prediction-API.git
```
## Prerequisites
Install python dependencies via command:
```
$ pip install -r requirements.txt
```
## App
To launch the App, launch it as follows:
```
$ python app.py
```
Copy the link and paste it on Postman<br>
Feed a json, ex: {"quotes" = "What doesn't kill us makes us str"}<br>
and press Post for the result.








