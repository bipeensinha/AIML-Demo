from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

print("Loading local AI model...")

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto"
)

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    }
]

print("\nLocal AI Chat")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("AI: Goodbye!")
        break

    messages.append({
        "role": "user",
        "content": question
    })

    # Convert chat messages into the format expected by Qwen
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Convert text into model inputs
    inputs = tokenizer(
        [text],
        return_tensors="pt"
    )

    # Generate response
    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=100
        )

    # Remove the original prompt from the generated output
    generated_ids = outputs[0][inputs.input_ids.shape[-1]:]

    # Convert tokens back to text
    answer = tokenizer.decode(
        generated_ids,
        skip_special_tokens=True
    )

    print("\nAI:", answer)

    messages.append({
        "role": "assistant",
        "content": answer
    })