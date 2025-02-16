# import torch
# import torch.optim as optim
# from sklearn.metrics import accuracy_score
# from torch.optim.lr_scheduler import ReduceLROnPlateau
# from torch.utils.data import DataLoader

# from src.model.model import SpeechModelConfig, Wav2VecModel


# def train(model, train_loader, optimizer, criterion, scheduler, device):
#     model.train()
#     running_loss = 0
#     all_preds = []
#     all_labels = []

#     for batch_idx, (audio, labels) in enumerate(train_loader):
#         audio, labels = audio.to(device), labels.to(device)

#         optimizer.zero_grad()
#         outputs = model(audio)

#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()

#         running_loss += loss.item()
#         _, preds = torch.max(outputs, 1)
#         all_preds.extend(preds.cpu().numpy())
#         all_labels.extend(labels.cpu().numpy())

#     accuracy = accuracy_score(all_labels, all_preds)
#     avg_loss = running_loss / len(train_loader)

#     scheduler.step(avg_loss)  # Update the learning rate scheduler
#     return avg_loss, accuracy


# def evaluate(model, eval_loader, criterion, device):
#     model.eval()
#     running_loss = 0
#     all_preds = []
#     all_labels = []

#     with torch.no_grad():
#         for batch_idx, (audio, labels) in enumerate(eval_loader):
#             audio, labels = audio.to(device), labels.to(device)

#             outputs = model(audio)
#             loss = criterion(outputs, labels)

#             running_loss += loss.item()
#             _, preds = torch.max(outputs, 1)
#             all_preds.extend(preds.cpu().numpy())
#             all_labels.extend(labels.cpu().numpy())

#     accuracy = accuracy_score(all_labels, all_preds)
#     avg_loss = running_loss / len(eval_loader)

#     return avg_loss, accuracy


# def main():
#     # Configuration setup
#     config = SpeechModelConfig(
#         model_name="wav2vec2-base", num_classes=4, hidden_dim=256, dropout=0.1
#     )

#     # Initialize model
#     model = Wav2VecModel(config).to(device)

#     # Create dataset and dataloaders
#     # train_dataset = CustomSpeechDataset(
#     #     audio_files=train_audio_files, labels=train_labels
#     # )
#     # eval_dataset = CustomSpeechDataset(
#     #     audio_files=eval_audio_files, labels=eval_labels
#     # )

#     train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
#     eval_loader = DataLoader(eval_dataset, batch_size=32)

#     # Optimizer and Loss function
#     optimizer = optim.Adam(model.parameters(), lr=1e-4)
#     criterion = torch.nn.CrossEntropyLoss()

#     # Learning Rate Scheduler: Reduce LR when validation loss plateaus
#     scheduler = ReduceLROnPlateau(
#         optimizer, "min", patience=3, factor=0.5, verbose=True
#     )

#     # Early stopping setup
#     patience = 5
#     best_loss = float("inf")
#     epochs_without_improvement = 0
#     checkpoint_path = "best_model.pth"

#     # Training loop
#     num_epochs = 50
#     for epoch in range(num_epochs):
#         print(f"Epoch {epoch + 1}/{num_epochs}")

#         # Training phase
#         train_loss, train_accuracy = train(
#             model, train_loader, optimizer, criterion, scheduler, device
#         )
#         print(
#             f"Training Loss: {train_loss:.4f}, Training Accuracy: {train_accuracy:.4f}"
#         )

#         # Evaluation phase
#         eval_loss, eval_accuracy = evaluate(
#             model, eval_loader, criterion, device
#         )
#         print(
#             f"Evaluation Loss: {eval_loss:.4f}, Evaluation Accuracy: {eval_accuracy:.4f}"
#         )

#         if eval_loss < best_loss:
#             print(
#                 f"Validation loss improved ({best_loss:.4f} --> {eval_loss:.4f}). Saving model."
#             )
#             save_checkpoint(
#                 model, optimizer, epoch, eval_loss, checkpoint_path
#             )
#             best_loss = eval_loss
#             epochs_without_improvement = 0
#         else:
#             epochs_without_improvement += 1
#             print(
#                 f"No improvement in validation loss for {epochs_without_improvement} epochs."
#             )

#             if epochs_without_improvement >= patience:
#                 print("Early stopping triggered. Training will stop.")
#                 break


# if __name__ == "__main__":
#     # Set device to GPU if available, otherwise use CPU
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#     # Set your train and evaluation audio files and labels here
#     train_audio_files = []  # List of training audio files
#     train_labels = []  # Corresponding labels for training
#     eval_audio_files = []  # List of evaluation audio files
#     eval_labels = []  # Corresponding labels for evaluation

#     main()
