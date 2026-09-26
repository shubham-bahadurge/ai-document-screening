import cv2
import os


def preprocess_image(input_path):
    """
    Prepare a document image for better OCR.

    Returns:
        processed_path: path to the processed image
        details: preprocessing information
    """

    image = cv2.imread(input_path)

    if image is None:
        raise ValueError("Unable to read image")

    original_height, original_width = image.shape[:2]


    # --------------------------------
    # 1. RESIZE
    # --------------------------------

    scale = 1

    if original_width < 1200:

        scale = 1200 / original_width

        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        image = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_CUBIC
        )


    # --------------------------------
    # 2. GRAYSCALE
    # --------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # --------------------------------
    # 3. NOISE REDUCTION
    # --------------------------------

    denoised = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )


    # --------------------------------
    # 4. CONTRAST ENHANCEMENT
    # --------------------------------

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(
        denoised
    )


    # --------------------------------
    # 5. ADAPTIVE THRESHOLD
    # --------------------------------

    processed = cv2.adaptiveThreshold(
        enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )


    # --------------------------------
    # SAVE PROCESSED IMAGE
    # --------------------------------

    directory = os.path.dirname(input_path)

    filename = os.path.basename(input_path)

    name, extension = os.path.splitext(
        filename
    )

    processed_filename = (
        name + "_processed.png"
    )

    processed_path = os.path.join(
        directory,
        processed_filename
    )


    cv2.imwrite(
        processed_path,
        processed
    )


    return processed_path, {

        "original_width": original_width,

        "original_height": original_height,

        "processed_width": processed.shape[1],

        "processed_height": processed.shape[0],

        "resized": scale != 1,

        "grayscale": True,

        "noise_reduction": True,

        "contrast_enhancement": True,

        "thresholding": True
    }