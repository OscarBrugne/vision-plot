# **Vision Plot - User Guide**

## **Overview**

VisionPlot is a modular project combining **Pen Plotter**, which converts images into line-based vector drawings for physical pen plotting, and **Projected Augmented Reality**, which uses a projector and camera system to dynamically overlay predefined visuals onto real-world surfaces. Both modules are powered by a **Process Engine** that manages the global logic.

## **1. Running a Script**

To run a script, follow these steps:

### **Step 1: Navigate to the Project Directory**

Open a terminal and navigate to the relevant directory, for example:

```bash
cd vision-plot/src/svg-utils
```

### **Step 2: Create a Virtual Environment**

If the virtual environment has not been created yet, run:

```bash
python -m venv .venv
```

This will create a virtual environment named `.venv`.

### **Step 3: Activate the Virtual Environment**

- **On Linux/macOS**:

  ```bash
  source .venv/bin/activate
  ```

- **On Windows (CMD)**:

  ```bash
  .\venv\Scripts\activate.bat
  ```

- **On Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### **Step 4: Install Dependencies**

Ensure all required dependencies are installed by running:

```bash
pip install -r requirements.txt
```

### **Step 5: Run a Script**

Once the environment is activated, you can run a script. For example:

```bash
python api/app.py
```

### **Step 6: Deactivate the Virtual Environment**

When finished, deactivate the virtual environment with:

```bash
deactivate
```

---

## **2. Running Unit Tests**

To run unit tests, follow these steps:

### **Step 1: Navigate to the Project Directory**

```bash
cd vision-plot/src/svg-utils
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

## **3. API Endpoints**

Here are the available POST endpoints for SVG generation:

### **/svg/generate_single_path**

This endpoint generates an SVG with a single path defined by a set of points.

#### **Request Format**

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

#### **Response Format**

```
{
    "svg": "<SVG_STRING>"
}
```

### **/svg/generate_multiple_paths**

This endpoint generates an SVG with multiple paths defined by sets of points.

#### **Request Format**

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

#### **Response Format**

```
{
    "svg": "<SVG_STRING>"
}
```
