#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char** argv) {
    if (argc < 2) {
        cerr << "Usage: spot_counter.exe <image_path>" << endl;
        return -1;
    }

    // Load image
    Mat img = imread(argv[1]);
    if (img.empty()) {
        cerr << "❌ Could not open image: " << argv[1] << endl;
        return -1;
    }
    cout << "✅ Loaded image: " << argv[1] << endl;

    // Convert to grayscale for better lighting handling
    Mat gray;
    cvtColor(img, gray, COLOR_BGR2GRAY);

    // Use adaptive threshold to isolate darker regions under variable light
    Mat mask;
    adaptiveThreshold(gray, mask, 255,
                      ADAPTIVE_THRESH_GAUSSIAN_C,
                      THRESH_BINARY_INV, 51, 10);

    // Clean up small noise with morphological ops
    morphologyEx(mask, mask, MORPH_OPEN,
                 getStructuringElement(MORPH_ELLIPSE, Size(3, 3)));

    // Find contours of dark regions
    vector<vector<Point>> contours;
    findContours(mask, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    // Filter out tiny contours (noise)
    int spotCount = 0;
    for (auto &c : contours) {
        double area = contourArea(c);
        if (area > 50) spotCount++;  // ignore small dust/noise
    }

    cout << "🔎 Detected " << spotCount << " dark spots." << endl;
    return 0;
}
