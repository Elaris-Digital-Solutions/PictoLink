import os
import json
import torch
from datasets import Dataset
from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)

# Configuration
MODEL_NAME = "google/mt5-small"
DATA_FILE = "ml/dataset_picto_v1.jsonl"
OUTPUT_DIR = "nlp_backend/models/mt5_picto_v1"
MAX_INPUT_LENGTH = 64
MAX_TARGET_LENGTH = 64
BATCH_SIZE = 4 # Small batch size for CPU/local testing
EPOCHS = 5

def load_dataset(path: str):
    """Loads dataset from jsonl."""
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    
    # Convert to HF Dataset
    return Dataset.from_list(data)

def preprocess_function(examples, tokenizer):
    inputs = examples["source"]
    targets = examples["target"]
    
    # T5 expects "translate English to German: ..." but for us it's just raw input
    # We can add a prefix if we want, but for now raw is fine
    
    model_inputs = tokenizer(inputs, max_length=MAX_INPUT_LENGTH, truncation=True)
    
    # Setup the tokenizer for targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=MAX_TARGET_LENGTH, truncation=True)
        
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def main():
    print(f"Loading model {MODEL_NAME}...")
    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    
    print(f"Loading data from {DATA_FILE}...")
    dataset = load_dataset(DATA_FILE)
    
    # Split train/test
    dataset = dataset.train_test_split(test_size=0.1)
    
    print("Tokenizing data...")
    tokenized_datasets = dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=dataset["train"].column_names
    )
    
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    
    training_args = Seq2SeqTrainingArguments(
        output_dir="./results",
        eval_strategy="no", # Disable eval to simplify
        learning_rate=2e-4,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        weight_decay=0.01,
        save_total_limit=2,
        num_train_epochs=EPOCHS,
        predict_with_generate=True,
        logging_steps=10,
        save_strategy="no",
    )
    
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        tokenizer=tokenizer,
        data_collator=data_collator,
    )
    
    print("Starting training...")
    try:
        trainer.train()
    except Exception as e:
        print(f"TRAINING FAILED: {e}")
        import traceback
        traceback.print_exc()
        return

    abs_output_dir = os.path.abspath(OUTPUT_DIR)
    print(f"Saving model to {abs_output_dir}...")
    
    if not os.path.exists(os.path.dirname(abs_output_dir)):
        print(f"Creating parent directory {os.path.dirname(abs_output_dir)}")
        os.makedirs(os.path.dirname(abs_output_dir), exist_ok=True)
        
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Done! Model saved to {abs_output_dir}")
    print(f"Directory contents: {os.listdir(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()
