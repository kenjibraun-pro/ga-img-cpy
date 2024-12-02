# genetic_algorithm.py
import copy
import random

from genome import Genome


def initialize_population(
    population_size: int, max_shapes: int, image_width: int, image_height: int
) -> list[Genome]:
    return [
        Genome(max_shapes, image_width, image_height) for _ in range(population_size)
    ]


def select_elite(population: list[Genome], elite_size: int) -> list[Genome]:
    return population[:elite_size]


def crossover(
    parent1: Genome, parent2: Genome, image_width: int, image_height: int
) -> Genome:
    shapes1 = parent1.shapes
    shapes2 = parent2.shapes
    cutoff = random.randint(0, min(len(shapes1), len(shapes2)))
    # Deep copy the shapes to prevent shared mutable state
    child_shapes = [
        copy.deepcopy(shape) for shape in shapes1[:cutoff] + shapes2[cutoff:]
    ]
    return Genome(
        max_shapes=0,
        image_width=image_width,
        image_height=image_height,
        shapes=child_shapes,
    )


def mutate_population(
    population: list[Genome],
    mutation_rate: float,
    max_shapes: int,
    image_width: int,
    image_height: int,
) -> list[Genome]:
    for genome in population:
        genome.mutate(mutation_rate, max_shapes, image_width, image_height)
    return population
