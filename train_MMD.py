import torch
import torch.optim as optim
from torch import nn
from model.ResnetMMD import ResnetMMD 
from dataset.transform import transform
from dataset.OfficeHome import OfficeHomeDataset

data_dir = "/content/drive/MyDrive/OfficeHome"
domains = ["Art", "Clipart"]

dataset = OfficeHomeDataset(root_dir=data_dir, domains=domains, transform=transform)
train_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

#model = ResnetBase(num_classes=65, is_nonlinear = False)
model = ResnetMMD(num_classes=65, is_nonlinear = False, rsc_f_drop_factor = 0.33, rsc_b_drop_factor = 0.33)
model.set_optimizer(optim.Adam(model.parameters(), lr=0.001))
model.set_loss_fn(nn.CrossEntropyLoss())
model.set_scheduler(optim.lr_scheduler.StepLR(model.optimizer, step_size=5, gamma=0.1))
for epoch in range(10):
    for x, y in train_loader:
        loss = model.update(x, y)
    model.update_lr()
    print(f"Epoch {epoch+1}, Loss: {loss}")