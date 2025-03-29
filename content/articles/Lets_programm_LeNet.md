---
title: 'Lets Program LeNet'
date: 2024-11-06
tags: ["coding", "CNN"]
---

[LeNet](http://vision.stanford.edu/cs598_spring07/papers/Lecun98.pdf) is one of the first [convolutional neural networks (CNNs)](https://en.wikipedia.org/wiki/Convolutional_neural_network). Its design is relatively simple and well-documented, making it a good candidate for implementation to gain practice with a deep learning library such as [PyTorch](https://pytorch.org/).

In this article, I will show how you can use PyTorch to implement a deep convolutional neural network, train it, and perform inference. If you are interested in more of the theory, I recommend consulting my [prior post](/articles/proseminar_cnn/) on CNNs. Another excellent resource is the [CS231n site on CNNs](https://cs231n.github.io/convolutional-networks/).

Familiarity with how convolutional neural networks work is recommended, as this article focuses mainly on the practical side.

## Prerequisites

You will need an up-to-date Python version installed. Additionally, you will need to install PyTorch, a deep learning library, and torchvision, which provides datasets for testing. To install PyTorch and torchvision, I recommend using [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html), which allows you to create a virtual Python environment where libraries won’t conflict with others you have installed. (If you are familiar with Docker, it is similar but specific to Python.) Alternatively, you can use pip, Python’s default package manager.

Run the command from the [PyTorch site](https://pytorch.org/get-started/locally/) in the terminal to get started. If you have an NVIDIA GPU with CUDA installed, you can use the CUDA version, which allows PyTorch to take advantage of your GPU for faster training and inference. Otherwise, use the CPU version.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/pytorch_installation.jpg">
</figure>
{{< /rawhtml >}}

When installing PyTorch with CUDA, it is important to select the compatible CUDA version. If you have CUDA installed but are unsure of your version, you can use the following command to check:

```sh
nvcc --version
```
If CUDA is not installed on your system, refer to NVIDIA’s official [installation guide](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/).

In addition to PyTorch, we will use [Matplotlib](https://matplotlib.org/) for visualization purposes. Refer to their [installation guide](https://matplotlib.org/stable/install/index.html) if you need help with installation.


## LeNet Overview

First, we need to clarify the components that make up LeNet-5. Below is a visualization of its architecture.

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/LeNet-5_architecture.png">
    <figcaption style="margin-top: 10px; text-align:center;">Source: Wikipedia</figcaption>
</figure>
{{< /rawhtml >}}


{{< rawhtml >}}
<figure style="max-width: 100%; width: 20%; float: right; margin: 0 0 1em 1em;">
    <div style="float: right; width: 100%;">
        <img loading="lazy" src="/attachments/LeNet-5_architecture_block_diagram.svg.png" style="width: 100%;">
    </div>
    <figcaption style="clear: both; text-align: center;">Source: <a href="https://en.wikipedia.org/wiki/LeNet#/media/File:LeNet-5_architecture_block_diagram.svg">Wikipedia</a></figcaption>
</figure>
{{< /rawhtml >}}


As shown, LeNet-5 consists of three main components:
- [Convolutional layer](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html), which uses a 2-dimensional kernel to scan the input from the previous layer.
- [Linear layer](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html), also called dense or fully connected layers.
- [Pooling layer](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html), specifically an average pooling layer, which is mainly used to reduce dimensionality.

Each of these layers has additional attributes, known as hyperparameters, that can be identified from the block diagram.

The input layer expects an input size of 28x28. The first convolutional layer will have 6 feature maps (output channels), with a kernel size of 5x5 and 2 pixels of padding. The average pooling layer will use a kernel size of 2x2 with a stride of 2.

A brief explanation, **Kernel size** refers to the dimensions of the filter (e.g., 3x3 or 5x5) used in a convolutional layer to scan the input image or feature map. **Stride** defines how many pixels the filter moves across the input during each convolution operation, affecting the output size. And at last, **Padding** involves adding extra pixels (usually zeros) around the input image to ensure the filter can fully cover the edges of the input or to control the output size.

## Implementation of LeNet

Now that we know the specific hyperparameters of our model, we can start coding. First, we need to define the structure of our network. PyTorch provides the [Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html) class, which our neural network should inherit from. This setup will make it easier to train our network later.

Let's import some of the libraries we'll use:

```python
# Importing all the libraries we need for now
import torch
import torch.nn as nn
import torch.nn.functional as F
```

Next, we can define our PyTorch `Module` class:

```python
# Our neural network
class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        pass 

    def forward(self, x):
        pass 
```

In the constructor (`__init__`), we’ll define the layers of our network. The `forward` method specifies what the network should do during the forward pass—in other words, how the layers should be applied to our input.

Let’s define our first [convolutional layer](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html). It has one input channel, because our input will be grayscale images (with only one color channel), 6 output channels, and a kernel size of 5:

```python 
self.conv1 = nn.Conv2d(1, 6, 5)
```

The [pooling layer](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html) is similarly easy to define; we just need to pass the kernel size and then the stride:

```python 
self.pool1 = nn.AvgPool2d(2, 2)
```

For the fully connected ([linear]((https://pytorch.org/docs/stable/generated/torch.nn.Linear.html))) layer, we specify the number of input neurons and output neurons:

```python
self.fc1 = nn.Linear(400, 120) 
```

You might wonder how to determine the 400 input neurons, given that only the output neurons are displayed in the LeNet block diagram. There are two ways:
1. You can calculate it using the formula below:
   \[
   H_{\text{out}} = \lfloor \frac{H_{\text{in}} + 2 \times \text{padding} - \text{kernelsize} - 1}{\text{stride}} + 1 \rfloor
   \]
2. Alternatively, set it to a random value and add a print statement before the linear layer definition to print the data’s dimensions.

With this knowledge, we can now define all the layers of our CNN:

```python 
class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        
        self.conv1 = nn.Conv2d(1, 6, 5) 
        self.pool1 = nn.AvgPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 3)
        self.pool2 = nn.AvgPool2d(2, 2)

        self.fc1 = nn.Linear(400, 120) 
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
```

Then, we can define the `forward` method, which processes the input through each layer:

```python 
    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool1(x)

        x = self.conv2(x)
        x = F.relu(x)
        x = self.pool2(x)

        # Uncomment the line below to print the dimensions of the data
        # print(x.size())

        # Flatten the 2D data to 1D
        x = x.view(-1, 400) 
        
        x = self.fc1(x)
        x = F.relu(x)

        x = self.fc2(x)
        x = F.relu(x)

        x = self.fc3(x)
        
        return x
```


## Testing our Model on the MNIST Datast

To test our model, we will use images from the [MNIST dataset](https://en.wikipedia.org/wiki/MNIST_database), a widely used collection of grayscale, handwritten digits. This dataset serves as a benchmark for evaluating image classification models, as it provides simple, standardized images that help assess how well the model recognizes basic patterns.

We can load this dataset using PyTorch's `DataLoader` class from the torchvision library. We'll also apply normalization to scale the pixel values. The values for normalization are sourced from [this discussion](https://discuss.pytorch.org/t/mnist-normalizing-and-scaling-the-dataset-at-the-same-time/95218):

```python
import torchvision
import time

test_transform = torchvision.transforms.Compose([
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize((0.1307,), (0.3081,))
])

train_transform = torchvision.transforms.Compose([
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize((0.1307,), (0.3081,))
])

test_loader = torch.utils.data.DataLoader(
    torchvision.datasets.MNIST(
        '.', 
        train=False, 
        download=True, 
        transform=test_transform
    ), 
    batch_size=64, 
    shuffle=False, 
    drop_last=True
)

train_loader = torch.utils.data.DataLoader(
    torchvision.datasets.MNIST(
        '.', 
        train=True, 
        download=True, 
        transform=train_transform
    ), 
    batch_size=64, 
    shuffle=False, 
    drop_last=True
)
```

We can view a sample image from this dataset using the matplotlib library. The following code loads and displays a sample image from the dataset using `matplotlib`, applying a grayscale colormap and no interpolation.


<div style="display: flex; align-items: center; gap: 0px;">
    <div style="flex: 1;">
        {{< highlight python >}}
import matplotlib.pyplot as plt

sample = next(iter(train_loader))[0][0].squeeze()

plt.imshow(sample, cmap='gray', interpolation='none')
        {{< /highlight >}}
    </div>
    <div style="flex: 1;">
        {{< rawhtml >}}
        <figure>
            <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:70%" src="/attachments/mnist_5.png">
        </figure>
        {{< /rawhtml >}}
    </div>
</div>

Once we initialize our model, we can pass this image through our network to see what digit the model predicts:

```python 
net = LeNet()

sample = next(iter(train_loader))[0][0]
net.forward(sample)
```

This produces the following output:

```sh
tensor([[-0.0340,  0.0443, -0.0341, -0.0727,  0.0751,  0.0734,  0.0544, -0.0317, 0.0051, -0.1094]], grad_fn=<AddmmBackward0>)
```

The higher each value is, the more likely the model thinks that the index of that value corresponds to the digit in the image. To get the actual prediction of the digit, we need to take the `argmax` of the output tensor:

```python
torch.argmax(torch.tensor([[-0.0340,  0.0443, -0.0341, -0.0727,  0.0751,  0.0734,  0.0544, -0.0317, 0.0051, -0.1094]]))
```

This returns `torch.tensor(7)`, meaning the model predicts that the digit in the image is 7.

As you can see from the image we depicted earlier, the initial prediction is not accurate. This is expected, as we haven't yet trained our network. To improve its performance, we will implement a training routine for our model.


## Training our LeNet Model


To train our model, we first define the number of epochs, which represents how many times we want to iterate over the entire training dataset. Next, we set up the loss function, which measures how close the model's predictions are to the actual target values. For this, we use [cross-entropy loss](https://en.wikipedia.org/wiki/Cross-entropy), a standard for classification problems. Additionally, we define an optimizer, which is responsible for adjusting the model parameters to minimize the loss. Here, we’ll use [stochastic gradient descent (SGD)](https://en.wikipedia.org/wiki/Stochastic_gradient_descent), but you could also experiment with other popular optimizers, such as [Adam](https://optimization.cbe.cornell.edu/index.php?title=Adam):

```python
n_epochs = 5 

optimizer = torch.optim.SGD(net.parameters(), lr=0.01)
# optimizer = torch.optim.Adam(net.parameters(), lr=0.1)
loss_function = nn.CrossEntropyLoss()
```

We also need to specify the device on which we want to perform the computations, either the `cpu` or `cuda` (if a compatible GPU is available):

```python
net = LeNet()

device = torch.device('cpu')
net.to(device)
```

Next, we iterate over our dataset in batches. The batch size, which we specified earlier in the `train_loader`, determines the number of images processed at once:

```python 
for epoch_n in range(n_epochs):
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        pass 
```

Within this loop, we perform the actual training. We start by clearing any gradients saved from previous iterations with `optimizer.zero_grad()` and transferring both inputs and targets to the device:

```python
optimizer.zero_grad()
inputs, targets = inputs.to(device), targets.to(device)
```

We then compute the model's predictions by passing the inputs through the network. To calculate the loss, we compare these predictions with the actual targets using our loss function:

```python
preds = net(inputs)
loss = loss_function(preds, targets)
```

The final steps involve backpropagating the loss and updating the model’s parameters:

```python 
loss.backward()
optimizer.step()
```

To monitor the training process, we can calculate the accuracy and store both the loss and accuracy values over each epoch:

```python
# Calculate accuracy
predicted_labels = torch.argmax(preds, dim=1)
correct = (predicted_labels == targets).sum().item()
accuracy = correct / targets.size(0)

loss_tmp.append(loss.item())
acc_tmp.append(accuracy)
```

With these steps, we can now train our model. The complete training loop is as follows:

```python
net = LeNet()
device = torch.device('cpu')

optimizer = torch.optim.SGD(net.parameters(), lr=0.01)
loss_function = nn.CrossEntropyLoss()

n_epochs = 5
loss_list = []
acc_list = []

for epoch_n in range(n_epochs):
    loss_tmp = []
    acc_tmp = []

    for batch_idx, (inputs, targets) in enumerate(train_loader):
        optimizer.zero_grad()
        inputs, targets = inputs.to(device), targets.to(device)

        preds = net(inputs)

        # Calculate loss
        loss = loss_function(preds, targets)
        loss.backward()
        optimizer.step()

        # Calculate accuracy
        predicted_labels = torch.argmax(preds, dim=1)
        correct = (predicted_labels == targets).sum().item()
        accuracy = correct / targets.size(0)

        loss_tmp.append(loss.item())
        acc_tmp.append(accuracy)

        if batch_idx % 100 == 0 and batch_idx != 0:
            l_avg = sum(loss_tmp) / len(loss_tmp)
            a_avg = sum(acc_tmp) / len(acc_tmp)

            print(f"Epoch [{epoch_n+1}/{n_epochs}], Batch [{batch_idx // 100}], Avg Loss: {l_avg:.4f}, Avg Acc: {a_avg:.4f}")

            loss_list.append(l_avg)
            acc_list.append(a_avg)
```

## Plotting the Accuracy and Loss of Training


We can plot the loss and accuracy of the training process using the `matplotlib` library to ensure that the training is progressing correctly. Here's how you can visualize the training metrics:

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = [10, 5]

fig, ax = plt.subplots(1)

# Plot accuracy
ax.plot(np.array(acc_list), color='tab:blue')
ax.set_xlabel('Mini-batch steps (100)')
ax.set_ylabel('LeNet Accuracy')
ax.tick_params(colors='tab:blue', axis='y')

# Plot loss
ax2 = ax.twinx()
ax2.plot(np.array(loss_list), color='tab:red', label='Loss')
ax2.set_ylabel('LeNet Loss')
ax2.tick_params(colors='tab:red', axis='y')

ax.set_title('LeNet Training')
```

{{< rawhtml >}}
<figure>
    <img loading="lazy" style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/lenet_loss_acc.png">
</figure>
{{< /rawhtml >}}

After training, when we pass an image through the model again, it now correctly predicts the number in the image:

```python
torch.tensor(5)
```

## Conclusion

With this, you've seen a basic implementation of LeNet, one of the first Convolutional Neural Networks (CNNs). There are many improvements that can be made on top of it, as demonstrated in more advanced architectures like ResNet, InceptionNet, and DeformableNet just to name a few.
