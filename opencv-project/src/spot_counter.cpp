#include <opencv2/opencv.hpp>
#include <iostream>
using namespace cv;

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: spot_counter.exe <image_path>" << std::endl;
        return -1;
    }

    // Load image
    cv::Mat img = cv::imread(argv[1]);
    if (img.empty()) {
        std::cerr << "❌ Could not open image: " << argv[1] << std::endl;
        return -1;
    }
    std::cout << "✅ Successfully loaded image: " << argv[1] << std::endl;

    // Convert to HSV
    cv::Mat hsv;
    cv::cvtColor(img, hsv, cv::COLOR_BGR2HSV);

    // Mask for dark/black areas
    cv::Mat badMask;
    cv::inRange(hsv, cv::Scalar(0, 0, 0), cv::Scalar(180, 255, 50), badMask);

    // Find contours
    std::vector<std::vector<cv::Point>> contours;
    cv::findContours(badMask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

    std::cout << "🔎 Detected " << contours.size() << " dark spots." << std::endl;

    return 0;
}

