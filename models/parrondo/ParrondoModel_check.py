from ParrondoModel import ParrondoModel

model = ParrondoModel(100)

for i in range(2000):
    model.step()


