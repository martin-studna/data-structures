import matplotlib.pyplot as plt
import glob

file_list = glob.glob('./out/*')

i=0
for file_name in file_list:
  file = open(file_name, 'r')
  print("file name: ", file_name)
  
  x = []
  y = []
  z = []

  for line in file:
    line = file.readline()
    tokens = line.split()
    print("token-1: ",tokens[0], "token-2: ", tokens[1])
    x.append(float(tokens[0]))
    y.append(float(tokens[1]))
    if len(tokens) == 3:
      z.append(float(tokens[2]))

  if len(z) == 0:
    plt.title(file_name.split("./out/",1)[1])
    plt.plot(x,y)
    plt.xlabel("Set size")
    plt.ylabel("Average number of rotations")
    plt.savefig(f'{file_name.split("./out/",1)[1]}-graph.png')
    plt.close()
  else:
    x1, x2, x3 = [], [], []
    y1, y2, y3 = [], [], []
    for i in range(0, len(x)):
      if x[i] == 10:
        x1.append(y[i])
        y1.append(z[i])
      if x[i] == 100:
        x2.append(y[i])
        y2.append(z[i])
      if x[i] == 1000:
        x3.append(y[i])
        y3.append(z[i])
    plt.title(f'{file_name.split("./out/",1)[1]}-10')
    plt.plot(x1,y1)
    plt.xlabel("Set size")
    plt.ylabel("Average number of rotations")
    plt.savefig(f'{file_name.split("./out/",1)[1]}-10-graph.png')
    plt.close()

    plt.title(f'{file_name.split("./out/",1)[1]}-20')
    plt.plot(x2,y2)
    plt.xlabel("Set size")
    plt.ylabel("Average number of rotations")
    plt.savefig(f'{file_name.split("./out/",1)[1]}-20-graph.png')
    plt.close()

    plt.title(f'{file_name.split("./out/",1)[1]}-30')
    plt.plot(x3,y3)
    plt.xlabel("Set size")
    plt.ylabel("Average number of rotations")
    plt.savefig(f'{file_name.split("./out/",1)[1]}-30-graph.png')
    plt.close()    
  
  i += 1
  
  file.close()