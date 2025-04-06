# **Vision Plot - User Guide**

## **Overview**

VisionPlot is a modular project combining **Pen Plotter**, which converts images into line-based vector drawings for physical pen plotting, and **Projected Augmented Reality**, which uses a projector and camera system to dynamically overlay predefined visuals onto real-world surfaces. Both modules are powered by the [CPEE](https://cpee.org/) **Process Engine** that manages the global logic.

This project was developed as part of the course **"Advanced Practical Course - Sustainable Process Automation: Humans, Software and the Mediator Pattern"** at the **Technical University of Munich (TUM)**.

### **Pen Plotter**

![Projection before calibration](https://github.com/OscarBrugne/vision-plot/static/car.jpg)
![Projection after calibration](https://github.com/OscarBrugne/vision-plot/static/car_spiral_sinus_one_line.png)
![Projected markers after calibration](https://github.com/OscarBrugne/vision-plot/static/car_hilbert_sinus_one_line.png)

### **Projected Augmented Reality**

![Projection before calibration](https://github.com/OscarBrugne/vision-plot/static/projection_before_calibration.png)
![Projection after calibration](https://github.com/OscarBrugne/vision-plot/static/projection_after_calibration.png)
![Projected markers after calibration](https://github.com/OscarBrugne/vision-plot/static/projected_markers_after_calibration.png)

## **1. Running a Script**

To run a script, follow these steps:

### **Step 1: Navigate to the Project Directory**

Open a terminal and navigate to the relevant directory, for example:

```bash
cd vision-plot/svg-utils
```

### **Step 2: Create a Virtual Environment**

If the virtual environment has not been created yet, run:

```bash
python -m venv .venv
```

(or `python3` depending on your system configuration).

This will create a virtual environment named `.venv`.

### **Step 3: Activate the Virtual Environment**

#### **On Linux/macOS**:

```bash
source .venv/bin/activate
```

#### **On Windows (CMD)**:

```cmd
.venv\Scripts\activate.bat
```

#### **On Windows (PowerShell)**:

```powershell
.venv\Scripts\Activate.ps1
```

### **Step 4: Install Dependencies**

Ensure all required dependencies are installed by running:

```bash
pip install -r requirements.txt
```

### **Step 5: Set Environment Variables**

Set the necessary environment variables for the script:

- HOST: The host address for the server
- PORT: The port number for the server

#### **On Linux/macOS**:

```bash
export HOST="::0"
export PORT=18000
```

#### **On Windows (CMD)**:

```cmd
set HOST=::0
set PORT=18000
```

#### **On Windows (PowerShell)**:

```powershell
$env:HOST="::0"
$env:PORT=18000
```

### **Step 6: Run a Script**

Once the environment is activated, you can run a script. For example:

```bash
python svg_utils/app.py
```

### **Step 7: Deactivate the Virtual Environment**

When finished, deactivate the virtual environment with:

```bash
deactivate
```

---

## **2. Running Unit Tests**

To run unit tests, follow these steps:

### **Step 1: Navigate to the Project Directory**

```bash
cd vision-plot/svg-utils/svg_utils
```

### **Step 2: Activate the Virtual Environment**

(Refer to the previous section if it's not already activated.)

### **Step 3: Run Tests with `unittest`**

To run all tests:

```bash
python -m unittest discover
```

Or to test a specific file:

```bash
python -m unittest test_svg_builder.py
```

### **Step 4: Deactivate the Virtual Environment**

```bash
deactivate
```

---

## **3. CPEE**

CPEE (Cloud Process Execution Engine) is a process engine that allows you to create and manage processes in a modular way.
To run the project with CPEE, you can import the testset files (xml) into the CPEE GUI and execute `main_project_images.xml`.
The `generate_projector_calibration_image.xml` is not actually implemented, the image has been generated manually.

---

## **4. API Endpoints**

### **SVG Utils API**

Here are the available POST endpoints for SVG Utils module:

#### **/svg/generate_single_path**

This endpoint generates an SVG with a single path defined by a set of points.

##### **Request Format**

```
{
    "points": [[x1, y1], [x2, y2], ...],
    "size": [width, height],
    "viewbox": [x, y, width, height] (optional),
    "is_closed_path": bool (optional),
    "stroke": "color" (optional, default "black"),
    "stroke_width": int (optional, default 1)
}
```

##### **Response Format**

```
{
    "svg": "<SVG_STRING>"
}
```

#### **/svg/generate_multiple_paths**

This endpoint generates an SVG with multiple paths defined by sets of points.

##### **Request Format**

```
{
    "paths": [[[x1, y1], [x2, y2], ...], [[x1, y1], [x2, y2], ...], ...],
    "size": [width, height],
    "viewbox": [x, y, width, height] (optional),
    "is_closed_path": bool (optional),
    "stroke": "color" (optional, default "black"),
    "stroke_width": int (optional, default 1)
}
```

##### **Response Format**

```
{
    "svg": "<SVG_STRING>"
}
```

### **Projected Augmented Reality API**

Here are the available endpoints for the Projected AR module:

#### **Camera API**

##### **POST /camera**

Opens a new camera stream.

###### **Request Format**

```
{
    "source": int (optional, default 0)
}
```

###### **Response Format**

```
{
    "message": "Camera opened successfully.",
    "camera_id": int,
    "camera_source": int
}
```

##### **GET /camera/<camera_id>**

Retrieves information about a specific camera.

###### **Response Format**

```
{
    "camera_id": int,
    "camera_source": int
}
```

##### **DELETE /camera/<camera_id>**

Closes the specified camera stream.

###### **Response Format**

```
{
    "message": "Camera with ID '<camera_id>' closed successfully."
}
```

##### **POST /camera/<camera_id>/capture**

Captures an image from the specified camera.

###### **Response Format**

```
{
    "message": "Image captured successfully.",
    "camera_id": int,
    "capture_id": int,
    "capture_filename": "string",
    "capture_filepath": "string",
    "capture_url": "string"
}
```

---

#### **Projector Calibration API**

##### **POST /projector-calibration/detect-markers**

Detects ArUco markers in an image.

###### **Request Format**

```
{
    "capture_filepath": "string",
    "aruco_dict_type": "string"
}
```

###### **Response Format**

```
{
    "detected_markers": {
        "marker_id": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
        ...
    }
}
```

##### **POST /projector-calibration/calculate-homography-correction**

Calculates the homography correction for the projector.

###### **Request Format**

```
{
    "detected_markers": {
        "marker_id": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
        ...
    },
    "real_markers": {
        "marker_id": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
        ...
    },
    "projected_markers": {
        "marker_id": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
        ...
    }
}
```

###### **Response Format**

```
{
    "homography_correction": [
        [h11, h12, h13],
        [h21, h22, h23],
        [h31, h32, h33]
    ]
}
```

##### **POST /projector-calibration/apply-homography**

Applies a homography transformation to an image.

###### **Request Format**

```
{
    "image_filepath": "string",
    "homography": [
        [h11, h12, h13],
        [h21, h22, h23],
        [h31, h32, h33]
    ]
}
```

###### **Response Format**

```
{
    "message": "Homography applied successfully.",
    "corrected_image_filepath": "string",
    "corrected_image_url": "string"
}
```
