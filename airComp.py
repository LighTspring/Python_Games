import torch as t
import torch.nn as nn
import torch.optim as optim


class airCompDNN(nn.Module):
    def __init__(self, N, K):
        super(airCompDNN, self).__init__()
        self.hidden_layer1 = nn.Linear(2 * N * K, 128)
        self.hidden_layer2 = nn.Linear(128, 64)
        self.output_layer = nn.Linear(64, K + 4 * N)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.hidden_layer1(x))
        x = self.relu(self.hidden_layer2(x))
        x = self.sigmoid(self.output_layer(x))
        return x


T0 = 10 ** (-25 / 10)  # -25dB,the pass loss at the reference distance
d = 1e3  # the distance between the transmitter and the receiver
d0 = 1
beta = 10
a = 2.2
P0 = 10 ** (40 / 10) * 1e-3  # 40dBm
sigma2 = 10 ** (-90 / 10) * 1e-3  # -90dBm
N = 10  # IACE consisting of N devices
K = 100  # RIS equipped with K passive reflective elements
HLoS = t.randn((K, N)) + 1j * t.randn((K, N))
HNLoS = t.randn((K, N)) + 1j * t.randn((K, N))
H = (T0 * (d0 / d) ** a)**0.5 * ((beta / (beta + 1))**0.5 * HLoS + (1 / (beta + 1))**0.5 * HNLoS)
# print(H.real)
# print(H.imag)
tempH = t.stack((H.real.T, H.imag.T), dim=1)  # (N,,2,K)
F = t.flatten(tempH)  # Features,(2NK,)
def customLoss(N, K):
    def Loss(output):
        fun = lambda x: t.exp(1j * 2 * t.pi * x)
        v = fun(output[:K])
        b = output[K:K+N]*P0**0.5*fun(output[K+N:K+2*N])
        B = 1e6
        c = output[K+2*N:K+3*N]*B*fun(output[K+3*N:])
        mse = t.abs(c*b*((H.conj().T*v[None,:])[:,None,:]@H).sum(dim=2)[:,0]-1)**2+sigma2*t.abs(c)**2
        return mse.sum()/N
    return Loss
# training
model = airCompDNN(N, K)
criterion = customLoss(N,K)  # defined myself
optimizer = optim.Adam(model.parameters(), lr=0.1)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.33, patience=10)  # set the learning rate scheduler
best_loss = float('inf')
epochs_without_improvement = 0

for epoch in range(150):
    output = model(F)
    loss = criterion(output)
    loss.backward()
    optimizer.step()
    scheduler.step(loss)
    if loss < best_loss:
        best_loss = loss
        epochs_without_improvement = 0
    else:
        epochs_without_improvement += 1
    print(f"Epoch: {epoch + 1},Loss: {loss.item()}")
    if epochs_without_improvement >= 100:
        print("Early stopping triggered")
        break
