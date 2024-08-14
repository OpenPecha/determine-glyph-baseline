import csv
from PIL import Image
import os
from src.determine_baseline.determine_glyph_metrics import save_glyph_metrics_to_csv_and_visualize

def test_save_glyph_metrics_to_csv_and_visualize(tmpdir):
    test_dir = tmpdir.mkdir("test_data")
    image1 = Image.new('1', (10, 10))
    image2 = Image.new('1', (10, 10))
    image1.save(os.path.join(test_dir, "image1.png"))
    image2.save(os.path.join(test_dir, "image2.png"))

    output_csv = os.path.join(test_dir, "test_metrics.csv")
    output_visual_dir = os.path.join(test_dir, "test_visualizations")
    save_glyph_metrics_to_csv_and_visualize(test_dir, output_csv, output_visual_dir)

    assert os.path.isfile(output_csv)

    assert os.path.isfile(os.path.join(output_visual_dir, "image1_visualization.png"))
    assert os.path.isfile(os.path.join(output_visual_dir, "image2_visualization.png"))

    with open(output_csv, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Check header
    assert rows[0] == ["image name", "baseline", "width", "lsb", "rsb"]

    # Extract rows
    metrics = {row[0]: row[1:] for row in rows[1:]}

    # Define expected metrics
    expected_metrics = {
        "image1.png": ["0", "7", "1", "-1"],
        "image2.png": ["0", "7", "1", "-1"]
    }

    # Assert that the expected metrics match the actual metrics
    assert metrics == expected_metrics

