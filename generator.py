width, height, small_size = 60, 60, 1
mesh = open("mesh2d_pro.txt", "w+")

for h in range(0, height, small_size):
    for w in range(0, width, small_size):
        mesh.write(f"{w} {h} {w+1} {h} {w} {h+1}\n")
        mesh.write(f"{w+1} {h+1} {w} {h+1} {w+1} {h}\n")

mesh.close()
