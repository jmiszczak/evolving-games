from PDGridModel import PDGridModel

# only for testing the procedure
model = PDGridModel(50,10,10,1)

for i in range(20):
    model.step()


