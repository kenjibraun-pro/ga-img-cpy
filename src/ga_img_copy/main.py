# main.py
import copy
import math
import random

from fitness import fitness_worker
from genetic_algorithm import (
    crossover,
    initialize_population,
    mutate_population,
    select_elite,
)
from genome import Genome
from mpire import WorkerPool
import numpy as np
from PIL import Image
from renderer import render_genome
from rich.progress import Progress
import typer


app = typer.Typer()


@app.command()
def evolve(
    target_image_path: str = typer.Argument(..., help="Path to the target image"),
    population_size: int = typer.Option(50, help="Size of the population"),
    generations: int = typer.Option(1000, help="Number of generations to evolve"),
    mutation_rate: float = typer.Option(0.1, help="Mutation rate"),
    elite_size: int = typer.Option(5, help="Number of elite individuals to carry over"),
    max_shapes: int = typer.Option(50, help="Maximum number of shapes in a genome"),
) -> None:
    """Evolve an image to match the target image using a genetic algorithm."""
    # Load the target image and get dimensions
    target_image = Image.open(target_image_path).convert("RGB")
    image_width, image_height = target_image.size
    target_array = np.array(target_image)

    # Initialize population
    population: list[Genome] = initialize_population(
        population_size, max_shapes, image_width, image_height
    )

    # Set up progress bar
    progress = Progress()
    task = progress.add_task("[green]Evolving...", total=generations)

    # Store best genomes for GIF
    best_genomes: list[Genome] = []

    with progress:
        for generation in range(generations):
            # Prepare arguments for mpire
            args = [
                (genome, target_array, image_width, image_height)
                for genome in population
            ]

            # Evaluate fitness in parallel
            with WorkerPool() as pool:
                population = pool.map(fitness_worker, args)

            # Sort population by fitness
            population.sort(
                key=lambda x: x.fitness if x.fitness is not None else math.inf
            )

            # Log best fitness
            best_fitness = population[0].fitness
            progress.console.log(
                f"Generation {generation}: Best Fitness = {best_fitness:.4f}"
            )

            # Save best genome (deep copy to prevent modifications)
            best_genomes.append(copy.deepcopy(population[0]))

            # Check for termination condition (optional)
            if best_fitness == 0:
                break

            # Selection
            elite = select_elite(population, elite_size)

            # Create new population with deep copies of elites
            new_population = [copy.deepcopy(genome) for genome in elite]

            # Generate offspring
            offspring: list[Genome] = []
            while len(new_population) + len(offspring) < population_size:
                parent1, parent2 = random.sample(elite, 2)
                child = crossover(parent1, parent2, image_width, image_height)
                offspring.append(child)

            # Mutate offspring (not elites)
            offspring = mutate_population(
                offspring, mutation_rate, max_shapes, image_width, image_height
            )

            # Combine elites and mutated offspring to form the new population
            population = new_population + offspring

            progress.update(task, advance=1)

    # Save the final image
    best_image = render_genome(population[0], image_width, image_height)
    best_image.save("evolved_image.png")

    # Generate GIF
    generate_gif(best_genomes, target_image, image_width, image_height)

    progress.console.log("[bold green]Evolution complete![/bold green]")


def generate_gif(
    best_genomes: list[Genome],
    target_image: Image.Image,
    image_width: int,
    image_height: int,
) -> None:
    frames = []
    target_image = target_image.convert("RGB")  # Ensure target image is in RGB mode
    for genome in best_genomes:
        generated_image = render_genome(genome, image_width, image_height)
        # Combine the target image and generated image side by side
        combined_width = target_image.width + generated_image.width
        combined_height = max(target_image.height, generated_image.height)
        combined_image = Image.new("RGB", (combined_width, combined_height))
        combined_image.paste(target_image, (0, 0))
        combined_image.paste(generated_image, (target_image.width, 0))
        frames.append(combined_image)

    # Save the frames as an animated GIF
    frames[0].save(
        "evolution.gif", save_all=True, append_images=frames[1:], duration=100, loop=0
    )


if __name__ == "__main__":
    app()
