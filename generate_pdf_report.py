import os
import sys
import subprocess

def install_and_import(package):
    try:
        __import__(package)
        print(f"'{package}' is already installed.")
    except ImportError:
        print(f"'{package}' not found. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed '{package}'.")

# Ensure reportlab is installed
install_and_import('reportlab')

# Now import ReportLab modules
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# --- Numbered Canvas for Running Headers and Page Numbers (Page X of Y) ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Suppress headers/footers on the cover page (Page 1)
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(54, 750, "ONCODETECT AI - DISEASE DETECTION WEB APPLICATION")
            
            # Header Rule
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
            # Footer Rule
            self.line(54, 55, 558, 55)
            
            # Footer - Page Number
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 42, "CONFIDENTIAL - CLINICAL PATHOLOGY RESEARCH REPORT")
            
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 42, page_text)
            
        self.restoreState()

# --- Main PDF Generator Function ---
def generate_report(output_filename="OncoDetect_AI_Project_Report.pdf"):
    print(f"Generating PDF report: {output_filename}...")
    
    # Page settings: Letter size with 0.75-inch (54 pt) margins
    # Total printable width = 612 - 108 = 504 pt
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_color = colors.HexColor("#0F172A")    # Dark Slate 900
    secondary_color = colors.HexColor("#1D4ED8")  # Royal Blue 700
    accent_color = colors.HexColor("#0D9488")     # Teal 600
    text_color = colors.HexColor("#334155")       # Slate 700
    border_color = colors.HexColor("#E2E8F0")     # Slate 200
    bg_light = colors.HexColor("#F8FAFC")         # Slate 50
    
    # Modify/Create Paragraph Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=primary_color,
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#475569"),
        spaceAfter=40
    )
    
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748B")
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=secondary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Header3',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=accent_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_color,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        backColor=bg_light,
        borderColor=border_color,
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8
    )
    
    story = []
    
    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 1.5 * inch))
    
    # Decorative Top Bar (Teal Accent)
    d_bar = Table([['']], colWidths=[504], rowHeights=[6])
    d_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), accent_color),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(d_bar)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("OncoDetect AI", title_style))
    story.append(Paragraph("AI-Powered Histopathological Cancer Detection Web Application", subtitle_style))
    
    story.append(Spacer(1, 2.0 * inch))
    
    # Metadata block
    meta_text = """
    <b>DOCUMENT TYPE:</b> Comprehensive Project Technical Report<br/>
    <b>APPLICATION DOMAIN:</b> Clinical Deep Learning Diagnostics (PCam Dataset)<br/>
    <b>TARGET AUDIENCE:</b> Medical Professionals, Developers, Stakeholders<br/>
    <b>VERSION:</b> 1.0.0 (Production Release)<br/>
    <b>DATE:</b> May 2026<br/>
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(PageBreak())
    
    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Capabilities", h1_style))
    
    summary_text = """
    <b>OncoDetect AI</b> is a state-of-the-art, full-stack, AI-powered disease detection web application
    specializing in the identification of metastatic breast cancer from histopathological tissue patches.
    Utilizing the PatchCamelyon (PCam) dataset benchmark, the system integrates deep learning image classifiers
    with a robust defensive quality-control validation pipeline and an interactive frontend client to form a cohesive,
    clinically viable diagnostic assistant.
    """
    story.append(Paragraph(summary_text, body_style))
    
    capabilities_intro = "Key system capabilities include:"
    story.append(Paragraph(capabilities_intro, body_style))
    
    caps = [
        "<b>Defensive Quality Gates:</b> Pre-screens and rejects out-of-focus, blank, grayscale (CT/MRI/X-ray), and text screenshot images to prevent corrupt input data from reaching the core models.",
        "<b>Autonomous Restoration Layer:</b> Restores focus and removes image acquisition noise dynamically using bilateral edge-preserving filters and unsharp masking algorithms.",
        "<b>Transfer Learning Classification:</b> Implements a MobileNetV2 verification network combined with a custom sigmoid classifier head to confirm histopathological color profile compliance.",
        "<b>Explainable AI (Grad-CAM):</b> Dynamically generates gradient-weighted class activation maps, displaying a spatial attention heatmap highlighting key cellular abnormalities.",
        "<b>Microscope Motion Hooks:</b> Connects to live electronic feeds, running pixel-differencing motion analysis in the browser to auto-capture cells upon focus lock.",
        "<b>Clinical PDF Reporting:</b> Generates formatted physical and digital reports including patient metadata, confidence percentages, visual reference heatmaps, and doctor review sign-offs."
    ]
    for cap in caps:
        story.append(Paragraph(f"• {cap}", bullet_style))
        
    story.append(Spacer(1, 10))
    
    # =========================================================================
    # SECTION 2: SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("2. System Architecture & Relational Schema", h1_style))
    
    arch_text = """
    The application utilizes a distributed client-server model designed for containerized deployment.
    The frontend (React + Vite) communicates with the backend (FastAPI) via structured JSON and multipart
    form-data HTTP requests. The backend leverages SQLAlchemy to perform database transactions on a SQLite database.
    """
    story.append(Paragraph(arch_text, body_style))
    
    story.append(Paragraph("Database Table Definitions", h2_style))
    
    # Table data for DB Entities
    db_data = [
        [Paragraph("<b>Table</b>", body_style), Paragraph("<b>Description</b>", body_style), Paragraph("<b>Key Attributes</b>", body_style)],
        [Paragraph("<b>users</b>", body_style), Paragraph("Stores registered pathologists and system administrators.", body_style), Paragraph("id (PK), username (Unique), email (Unique), hashed_password, is_admin", body_style)],
        [Paragraph("<b>patients</b>", body_style), Paragraph("Keeps patient records including Medical Record Numbers (MRN) and details.", body_style), Paragraph("id (PK), patient_id (Unique MRN), name, age, gender, doctor_id (FK to users)", body_style)],
        [Paragraph("<b>predictions</b>", body_style), Paragraph("Logs diagnostic scans, model outputs, confidence metrics, and timestamps.", body_style), Paragraph("id (PK), filename, prediction_label, confidence_score, user_id (FK), patient_id (FK)", body_style)]
    ]
    
    db_table = Table(db_data, colWidths=[80, 220, 204])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('BOX', (0,0), (-1,-1), 1, primary_color),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(db_table)
    
    story.append(PageBreak())
    
    # =========================================================================
    # SECTION 3: BACKEND DEEP DIVE
    # =========================================================================
    story.append(Paragraph("3. Backend Implementation Detail (FastAPI & ML Core)", h1_style))
    
    backend_intro = """
    The backend exposes REST API endpoints for user accounts, patient records, and machine learning predictions.
    Here is an breakdown of the backend scripts and their individual functions:
    """
    story.append(Paragraph(backend_intro, body_style))
    
    # Files listing
    files_detail = [
        ("main.py", "Acts as the application entry point. Initializes CORS middleware, maps base metadata definitions, and binds standard request routes. Implements /api/register, /api/token, /api/predict (which handles patient indexing and executes inference), /api/predictions/history, and /api/admin/stats."),
        ("auth.py", "Manages credentials hashing and JWT verification. Utilizes passlib with the bcrypt scheme to secure passwords in transit, and jose to create access tokens. Extracts authorization headers to resolve request contexts dynamically via get_current_user dependencies."),
        ("database.py", "Defines the connection pool. Exposes get_db() generators that bind sessions to FastAPI endpoints, returning database contexts and closing them upon transaction completion."),
        ("models.py", "Declares SQLAlchemy models representing the relational database tables. Configures foreign key relations and maps back-populating ORM properties for user-patient-prediction trees."),
        ("schemas.py", "Declares Pydantic schemas validating input payloads and output serialization configurations."),
        ("ml_utils.py", "Manages the core TensorFlow cancer detection model load and inference logic. Defines preprocess_image() (scaling inputs to 96x96x3 normalized arrays) and get_prediction() (returning diagnostic classes, confidence scores, and heatmaps). Includes fallbacks to mock simulations if running on incompatible CPU environments.")
    ]
    
    for filename, desc in files_detail:
        story.append(Paragraph(f"<b>{filename}</b>", h2_style))
        story.append(Paragraph(desc, body_style))
        
    story.append(Spacer(1, 10))
    
    # =========================================================================
    # SECTION 4: SECURITY & RESTORATION LAYER
    # =========================================================================
    story.append(Paragraph("4. Defensive Security & Quality Restoration Layer", h1_style))
    
    sec_intro = """
    A critical element of clinical software is defensive validation.
    OncoDetect AI implements a double-stage defensive pipeline in <b>secure_image_loader.py</b>
    and <b>validator_inference.py</b> to protect downstream neural networks.
    """
    story.append(Paragraph(sec_intro, body_style))
    
    story.append(Paragraph("The Nine Defensive Validation Gates", h2_style))
    
    gates = [
        "<b>1. File Integrity:</b> Opens files in PIL and invokes verify() to catch truncated byte streams or broken compression formats.",
        "<b>2. Size Boundaries:</b> Restricts resolutions to a minimum of 32x32 pixels, and maximum file size to 10MB.",
        "<b>3. Blank/Uniform Screen Check:</b> Calculates standard deviation of pixel values. Values below 8.0 identify empty slides, white pages, or single-color background errors.",
        "<b>4. Noise / Blur Restoration Check:</b> Estimates blur/noise variance using a Laplacian operator. Triggers auto-enhancement if Laplacian variance is below 15.0 or noise sigma exceeds 4.0.",
        "<b>5. Grayscale Block:</b> Examines total inter-channel variance. Scans with differences below 15 (monochrome CT, MRI, X-rays) are rejected, as the network expects color H&E stains.",
        "<b>6. Post-Restoration Blur Check:</b> Re-evaluates Laplacian variance after restoration. If it remains below 3.0, the image is blocked as unreadable.",
        "<b>7. Text & Screenshot Detection:</b> Applies adaptive binarization and filters connected components for small rectangular shapes. Prevents doctors from uploading PDF charts or UI screenshots.",
        "<b>8. Hough Line Geometric Gate:</b> Uses Canny edge detection and Probabilistic Hough Line Transforms. If 8+ straight lines are found, it identifies the image as a chart/document and rejects it.",
        "<b>9. Low Saturation/Staining Check:</b> Evaluates mean saturation. Values below 18.0 indicate unstained tissue patches and reject the upload."
    ]
    for gate in gates:
        story.append(Paragraph(gate, bullet_style))
        
    story.append(Spacer(1, 10))
    story.append(PageBreak())
    
    # Keep Restoration details together
    restoration_story = []
    restoration_story.append(Paragraph("Automatic Image Restoration Pipeline", h2_style))
    restoration_story.append(Paragraph(
        "If an image is identified as a valid H&E medical slide but displays blur or noise, the system "
        "dynamically triggers a restoration pipeline using OpenCV prior to ML inference:",
        body_style
    ))
    
    enhancement_steps = [
        "<b>Luminance Separation:</b> Converts the RGB array to YCrCb space, isolating the luminance channel (Y) to prevent color shifts or chromatic distortion.",
        "<b>Edge-Preserving Denoising:</b> Applies a Bilateral Filter (d=5, sigmaColor=50, sigmaSpace=50) to the Y channel to smooth high-frequency background noise while keeping sharp cell borders.",
        "<b>Unsharp Masking:</b> Sharpening is achieved by applying a Gaussian Blur (5x5 kernel) to the denoised Y channel, and adding a weighted difference back: <i>Sharpened = Denoised * 1.8 - Blurred * 0.8</i>.",
        "<b>RGB Recomposition:</b> Re-merges channels back into YCrCb and converts back to RGB, saving the enhanced bytes."
    ]
    for step in enhancement_steps:
        restoration_story.append(Paragraph(f"• {step}", bullet_style))
        
    story.append(KeepTogether(restoration_story))
    story.append(Spacer(1, 10))
    
    # =========================================================================
    # SECTION 5: MACHINE LEARNING PIPELINE
    # =========================================================================
    story.append(Paragraph("5. AI Models, Training, & Explainability (XAI)", h1_style))
    
    ml_intro = """
    OncoDetect AI features a double-stage model configuration: a MobileNetV2 medical scan validator,
    and a custom cancer classifier.
    """
    story.append(Paragraph(ml_intro, body_style))
    
    story.append(Paragraph("Model 1: MobileNetV2 Medical Image Validator", h2_style))
    story.append(Paragraph(
        "A binary classifier determining if an upload is a histopathological slide or a generic scene image. "
        "Built using Transfer Learning with a pre-trained MobileNetV2 base (ImageNet weights) with custom head layers:",
        body_style
    ))
    
    code_layers = """InputLayer(96x96x3)
  --> Preprocessing Lambda (normalize input to [-1, 1])
  --> MobileNetV2 Frozen Base (without classification top)
  --> GlobalAveragePooling2D()
  --> Dropout(rate=0.3)
  --> Dense(128 units, Activation='relu')
  --> Dropout(rate=0.2)
  --> Dense(1 unit, Activation='sigmoid')"""
    story.append(Paragraph(code_layers, code_style))
    
    story.append(Paragraph("Validator Training Protocol (validator_train.py)", h3_style))
    story.append(Paragraph(
        "Training runs in two phases: Phase 1 fits the customized classification head for 5 epochs using "
        "Adam (learning rate 1e-4) while freezing the base model. Phase 2 unfreezes the top 20 convolutional "
        "layers of MobileNetV2, running fine-tuning with a very low learning rate (1e-5) for domain adaptation. "
        "Mixed precision training is used to speed up training on GPUs.",
        body_style
    ))

    story.append(Paragraph("Fallback Feature-Classifier (train_medical_classifier.py)", h3_style))
    story.append(Paragraph(
        "If TensorFlow is not available, the system uses a custom 40-dimensional Logistic Regression model "
        "trained on HSV histogram features (18 Hue bins, 8 Saturation bins, 8 Value bins) and 6 statistical features "
        "(mean saturation, mean value, non-medical color ratio, and standard deviations).",
        body_style
    ))
    
    story.append(Paragraph("Explainable AI (Grad-CAM)", h2_style))
    story.append(Paragraph(
        "To provide transparency, the system computes Gradient-Weighted Class Activation Mapping (Grad-CAM) "
        "for the validator and classifier. By tracking the output of the final convolutional layer relative to "
        "prediction logits, the system generates spatial focus heatmaps showing where the AI focused to make its decision.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # =========================================================================
    # SECTION 6: API ROUTES
    # =========================================================================
    story.append(Paragraph("6. REST API Endpoint Specifications", h1_style))
    
    api_data = [
        [Paragraph("<b>Route</b>", body_style), Paragraph("<b>Method</b>", body_style), Paragraph("<b>Auth</b>", body_style), Paragraph("<b>Description</b>", body_style)],
        [Paragraph("<code>/api/register</code>", body_style), Paragraph("POST", body_style), Paragraph("Public", body_style), Paragraph("Registers user, hashes password via bcrypt, flags first user as admin.", body_style)],
        [Paragraph("<code>/api/token</code>", body_style), Paragraph("POST", body_style), Paragraph("Public", body_style), Paragraph("Authenticates username and password, returns an HS256 JWT.", body_style)],
        [Paragraph("<code>/api/users/me</code>", body_style), Paragraph("GET", body_style), Paragraph("Bearer JWT", body_style), Paragraph("Decodes the JWT token and returns current user details.", body_style)],
        [Paragraph("<code>/api/patients</code>", body_style), Paragraph("GET", body_style), Paragraph("Bearer JWT", body_style), Paragraph("Lists all patients registered under the current doctor.", body_style)],
        [Paragraph("<code>/api/predict</code>", body_style), Paragraph("POST", body_style), Paragraph("Bearer JWT", body_style), Paragraph("Accepts Form-data image file + patient details. Runs quality filters, gets/creates the patient, runs ML cancer prediction, logs output, and returns heatmaps.", body_style)],
        [Paragraph("<code>/api/predictions/history</code>", body_style), Paragraph("GET", body_style), Paragraph("Bearer JWT", body_style), Paragraph("Returns diagnostic scan logs for the active doctor.", body_style)],
        [Paragraph("<code>/api/admin/stats</code>", body_style), Paragraph("GET", body_style), Paragraph("Admin JWT", body_style), Paragraph("Returns global metrics: user counts, total predictions, cancer rates, and a history of the last 10 scans.", body_style)]
    ]
    
    api_table = Table(api_data, colWidths=[105, 55, 65, 279])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('BOX', (0,0), (-1,-1), 1, primary_color),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(api_table)
    
    story.append(Spacer(1, 15))
    
    # =========================================================================
    # SECTION 7: FRONTEND OVERVIEW
    # =========================================================================
    story.append(Paragraph("7. Frontend Client Implementation", h1_style))
    
    frontend_text = """
    The frontend application is built in React utilizing Vite, Tailwind CSS v4 for styling, and Framer Motion for animations.
    Here is an overview of the key components and views:
    """
    story.append(Paragraph(frontend_text, body_style))
    
    pages = [
        ("App.jsx", "Configures routing and manages JWT auth state via Axios interceptors. Automatically checks token validation on mount."),
        ("Navbar.jsx", "Header component showing path options (Dashboard, Upload, Microscope Scan, Admin panel) based on user credentials."),
        ("Landing.jsx", "Marketing page outlining system features, visual quality gates, and AI capabilities."),
        ("Dashboard.jsx", " Pathologist workstation, displaying analytics tiles (Patient Counts, Scan Totals, Positive cases, alerts) and quick-action links."),
        ("Upload.jsx", "Diagnostic workspace featuring drag-and-drop file zones, patient ID matching, quality gate status alerts, and side-by-side original/enhanced scans with Grad-CAM overlays."),
        ("ReportModal.jsx", "Interactive clinical pathology report preview. Formats layouts dynamically to print high-resolution reports, download text summaries, or sign off diagnostic results.")
    ]
    for page_name, page_desc in pages:
        story.append(Paragraph(f"<b>{page_name}</b>", h2_style))
        story.append(Paragraph(page_desc, body_style))
        
    story.append(Spacer(1, 10))
    story.append(PageBreak())
    
    # Motion Scan Details
    story.append(Paragraph("Microscope Scanner Page (MotionScan.jsx)", h2_style))
    story.append(Paragraph(
        "The Microscope Scanner connects directly to electronic microscope feeds or USB webcams via browser "
        "navigator.mediaDevices APIs. To support automated diagnostic collection, the component implements a "
        "pixel-differencing motion analysis algorithm:",
        body_style
    ))
    
    motion_steps = [
        "<b>Differencing Loop:</b> Draws incoming video frames onto an offscreen 96x96 canvas every 200ms.",
        "<b>Variance Check:</b> Loops through the image matrix comparing red, green, and blue values of current and previous frames. Differences over 18 identify changed pixels.",
        "<b>Trigger Event:</b> Computes the percentage of changed pixels to total pixels. When this value crosses the user's sensitivity threshold, it captures a 512x512 crop from the video feed.",
        "<b>Safety Lock:</b> Applies a 10-second cooldown to prevent duplicate uploads while the slide is moving, and sends the capture to the backend /api/predict route."
    ]
    for step in motion_steps:
        story.append(Paragraph(step, bullet_style))
        
    story.append(Spacer(1, 15))
    
    # =========================================================================
    # SECTION 8: RUNNING & DEPLOYING
    # =========================================================================
    story.append(Paragraph("8. Running & Deploying OncoDetect AI", h1_style))
    
    deploy_text = """
    The application can be run locally for development or deployed inside Docker containers for staging environments.
    """
    story.append(Paragraph(deploy_text, body_style))
    
    story.append(Paragraph("Local Development Execution", h2_style))
    
    dev_steps = """# 1. Start the FastAPI server
cd server
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 2. Start the Vite React app (in a separate terminal)
cd client
npm install
npm run dev"""
    story.append(Paragraph(dev_steps, code_style))
    
    story.append(Paragraph("Docker Compose Architecture", h2_style))
    story.append(Paragraph(
        "Using the root <code>docker-compose.yml</code> file, the application spins up two services: "
        "the FastAPI server (mapped to port 8000) and the React web app compiled and served through Nginx "
        "(mapped to port 80). The services are orchestrated automatically with:",
        body_style
    ))
    story.append(Paragraph("docker-compose up --build -d", code_style))
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_filename}!")

if __name__ == "__main__":
    generate_report()
