# 🚀 ISRO Mars Rover Landing Surface Analysis

This repository presents an unsupervised statistical approach for analyzing Martian surface point cloud data to identify safe landing zones for the ISRO Mars Rover mission. The methodology is focused on differentiating smooth (flat) and rough (curved) regions through local geometry and curvature analysis.
![Segmented-Surface](https://github.com/user-attachments/assets/52d26f2a-8199-4588-b175-64991f368b37)
![Mars-Surface](https://github.com/user-attachments/assets/6a440497-0c0f-4c1c-92b3-db5f2250957a)

---

## 📌 Objective

To develop an unsupervised pipeline that:
- Segments 3D point cloud data into smooth and rough regions.
- Identifies flat, safe landing zones based on curvature and clustering techniques.

---

## 🧠 Core Methodology
![Roadmap](https://github.com/user-attachments/assets/8264475b-41aa-4cf3-a898-b8ecc27c7200)

### 🔹 Local Geometry Estimation
- **k-Nearest Neighbors (kNN):** Identifies local neighborhood for each point.
- **Principal Component Analysis (PCA):** Computes eigenvalues of the covariance matrix to understand local surface shape.

### 🔹 Curvature Estimation
- **Curvature Metric (κ):**  
  κ = λ_{min}/{λ_1 + λ_2 + λ_3} 
  A lower κ indicates flatter surface areas.

### 🔹 Thresholding
- Points are classified as **smooth** or **rough** using a curvature threshold `τ`.

### 🔹 Clustering
- Spatial clustering (e.g., region growing) groups smooth points to form contiguous flat landing zones.

---

## ✅ Advantages

- **Unsupervised:** Requires no labeled data.
- **Robust:** Relies on statistical properties, making it noise-tolerant.
- **Scalable:** Can be extended to multi-scale analysis.
- **Versatile:** Applicable to various 3D datasets (LiDAR, stereo vision, depth sensors).

---

## 🚁 Applications

- Mars Rover **safe landing zone detection**
- Autonomous **terrain navigation**
- 3D **environmental segmentation** for robotics

---

## 📄 Report Summary

The approach was tested on Martian surface point clouds and demonstrated strong performance in:
- Identifying statistically flat regions.
- Avoiding misleading isolated points via clustering.
- Offering a reliable alternative in the absence of labeled terrain data.

---

## 📂 Files

- `ISRO-Report.pdf`: Complete technical documentation.
- `Dataset`: [Link](https://drive.google.com/file/d/1Tze5Je0KvKmqpZj6ZC2jjbLE5x_8Zc8r/view?usp=sharing)

---

## 🛰️ Acknowledgments

This project is part of a research effort supporting ISRO’s Mars Exploration Program. Special thanks to the data simulation and mission planning teams.

---

## 📬 Contact

For questions or collaboration, please contact:
**Satyam Swayamjeet Sahoo**  
Email: [satyam7772004@gmail.com](mailto:satyam7772004@gmail.com)

---

