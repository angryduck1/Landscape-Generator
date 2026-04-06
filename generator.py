import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

class MHRNGenerator: #Memory Hill River Noise
    def __init__(self):
        self.array = None
        self.base_value = None

        self.x_max = None
        self.y_max = None

    def clip_base_row(self):
        range_array_higher = []
        range_higher = []
        count = False

        for i in range(self.x_max):
            value = self.array[0, i]

            if float(value) > self.base_value:
                range_array_higher.append(i)
                count = True
            elif (float(value) == self.base_value or float(value) < self.base_value) and count == False:
                pass
            else:
                if range_array_higher and len(range_array_higher) != 1:
                    range_higher.append(list(range_array_higher))
                    range_array_higher.clear()
                    count = False

        if range_array_higher:
            range_higher.append(list(range_array_higher))
            range_array_higher.clear()
            count = False

        return range_higher

    def lerp(self, value, target, speed):
        return value + (target - value) * speed

    def find_average_value(self, y, range_array, array):
        range_values = []

        for i in range_array:
            range_values.append(array[y, i])

        return np.mean(range_values).item()

    def change_range(self, range_array, average_value, max_x):
        if len(range_array) <= 1:
            range_array.clear()
            return

        random_selector = np.random.uniform(0.0, 1.0)

        if random_selector > average_value:
            random_add_left = np.random.randint(0, len(range_array) - 1)
            random_add_right = np.random.randint(0, len(range_array) - 1)

            for i in range(random_add_left):
                index = range_array[0] - i
                if index >= 0 and index < range_array[0]:
                    range_array.insert(0, index)

            for i in range(random_add_right):
                index = range_array[-1] + i
                if index < max_x and index > range_array[-1]:
                    range_array.append(index)
        else:
            max_to_pop = (len(range_array) - 2) // 2

            if max_to_pop > 0:
                random_pop = np.random.randint(0, max_to_pop + 1)

                for i in range(random_pop):
                    range_array.pop(0)

                for i in range(random_pop):
                    range_array.pop(-1)

    def mhrn_generate(self, range_higher):
        for y in range(1, self.y_max):
            for x in range(0, self.x_max):
                target = np.random.uniform(0.0, 0.2)
                self.array[y, x] = self.lerp(self.array[y - 1, x], target, 0.05)

            for current_idx, current_range in enumerate(range_higher):
                if current_range:
                    average_value = self.find_average_value(y - 1, current_range, self.array)

                    self.change_range(current_range, average_value, self.x_max)

                    if len(current_range) == 0:
                        continue

                    target_selector = np.random.uniform(0.0, 1.0)

                    if target_selector > average_value:
                        target = np.random.uniform(0.7, 1.0)
                    else:
                        target = np.random.uniform(0.0, 0.2)

                    offset = np.random.choice([-1, 0, 1], p=[0.2, 0.6, 0.2])

                    new_range = []

                    for idx, i in enumerate(current_range):
                        new_idx = i + offset

                        if 0 <= new_idx < self.x_max:
                            self.array[y, new_idx] = self.lerp(self.array[y - 1, i], target, 0.1)
                            new_range.append(new_idx)

                    range_higher[current_idx] = sorted(new_range)

            range_higher = [r for r in range_higher if len(r) > 0]

    def save_x_y(self, label1, label2, root):
        try:
            self.x_max = int(label1.get())
            self.y_max = int(label2.get())

            print("Successful save!")

            root.destroy()
        except ValueError:
            print("Error! Write integer value!")

    def create_window(self):
        root = Tk()
        root.title("MHRN Generator")

        root.geometry("512x512")

        label1 = Label(root, text="Enter X", font=("Arial", 20))
        label1.pack()

        entry1 = Entry(root, width=20, font=("Arial", 20))
        entry1.pack()

        label2 = Label(root, text="Enter Y", font=("Arial", 20))
        label2.pack()

        entry2 = Entry(root, width=20, font=("Arial", 20))
        entry2.pack()

        button = Button(root, text="Generate MHRN", font=("Arial", 20),
                        command=lambda: self.save_x_y(entry1, entry2, root))
        button.pack()

        root.mainloop()

    def generate(self):
        self.create_window()

        self.array = np.zeros([self.y_max, self.x_max])

        self.array[0, :] = np.random.uniform(0.0, 1.0, self.x_max)
        self.base_value = np.median(self.array[0, :]).item()

        range_higher = self.clip_base_row()

        self.mhrn_generate(range_higher)

        plt.imshow(self.array, vmin=0, vmax=1, cmap='terrain')
        plt.show()