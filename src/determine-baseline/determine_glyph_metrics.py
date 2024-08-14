import os
import numpy as np
from PIL import Image
import csv
import matplotlib.pyplot as plt


def convert_to_binary_image(image):
    if image.mode != '1':
        return image.convert('1')
    return image


def extract_black_pixels(image_array):
    return np.where(image_array == 0)


def calculate_edges_and_width(black_pixels):
    top_edge = black_pixels[0].min()
    left_edge = black_pixels[1].min()
    right_edge = black_pixels[1].max()
    glyph_width = right_edge - left_edge
    return top_edge, left_edge, right_edge, glyph_width


def calculate_baseline(image_array, top_edge):
    top_row_black_pixels = np.where(image_array[top_edge, :] == 0)[0]
    baseline_start = top_row_black_pixels.min() + 1
    baseline_end = top_row_black_pixels.max() + 1
    return baseline_start, baseline_end, 


def calculate_side_bearings(left_edge, right_edge, baseline_start, baseline_end):
    lsb = baseline_start - left_edge
    rsb = right_edge - baseline_end
    return lsb, rsb


def get_glyph_metrics(image):
    binary_image = convert_to_binary_image(image)
    image_array = np.array(binary_image)
    image_array = image_array[:, 1:-1]

    black_pixels = extract_black_pixels(image_array)
    if black_pixels[0].size == 0 or black_pixels[1].size == 0:
        return None

    top_edge, left_edge, right_edge, glyph_width = calculate_edges_and_width(black_pixels)
    baseline_start, baseline_end = calculate_baseline(image_array, top_edge)
    lsb, rsb = calculate_side_bearings(left_edge, right_edge, baseline_start, baseline_end)

    return {
        'top_edge': top_edge,
        'left_edge': left_edge,
        'right_edge': right_edge,
        'glyph_width': glyph_width,
        'lsb': lsb,
        'rsb': rsb,
        'baseline_start': baseline_start,
        'baseline_end': baseline_end
    }


def visualize_glyph_metrics(image, metrics, output_path):
    binary_image = convert_to_binary_image(image)
    image_array = np.array(binary_image)

    fig, ax = plt.subplots()
    ax.imshow(image_array, cmap='gray')
    # baseline
    ax.axhline(y=metrics['top_edge'], color='red', linestyle='--', label='baseline')

    # left edge and right edge lines
    ax.axvline(x=metrics['left_edge'], color='blue', linestyle='--', label='left edge')
    ax.axvline(x=metrics['right_edge'], color='green', linestyle='--', label='right edge')

    # baseline start and end
    ax.axvline(x=metrics['baseline_start'], color='orange', linestyle='--', label='baseline starts')
    ax.axvline(x=metrics['baseline_end'], color='purple', linestyle='--', label='baseline ends')

    ax.legend()
    plt.title(f"metric visualization: {os.path.basename(output_path)}")
    plt.savefig(output_path)
    plt.close()


def save_glyph_metrics_to_csv_and_visualize(directory, output_csv, output_visual_dir):
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image Name", "Baseline", "Width", "LSB", "RSB"])

        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                image_path = os.path.join(directory, filename)
                image = Image.open(image_path)
                metrics = get_glyph_metrics(image)

                if metrics:
                    writer.writerow([
                        filename,
                        metrics['top_edge'],
                        metrics['glyph_width'],
                        metrics['lsb'],
                        metrics['rsb']
                    ])
                    output_visual_path = os.path.join(
                        output_visual_dir, f"{os.path.splitext(filename)[0]}_visualization.png")
                    visualize_glyph_metrics(image, metrics, output_visual_path)


def main():
    directory_path = '../../data/glyph_images'
    output_csv = '../../data/glyph_metrics_csv/glyph_metrics.csv'
    output_visual_dir = '../../data/glyph_visualizations'
    
    os.makedirs(output_visual_dir, exist_ok=True)
    save_glyph_metrics_to_csv_and_visualize(directory_path, output_csv, output_visual_dir)


if __name__ == "__main__":
    main()
