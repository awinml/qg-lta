# external libraries
import torch
import os

# internal utilities
from preprocessing import DataPreprocessor
from torchtext import data
from model import Seq2Seq
import config

# Preprocessing values used for training
prepro_params = {
    "word_embedding_size": config.word_embedding_size,
    "answer_embedding_size": config.answer_embedding_size,
    "max_len_context": config.max_len_context,
    "max_len_question": config.max_len_question,
}

# Hyper-parameters setup
hyper_params = {
    "eval_batch_size": config.eval_batch_size,
    "hidden_size": config.hidden_size,
    "n_layers": config.n_layers,
    "drop_prob": config.drop_prob,
    "cuda": config.cuda,
    "use_answer": config.use_answer,
    "min_len_question": config.min_len_question,
    "max_len_question": config.max_len_question,
    "top_k": config.top_k,
    "top_p": config.top_p,
    "temperature": config.temperature,
    "decode_type": config.decode_type
}

# Train on GPU if CUDA variable is set to True (a GPU with CUDA is needed to do so)
device = torch.device("cuda" if hyper_params["cuda"] else "cpu")
torch.manual_seed(42)
# Changed Path from "output/" to "data/output/""
experiment_path = "data/output/{}".format(config.exp)

# Preprocess the data
dp = DataPreprocessor()
_, _, vocabs = dp.load_data(os.path.join(config.out_dir, "train-dataset.pt"),
                            os.path.join(config.out_dir, "dev-dataset.pt"),
                            config.glove)

# Load the data into datasets of mini-batches
ext = "sentence" if not config.paragraph else "context"
test_dataset = dp.generate_data(os.path.join(config.out_dir, "dev"), ext,
                                "question", max_len=prepro_params["max_len_context"])

test_dataloader = data.BucketIterator(test_dataset,
                                      batch_size=hyper_params["eval_batch_size"],
                                      sort_key=lambda x: len(x.sentence),
                                      shuffle=False)

# Load the model
model = Seq2Seq(in_vocab=vocabs["src_vocab"],
                hidden_size=hyper_params["hidden_size"],
                n_layers=hyper_params["n_layers"],
                trg_vocab=vocabs['trg_vocab'],
                device=device,
                drop_prob=hyper_params["drop_prob"],
                use_answer=hyper_params["use_answer"])

# Load the model weights resulting from training
if not hyper_params["cuda"]:
    model.load_state_dict(torch.load(os.path.join(experiment_path, "model.pkl"),
                                     map_location=lambda storage, loc: storage)["state_dict"])
else:
    model.load_state_dict(torch.load(os.path.join(experiment_path, "model.pkl"))["state_dict"])
model.to(device)

# Enter evaluation loop
model.eval()
with torch.no_grad():
    for i, batch in enumerate(test_dataloader):
        # Load a batch of input sentence, sentence lengths and questions
        sentence, len_sentence, question = batch.src[0], batch.src[1], batch.trg[0]
        answer = batch.feat.to(device) if hyper_params["use_answer"] else None
        # Forward pass to get output/logits
        pred = model(sentence, len_sentence, answer=answer)
        # Convert the predicted indexes to words
        pred = [vocabs["trg_vocab"].itos[i] for i in pred if vocabs["trg_vocab"].itos[i]]
        # Print the sentence generated by the model
        print(" ".join(pred[1:]))
