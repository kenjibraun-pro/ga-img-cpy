# genome.py
import random


class Shape:
    def __init__(self, image_width: int, image_height: int) -> None:
        self.type: str = random.choice(["circle", "rectangle"])
        self.position: tuple[int, int] = (
            random.randint(0, image_width),
            random.randint(0, image_height),
        )
        self.color: tuple[int, int, int] = (
            random.randint(0, 255),  # Red
            random.randint(0, 255),  # Green
            random.randint(0, 255),  # Blue
        )

        if self.type == "circle":
            self.radius: int = random.randint(5, min(image_width, image_height) // 4)
            # Circles do not have rotation
        elif self.type == "rectangle":
            self.width: int = random.randint(5, image_width // 2)
            self.height: int = random.randint(5, image_height // 2)
            self.rotation: float = random.uniform(0, 360)

    def mutate(self, mutation_rate: float, image_width: int, image_height: int) -> None:
        if random.random() < mutation_rate:
            self.type = random.choice(["circle", "rectangle"])
            # Reinitialize shape-specific attributes
            if self.type == "circle":
                self.radius = random.randint(5, min(image_width, image_height) // 4)
                # Remove rectangle-specific attributes
                if hasattr(self, "width"):
                    del self.width
                if hasattr(self, "height"):
                    del self.height
                if hasattr(self, "rotation"):
                    del self.rotation
            elif self.type == "rectangle":
                self.width = random.randint(5, image_width // 2)
                self.height = random.randint(5, image_height // 2)
                self.rotation = random.uniform(0, 360)
                # Remove circle-specific attributes
                if hasattr(self, "radius"):
                    del self.radius

        if random.random() < mutation_rate:
            new_x = random.randint(0, image_width)
            new_y = random.randint(0, image_height)
            self.position = (new_x, new_y)

        if random.random() < mutation_rate:
            self.color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

        if self.type == "circle":
            if random.random() < mutation_rate:
                self.radius = random.randint(5, min(image_width, image_height) // 4)
            # No rotation for circles

        elif self.type == "rectangle":
            if random.random() < mutation_rate:
                self.width = random.randint(5, image_width // 2)
            if random.random() < mutation_rate:
                self.height = random.randint(5, image_height // 2)
            if random.random() < mutation_rate:
                self.rotation = random.uniform(0, 360)


class Genome:
    def __init__(
        self,
        max_shapes: int,
        image_width: int,
        image_height: int,
        shapes: list[Shape] | None = None,
    ) -> None:
        if shapes is not None:
            self.shapes: list[Shape] = shapes
        else:
            num_shapes = random.randint(1, max_shapes) if max_shapes > 0 else 0
            self.shapes = [Shape(image_width, image_height) for _ in range(num_shapes)]
        self.fitness: float | None = None

    def mutate(
        self, mutation_rate: float, max_shapes: int, image_width: int, image_height: int
    ) -> None:
        # Mutate existing shapes
        for shape in self.shapes:
            shape.mutate(mutation_rate, image_width, image_height)
        # Add a new shape
        if len(self.shapes) < max_shapes and random.random() < mutation_rate:
            self.shapes.append(Shape(image_width, image_height))
        # Remove a shape
        if len(self.shapes) > 1 and random.random() < mutation_rate:
            self.shapes.pop(random.randint(0, len(self.shapes) - 1))
