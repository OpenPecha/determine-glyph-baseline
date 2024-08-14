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

        assert rows[0] == ["image name", "baseline", "width", "lsb", "rsb"]
        expected_image1_row = ["image1.png", "0", "7", "1", "-1"]
        expected_image2_row = ["image2.png", "0", "7", "1", "-1"]

        assert rows[1] == expected_image1_row
        assert rows[2] == expected_image2_row
