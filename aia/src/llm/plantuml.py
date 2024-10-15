import plantuml 

import matplotlib.pyplot as plt

# Define the PlantUML code
plantuml_code = """
@startuml
title Dog Class Diagram

class Animal {
  - name: String
  - age: int
  + eat()
  + sleep()
} left

class Dog extends Animal {
  - breed: String
  - size: String
  + bark()
  + wagTail()
} right

@enduml
"""

# Create a PlantUML object
puml = plantuml()

# Render the PlantUML code to a PNG file
puml.render(plantuml_code, "dog_class_diagram.png")

plt.imshow(plt.imread("dog_class_diagram.png"))
plt.show()
