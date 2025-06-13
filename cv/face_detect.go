package main

import (
	"fmt"
	"image"
	"image/color"
	"math"

	"gocv.io/x/gocv"
)

func main() {
	classifier := gocv.NewCascadeClassifier()
	defer classifier.Close()

	if !classifier.Load("data/face_detect.xml") {
		fmt.Println("Error reading cascade file: data/face_detect.xml")
		return
	}

	passportWindow := gocv.NewWindow("passport")
	defer passportWindow.Close()

	selfieWindow := gocv.NewWindow("selfie")
	defer selfieWindow.Close()

	passportImg := gocv.IMRead("data/passport.jpg", gocv.IMReadColor)
	if passportImg.Empty() {
		fmt.Println("Error reading image file")
		return
	}
	defer passportImg.Close()

	selfieImg := gocv.IMRead("data/selfie.jpg", gocv.IMReadColor)
	if selfieImg.Empty() {
		fmt.Println("Error reading image file")
		return
	}
	defer selfieImg.Close()

	// Get the largest faces from both images
	passportFace := detectFace(passportImg, classifier, passportWindow)
	selfieFace := detectFace(selfieImg, classifier, selfieWindow)

	// Compare the faces
	similarity := compareFaces(passportImg, selfieImg, passportFace, selfieFace)
	fmt.Printf("Face similarity score: %.2f%%\n", similarity*100)

	// Determine if it's the same person
	threshold := 0.6 // 60% similarity threshold
	if similarity >= threshold {
		fmt.Println("✅ Faces match! Likely the same person.")
	} else {
		fmt.Println("❌ Faces don't match! Different persons.")
	}
}

// findLargestRectangle returns the rectangle with the largest area
func findLargestRectangle(rects []image.Rectangle) image.Rectangle {
	if len(rects) == 0 {
		return image.Rectangle{}
	}

	largest := rects[0]
	for _, r := range rects[1:] {
		if r.Dx()*r.Dy() > largest.Dx()*largest.Dy() {
			largest = r
		}
	}
	return largest
}

func detectFace(img gocv.Mat, classifier gocv.CascadeClassifier, window *gocv.Window) image.Rectangle {
	// Detect faces
	rects := classifier.DetectMultiScale(img)
	fmt.Printf("Found %d faces\n", len(rects))

	// Find the largest face
	largestFace := findLargestRectangle(rects)

	// Draw rectangles around all faces
	blue := color.RGBA{0, 0, 255, 0}
	green := color.RGBA{0, 255, 0, 0}

	for _, r := range rects {
		gocv.Rectangle(&img, r, blue, 2)
	}

	if !largestFace.Empty() {
		gocv.Rectangle(&img, largestFace, green, 3)
	}

	// Display result
	window.IMShow(img)
	window.WaitKey(0)

	return largestFace
}

// compareFaces compares two faces and returns a similarity score between 0 and 1
func compareFaces(img1, img2 gocv.Mat, face1, face2 image.Rectangle) float64 {
	// Extract face regions
	face1Region := img1.Region(face1)
	face2Region := img2.Region(face2)
	defer face1Region.Close()
	defer face2Region.Close()

	// Resize both faces to the same size for comparison
	targetSize := image.Point{128, 128}
	face1Resized := gocv.NewMat()
	face2Resized := gocv.NewMat()
	defer face1Resized.Close()
	defer face2Resized.Close()

	gocv.Resize(face1Region, &face1Resized, targetSize, 0, 0, gocv.InterpolationLinear)
	gocv.Resize(face2Region, &face2Resized, targetSize, 0, 0, gocv.InterpolationLinear)

	// Convert to grayscale
	face1Gray := gocv.NewMat()
	face2Gray := gocv.NewMat()
	defer face1Gray.Close()
	defer face2Gray.Close()

	gocv.CvtColor(face1Resized, &face1Gray, gocv.ColorBGRToGray)
	gocv.CvtColor(face2Resized, &face2Gray, gocv.ColorBGRToGray)

	// Calculate histogram similarity
	hist1 := calculateHistogram(face1Gray)
	hist2 := calculateHistogram(face2Gray)

	// Compare histograms
	return compareHistograms(hist1, hist2)
}

// calculateHistogram calculates the histogram of a grayscale image
func calculateHistogram(img gocv.Mat) []float64 {
	hist := gocv.NewMat()
	defer hist.Close()

	channels := []int{0}
	histSize := []int{256}
	ranges := []float64{0, 256}

	gocv.CalcHist([]gocv.Mat{img}, channels, gocv.NewMat(), &hist, histSize, ranges, false)

	// Normalize histogram
	gocv.Normalize(hist, &hist, 0, 1, gocv.NormMinMax)

	// Convert histogram to float64 slice
	histData := make([]float64, 256)
	for i := 0; i < 256; i++ {
		histData[i] = float64(hist.GetFloatAt(0, i))
	}
	return histData
}

// compareHistograms compares two histograms and returns a similarity score
func compareHistograms(hist1, hist2 []float64) float64 {
	var sum float64
	for i := range hist1 {
		sum += math.Min(hist1[i], hist2[i])
	}
	return sum
}
