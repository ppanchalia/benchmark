
# Generated by gen_torchvision_benchmark.py
import torch
import torch.optim as optim
import torchvision.models as models
from ...util.model import BenchmarkModel

class Model(BenchmarkModel):
    def __init__(self, device="cpu", jit=False):
        super().__init__()
        self.device = device
        self.jit = jit
        self.model = models.alexnet()
        if self.jit:
            self.model = torch.jit.script(self.model)
        self.example_inputs = (torch.randn((32, 3, 224, 224)),)

    def get_module(self):
        return self.model, self.example_inputs

    def train(self, niter=3):
        optimizer = optim.Adam(self.model.parameters())
        loss = torch.nn.CrossEntropyLoss()
        for _ in range(niter):
            optimizer.zero_grad()
            pred = self.model(*self.example_inputs)
            y = torch.empty(pred.shape[0], dtype=torch.long).random_(pred.shape[1])
            loss(pred, y).backward()
            optimizer.step()

    def eval(self, niter=1):
        model, example_inputs = self.get_module()
        example_inputs = example_inputs[0][0].unsqueeze(0)
        for i in range(niter):
            model(example_inputs)


if __name__ == "__main__":
    m = Model(device="cuda", jit=True)
    module, example_inputs = m.get_module()
    module(*example_inputs)
    m.train(niter=1)
    m.eval(niter=1)
    