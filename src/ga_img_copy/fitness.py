# fitness.py

from genome import Genome
import numpy as np
from numpy.typing import NDArray
from renderer import render_genome
from skimage.metrics import mean_squared_error


def fitness_worker(
    genome: Genome, target_array: NDArray[np.uint8], image_width: int, image_height: int
) -> Genome:
    generated_image = render_genome(genome, image_width, image_height)
    generated_array = np.array(generated_image)
    mse = mean_squared_error(target_array, generated_array)
    genome.fitness = mse
    return genome
