import numpy as np
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# Transform to normalized Tensors
transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.1307,), (0.3081,))])

# Download dataset, and normalize.
train_dataset = datasets.MNIST(
    './MNIST/', train=True, transform=transform, download=True)
# test_dataset = datasets.MNIST('./MNIST/', train=False, transform=transform, download=True)


train_loader = DataLoader(train_dataset, batch_size=len(train_dataset))
# test_loader = DataLoader(test_dataset, batch_size=len(test_dataset))


# Transform to numpy arrays.
train_dataset_array = next(iter(train_loader))[0].numpy()
train_label_array = next(iter(train_loader))[1].numpy()
# test_dataset_array = next(iter(test_loader))[0].numpy()

# Reshape to 784*1 array.
train_dataset_array = train_dataset_array.reshape((60000, 784))

# Save to file.
# np.save('./MNIST/train_images.npy', train_dataset_array)
# np.save('./MNIST/train_labels.npy', train_label_array)

np.savetxt('./MNIST/train_images.txt', train_dataset_array)
