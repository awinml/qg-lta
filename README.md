# Neural Question Generation: Learning to Ask

https://github.com/GauthierDmn/question_generation

Code rewritten to be compatible with Python 3.x.


# Set-Up
## Donwloading NewsQA Dataset
Before running the following commands to train your model, you need to download the NewsQA dataset manually [here](https://github.com/Maluuba/newsqa). Follow the steps below to save it in a JSON file.

### Steps to download the NewsQA dataset manually:
* Clone this repository : [Maluuba/newsqa](https://github.com/Maluuba/newsqa)
* Download the tar.gz file for the questions and answers from [here][maluuba_newsqa_dl] to the maluuba/newsqa folder. No need to extract anything.
* Download the CNN stories from [here][cnn_stories] to the maluuba/newsqa folder.
* Use Python 2.7 to package the dataset (Python 2.7):
** Create an Python 2.7 environment with pandas>=0.19.2.
** Open newsqa/maluuba/newsqa/data_generator.py and comment last four lines:
```
    # tokenized_data_path = os.path.join(dir_name, 'newsqa-data-tokenized-v1.csv')
    # tokenize(output_path=tokenized_data_path)
    # split_data(dataset_path=tokenized_data_path)
    # simplify(output_dir_path='split_data')
```
This will make sure that we just create the data without tokenization. The tokenization step requires JAVA. This will eliminate that dependency.

Downloading NewsQA Data still requires python 2.x. It has been downloaded in the data/newsqa-data-v1 directory for further use.


## Running model

* Clone this repository : [here](https://github.com/GauthierDmn/question_generation)
* Create a data directory: `mkdir data`
* Create a directory for your experiments, logs and model weights: `mkdir data/output`
* By default the GloVE, SquAD and NewsQA datasets are to be stored under 
`data/glove.6b`, `data/squad`, `data/newsqa/newsqa-data-v1`.
* Download GloVE word vectors: https://nlp.stanford.edu/projects/glove/ and extract the files in the `data/glove.6b` directory.
* Put the NewsQA data file `combined-newsqa-data-v1.json` file in the `data/newsqa/newsqa-data-v1` directory. 
* Modify the `config.py` file to set up the paths (if the paths are different) where your GloVE, SquAD and NewsQA datasets, and where your models will be saved (output directory).
* Create a Python virtual environment, source to it: `mkvirualenv qa-env ; workon qa-env` if you use virtualenvwrapper
* Install the dependencies: `pip install -r requirements.txt ; python -m spacy download en`
* Run `python make_dataset.py` to download SquAD dataset, and join SQuAD and NewsQA datasets into a single file
* Run `python preprocessing.py` to preprocess the data
* Run `python train.py` to train the model with hyper-parameters found in `config.py`
* Run `python eval.py` on a test file to generate your own questions!




